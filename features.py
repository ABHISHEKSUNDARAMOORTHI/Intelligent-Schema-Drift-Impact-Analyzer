# features.py
import streamlit as st
import json
import re
from ai_logic import ask_gemini # Import ask_gemini
from schema_utils import strip_sql_comments_and_normalize, parse_create_table_statement, compare_schemas # Import utility functions
import os # New import for file operations
from datetime import datetime # New import for timestamping

# Define a directory to store historical drift reports
HISTORY_DIR = "schema_drift_history"

def render_input_section():
    """Renders the input text areas for old and new schemas and the compare button."""
    st.markdown("<h2>Input Schema Versions</h2>", unsafe_allow_html=True)
    st.markdown("<p>Paste your old (v1) and new (v2) table schema definitions below. Supported formats: SQL <code>CREATE TABLE</code> statements or simple JSON schema arrays.</p>", unsafe_allow_html=True)

    col_old_schema, col_new_schema = st.columns(2, gap="large")

    with col_old_schema:
        st.markdown("<h3><i class='fas fa-code-branch'></i> Old Schema (Version 1)</h3>", unsafe_allow_html=True)
        st.session_state.old_schema_input = st.text_area(
            "Paste Old Schema SQL or JSON here:",
            value=st.session_state.old_schema_input,
            height=400,
            key="old_schema_input_area"
        )

    with col_new_schema:
        st.markdown("<h3><i class='fas fa-code-pull-request'></i> New Schema (Version 2)</h3>", unsafe_allow_html=True)
        st.session_state.new_schema_input = st.text_area(
            "Paste New Schema SQL or JSON here:",
            value=st.session_state.new_schema_input,
            height=400,
            key="new_schema_input_area"
        )

    # The button directly calls generate_drift_report
    if st.button("🚀 Compare Schemas & Analyze Drift", type="primary", use_container_width=True, key="analyze_drift_btn"):
        generate_drift_report()


def generate_drift_report():
    """
    Parses schemas, compares them, and generates an AI report on schema drift.
    Updates st.session_state.schema_diff_report and st.session_state.diff_summary_metrics.
    Also saves the analysis to a historical log.
    """
    old_schema_raw = st.session_state.old_schema_input
    new_schema_raw = st.session_state.new_schema_input

    # Ensure inputs are not empty before proceeding
    if not old_schema_raw.strip() or not new_schema_raw.strip():
        st.error("⚠️ Please provide both Old and New schema definitions in the text areas above to perform a comparison.")
        st.session_state.schema_diff_report = ""
        st.session_state.diff_summary_metrics = {} # Clear metrics on error
        return # Exit the function early if inputs are missing

    # Clear previous report and metrics to give immediate feedback on new attempt
    st.session_state.schema_diff_report = ""
    st.session_state.diff_summary_metrics = {}

    # 1. Parse Schemas
    try:
        with st.spinner("Parsing schemas..."):
            # Try parsing old schema as JSON first (after stripping comments)
            cleaned_old_input = strip_sql_comments_and_normalize(old_schema_raw)
            try:
                parsed_json_old = json.loads(cleaned_old_input)
                temp_old_schema = {}
                for table_obj in parsed_json_old:
                    table_name = table_obj.get('table_name', 'untitled_table').lower()
                    columns_data = {}
                    for col_obj in table_obj.get('columns', []):
                        col_name_lower = col_obj.get('name', 'untitled_col').lower()
                        columns_data[col_name_lower] = {
                            'type': col_obj.get('type', 'UNKNOWN').lower(),
                            'is_pk': col_obj.get('is_pk', False),
                            'nullable': not col_obj.get('not_null', False), # Infer nullable from not_null
                            'unique': col_obj.get('unique', False)
                        }
                    temp_old_schema[table_name] = columns_data
                st.session_state.parsed_old_schema = temp_old_schema
            except json.JSONDecodeError:
                # If not JSON, assume SQL and parse it
                st.session_state.parsed_old_schema = parse_create_table_statement(old_schema_raw)
            
            # Try parsing new schema as JSON first (after stripping comments)
            cleaned_new_input = strip_sql_comments_and_normalize(new_schema_raw)
            try:
                parsed_json_new = json.loads(cleaned_new_input)
                temp_new_schema = {}
                for table_obj in parsed_json_new:
                    table_name = table_obj.get('table_name', 'untitled_table').lower()
                    columns_data = {}
                    for col_obj in table_obj.get('columns', []):
                        col_name_lower = col_obj.get('name', 'untitled_col').lower()
                        columns_data[col_name_lower] = {
                            'type': col_obj.get('type', 'UNKNOWN').lower(),
                            'is_pk': col_obj.get('is_pk', False),
                            'nullable': not col_obj.get('not_null', False),
                            'unique': col_obj.get('unique', False)
                        }
                    temp_new_schema[table_name] = columns_data
                st.session_state.parsed_new_schema = temp_new_schema
            except json.JSONDecodeError:
                st.session_state.parsed_new_schema = parse_create_table_statement(new_schema_raw)

    except Exception as e:
        st.error(f"❌ Error during schema parsing: {e}. Please ensure your input format (SQL or JSON) is valid and well-formed.")
        st.session_state.parsed_old_schema = {}
        st.session_state.parsed_new_schema = {}
        st.session_state.diff_summary_metrics = {}
        return

    # Check if parsing resulted in empty schemas (meaning parsing failed for practical purposes)
    if not st.session_state.parsed_old_schema and not st.session_state.parsed_new_schema:
        st.error("❌ Both schemas could not be parsed. Please check the input format carefully (SQL CREATE TABLE or valid JSON).")
        st.session_state.schema_diff_report = ""
        st.session_state.diff_summary_metrics = {}
        return
    elif not st.session_state.parsed_old_schema:
        st.warning("⚠️ Could not parse **Old Schema**. The report will only show additions from the New Schema or might be incomplete.")
    elif not st.session_state.parsed_new_schema:
        st.warning("⚠️ Could not parse **New Schema**. The report will only show deletions from the Old Schema or might be incomplete.")


    # 2. Compare Schemas
    with st.spinner("Comparing schemas for drift..."):
        schema_diff = compare_schemas(st.session_state.parsed_old_schema, st.session_state.parsed_new_schema)
    
    # --- Debugging Output START ---
    # st.write("--- Debugging Schema Diff ---")
    # st.write("Raw Schema Diff:", schema_diff)
    # st.write("Modified Tables in Diff (for column counts):", schema_diff.get("modified_tables", {}))
    # --- Debugging Output END ---


    # Calculate summary metrics
    total_tables_old = len(st.session_state.parsed_old_schema)
    total_tables_new = len(st.session_state.parsed_new_schema)
    added_table_count = len(schema_diff["added_tables"])
    deleted_table_count = len(schema_diff["deleted_tables"])
    modified_table_count = len(schema_diff["modified_tables"])

    added_column_count = sum(len(td["added_columns"]) for td in schema_diff["modified_tables"].values())
    deleted_column_count = sum(len(td["deleted_columns"]) for td in schema_diff["modified_tables"].values())
    modified_column_count = sum(len(td["modified_columns"]) for td in schema_diff["modified_tables"].values())
    
    # Add renamed column count
    renamed_column_count = sum(len(td["renamed_columns"]) for td in schema_diff["modified_tables"].values())


    st.session_state.diff_summary_metrics = {
        "total_tables_old": total_tables_old,
        "total_tables_new": total_tables_new,
        "added_table_count": added_table_count,
        "deleted_table_count": deleted_table_count,
        "modified_table_count": modified_table_count,
        "added_column_count": added_column_count,
        "deleted_column_count": deleted_column_count,
        "modified_column_count": modified_column_count,
        "renamed_column_count": renamed_column_count, # Add this to metrics
    }

    # --- Debugging Output START ---
    # st.write("Calculated Diff Summary Metrics:", st.session_state.diff_summary_metrics)
    # st.write("--- End Debugging ---")
    # --- Debugging Output END ---


    # 3. Generate AI Report
    prompt = f"""
    You are an expert data architect tasked with analyzing schema drift.
    I am providing you with a structured comparison between an OLD database schema and a NEW version.
    Your task is to generate a comprehensive, human-readable report detailing the schema changes.
    For each significant change, explain its potential impact on existing data pipelines, reports, and applications.
    Suggest practical remediation steps or considerations for data engineers.

    The schema comparison is as follows (in JSON format):
    ```json
    {json.dumps(schema_diff, indent=2)}
    ```

    Please format your response using **Markdown** with the following highly structured and clear sections, making it easy for new team members to understand:

    1.  **Overall Executive Summary:** A high-level overview of the most critical changes. Highlight the total number of tables added, deleted, or modified, and columns added, deleted, or modified.

    For each table affected by schema drift, create a dedicated section:
    ### 📁 Table: [Table Name]
    ---
    Within each table section, use these sub-sections:

    #### **➕ Columns Added**
    * List each added column.
    * For each: `Column Name: \`[name]\` (Type: \`[type]\`)`
    * Add a brief note on its purpose or what it might contain (e.g., "This new column will capture ...").

    #### **❌ Columns Deleted**
    * List each deleted column.
    * For each: `Column Name: \`[name]\` (Type: \`[type]\`)`
    * Add a note on potential data loss or breaking changes (e.g., "Deletion of this column will lead to data loss for ... and might break ...").

    #### **✏️ Columns Modified**
    * List each modified column.
    * For each modified column:
        * `Column Name: \`[name]\``
        * `Old Type: \`[old_type_details]\``
        * `New Type: \`[new_type_details]\``
        * **Impact 🔥:** Explain the specific impact of this modification (e.g., "Data type change from X to Y might break ETL jobs expecting the old format and require data migration.").
        * **Remediation 🛠️:** Suggest specific actions to resolve the impact (e.g., "Update ETL scripts, perform data backfill/migration, review downstream application logic, and conduct thorough regression testing.").

    #### **🔁 Renamed Columns**
    * If the `schema_diff` includes a `renamed_columns` section for this table, list them here explicitly.
    * For each renamed column: `\`[Old Name]\` ➡️ \`[New Name]\`` (Old Type: \`[old_type]\` -> New Type: \`[new_type]\`)
    * Add a note on the impact of the rename (e.g., "Renaming requires updating all queries and applications referencing the old name.").
    * If no renames are detected for a table by the diff, explicitly state: `No inferred renames detected for this table.`

    ---
    Finally, conclude the report with:

    ### **✅ General Best Practices & Proactive Schema Governance Tips**
    * Provide bullet points on best practices for managing schema evolution (e.g., version control, backward compatibility, communication with stakeholders).
    * Suggest proactive measures to minimize schema drift impact (e.g., using views, robust ETL error handling).

    Ensure all explanations are clear, concise, and actionable for a data engineering team.
    """
    
    ai_report = "" # Initialize here to ensure it's always defined
    try:
        with st.spinner("Generating AI-powered schema drift analysis..."):
            ai_report = ask_gemini(prompt)
            st.session_state.schema_diff_report = ai_report
            st.toast("Drift analysis complete! 🚀 Check the report below.")
    except Exception as e:
        st.error(f"❌ Error generating AI report: {e}. This might be due to API key issues, rate limits, or a very complex input for the AI.")
        st.session_state.schema_diff_report = f"Error: Could not generate AI report. {e}"

    # --- New: Save analysis to historical log ---
    try:
        os.makedirs(HISTORY_DIR, exist_ok=True) # Create directory if it doesn't exist
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(HISTORY_DIR, f"drift_report_{timestamp}.json")

        historical_data = {
            "timestamp": timestamp,
            "old_schema_raw": old_schema_raw,
            "new_schema_raw": new_schema_raw,
            "parsed_old_schema": st.session_state.parsed_old_schema, # Save parsed schemas too
            "parsed_new_schema": st.session_state.parsed_new_schema,
            "schema_diff": schema_diff,
            "summary_metrics": st.session_state.diff_summary_metrics,
            "ai_report_markdown": ai_report # Save the generated markdown report
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(historical_data, f, indent=2)
        st.success(f"Analysis saved to historical log: `{filename}`")
    except Exception as e:
        st.error(f"Failed to save historical analysis: {e}")

