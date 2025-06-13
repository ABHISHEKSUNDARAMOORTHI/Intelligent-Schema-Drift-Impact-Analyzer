# schema_utils.py
import re
import json
from Levenshtein import distance as levenshtein_distance # Using Levenshtein for string similarity

# --- Helper Function for Input Cleaning ---
def strip_sql_comments_and_normalize(sql_string):
    """
    Removes SQL comments (--, /* */) and normalizes whitespace.
    Aims to clean input for parsing, not to be a full SQL parser.
    """
    # Remove single-line comments (--)
    cleaned = re.sub(r"--.*$", "", sql_string, flags=re.MULTILINE)
    # Remove multi-line comments (/* ... */)
    cleaned = re.sub(r"/\*[\s\S]*?\*/", "", cleaned, flags=re.DOTALL)
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def parse_create_table_statement(sql_statement):
    """
    Simple parser to extract table name and columns from a CREATE TABLE SQL statement.
    This is a simplified parser and may not handle all edge cases or complex SQL syntax.
    Returns a dictionary: {table_name: {column_name: {type: ..., nullable: ..., primary_key: ..., etc.}}}
    """
    schema = {}
    
    # Regex to find CREATE TABLE statements and their content
    table_matches = re.findall(r"CREATE TABLE (\w+)\s*\((.*?)\);", sql_statement, re.IGNORECASE | re.DOTALL)

    for table_name, columns_str in table_matches:
        table_name = table_name.lower()
        columns_info = {}
        
        # Split columns and process each
        column_defs = re.findall(r"(\w+)\s+([\w\(\),\s]+)(?: PRIMARY KEY| NOT NULL| UNIQUE| REFERENCES \w+\(\w+\)| DEFAULT [^,]+)*", columns_str, re.IGNORECASE)
        

        for col_name, col_type_str in column_defs:
            col_name = col_name.lower()
            col_type = col_type_str.strip().lower()
            
            # Simple attribute detection (can be expanded)
            is_pk = 'primary key' in columns_str.lower() and col_name in columns_str.lower()
            nullable = 'not null' not in columns_str.lower() or col_name + ' not null' not in columns_str.lower() # basic, might be inaccurate
            is_unique = 'unique' in columns_str.lower() and col_name in columns_str.lower()

            columns_info[col_name] = {
                'type': col_type,
                'nullable': nullable,
                'primary_key': is_pk,
                'unique': is_unique,
                # Add more attributes as needed (e.g., default value, foreign key references)
            }
        
        schema[table_name] = columns_info
    return schema

# --- Schema Comparison (Diffing) Logic ---
def compare_schemas(old_schema, new_schema):
    """
    Compares two parsed schema dictionaries and returns a detailed diff,
    including inferred column renames using Levenshtein distance.
    """
    diffs = {
        "added_tables": [],
        "deleted_tables": [],
        "modified_tables": {}, # {table_name: {added_cols:[], deleted_cols:[], modified_cols:{}, renamed_cols:{}}}
    }

    # Identify added and deleted tables
    old_tables = set(old_schema.keys())
    new_tables = set(new_schema.keys())

    diffs["added_tables"] = list(new_tables - old_tables)
    diffs["deleted_tables"] = list(old_tables - new_tables)

    # Compare common tables for column changes
    for table_name in old_tables.intersection(new_tables):
        old_cols = old_schema[table_name]
        new_cols = new_schema[table_name]

        table_diff = {
            "added_columns": [],
            "deleted_columns": [],
            "modified_columns": {}, # {col_name: {old_props: {}, new_props: {}}}
            "renamed_columns": {} # {old_name: new_name, old_type: ..., new_type: ...}
        }

        old_col_names = list(old_cols.keys()) # Convert to list for easier iteration
        new_col_names = list(new_cols.keys()) # Convert to list

        # Initialize lists for columns truly added/deleted after rename inference
        temp_added_columns = list(set(new_col_names) - set(old_col_names))
        temp_deleted_columns = list(set(old_col_names) - set(new_col_names))

        # --- Inferred Column Renames Logic ---
        # A simple approach: iterate through deleted and added columns
        # and find the best match based on Levenshtein distance and similar type.
        # This can be complex for many-to-many renames or very short names.
        
        rename_threshold = 2 # Max Levenshtein distance for a rename candidate
        matched_new_cols = set() # To ensure an added column is only matched once

        for deleted_col_name in list(temp_deleted_columns): # Iterate over a copy
            best_match = None
            min_distance = float('inf')
            
            for added_col_name in list(temp_added_columns): # Iterate over a copy
                # Ensure it hasn't been matched yet
                if added_col_name in matched_new_cols:
                    continue

                # Check if types are roughly compatible (e.g., both numerical, both string-like)
                # This is a simple type compatibility check, can be made more robust.
                old_type = old_cols.get(deleted_col_name, {}).get('type')
                new_type = new_cols.get(added_col_name, {}).get('type')

                # Basic type compatibility check
                types_compatible = False
                if old_type and new_type:
                    if old_type == new_type: # Exact type match
                        types_compatible = True
                    elif 'int' in old_type and 'int' in new_type: # int vs integer
                        types_compatible = True
                    elif 'decimal' in old_type and 'decimal' in new_type: # float vs decimal
                        types_compatible = True
                    elif 'varchar' in old_type and 'varchar' in new_type: # varchar length changes
                         types_compatible = True
                    elif 'text' in old_type and 'varchar' in new_type:
                         types_compatible = True
                    elif 'date' in old_type and 'date' in new_type: # date vs timestamp
                         types_compatible = True


                # Calculate Levenshtein distance
                dist = levenshtein_distance(deleted_col_name, added_col_name)
                
                # Consider a rename if distance is low and types are compatible
                if dist <= rename_threshold and types_compatible and dist < min_distance:
                    min_distance = dist
                    best_match = added_col_name

            if best_match:
                table_diff["renamed_columns"][deleted_col_name] = {
                    "new_name": best_match,
                    "old_type": old_cols[deleted_col_name]['type'],
                    "new_type": new_cols[best_match]['type']
                }
                temp_deleted_columns.remove(deleted_col_name)
                temp_added_columns.remove(best_match)
                matched_new_cols.add(best_match) # Mark this new column as matched

        table_diff["added_columns"] = temp_added_columns
        table_diff["deleted_columns"] = temp_deleted_columns

        # Check for modified columns (common names, *after* rename inference)
        # This now only considers columns that were NOT identified as renames.
        common_col_names_after_rename = set(old_cols.keys()).intersection(set(new_cols.keys()))
        for renamed_old_name, rename_info in table_diff["renamed_columns"].items():
            if renamed_old_name in common_col_names_after_rename:
                common_col_names_after_rename.remove(renamed_old_name) # Ensure renamed old name is not checked as modified
            if rename_info["new_name"] in common_col_names_after_rename:
                common_col_names_after_rename.remove(rename_info["new_name"]) # Ensure renamed new name is not checked as modified


        for col_name in common_col_names_after_rename:
            old_props = old_cols[col_name]
            new_props = new_cols[col_name]
            
            if old_props != new_props:
                modified_props = {}
                for prop_key in set(old_props.keys()).union(new_props.keys()):
                    if old_props.get(prop_key) != new_props.get(prop_key):
                        modified_props[prop_key] = {
                            "old_value": old_props.get(prop_key),
                            "new_value": new_props.get(prop_key)
                        }
                table_diff["modified_columns"][col_name] = modified_props
        
        # Only add table_diff if there were actual changes within the table
        if any(table_diff[key] for key in ["added_columns", "deleted_columns", "modified_columns", "renamed_columns"]):
            diffs["modified_tables"][table_name] = table_diff

    return diffs

