# analysis_enhancements.py
import streamlit as st
import json
from ai_logic import ask_gemini # Import the AI utility function

def get_risk_score(schema_diff: dict) -> str:
    """
    Uses Gemini AI to generate a risk score (1-10) for schema changes.
    Returns the AI's explanation and score.
    """
    if not schema_diff:
        return "N/A - No schema differences to score."

    prompt = f"""
    Based on the following schema difference report in JSON format, assess the potential risk (from 1 to 10, where 1 is minimal risk and 10 is very high risk) that these changes pose to existing data pipelines (ETLs), dashboards, and applications.

    Consider factors like:
    - Deletion of tables/columns
    - Data type changes (especially incompatible ones like VARCHAR to INT)
    - Column renames
    - Changes in primary/foreign key constraints
    - Overall volume and complexity of changes

    Provide a concise explanation for the risk score.

    Schema Difference Report:
    ```json
    {json.dumps(schema_diff, indent=2)}
    ```

    Format your response as follows:
    **Risk Score:** [Score 1-10]
    **Explanation:** [Concise explanation of why this score was given, highlighting key risk factors.]
    """

    try:
        with st.spinner("Calculating impact-aware risk score... 🚦"):
            ai_response = ask_gemini(prompt)
            return ai_response
    except Exception as e:
        return f"Error calculating risk score: {e}"

def get_regression_test_suggestions(schema_diff: dict, old_schema: dict, new_schema: dict) -> str:
    """
    Uses Gemini AI to suggest regression tests based on schema changes.
    Returns the AI's suggestions.
    """
    if not schema_diff:
        return "No schema differences to suggest tests for."

    prompt = f"""
    Based on the following schema difference report, provide specific suggestions for regression tests that should be performed after these database schema changes are implemented.

    Focus on different areas:
    - **Data Integrity Tests:** (e.g., ensure no data loss, referential integrity)
    - **ETL/ELT Pipeline Tests:** (e.g., ensuring data flows correctly, transformations work)
    - **Reporting/Dashboard Tests:** (e.g., data accuracy, dashboard rendering)
    - **Application Tests:** (e.g., API integrations, user-facing features)
    - **Performance Tests:** (e.g., query performance, load times)

    Consider the detailed changes (added, deleted, modified, renamed tables/columns) to provide tailored suggestions.

    Old Schema (for context):
    ```json
    {json.dumps(old_schema, indent=2)}
    ```
    New Schema (for context):
    ```json
    {json.dumps(new_schema, indent=2)}
    ```
    Schema Difference Report:
    ```json
    {json.dumps(schema_diff, indent=2)}
    ```

    Format your response using **Markdown** with clear headings and bullet points for each test category.
    """
    try:
        with st.spinner("Generating automated regression test suggestions... 🧪"):
            ai_response = ask_gemini(prompt)
            return ai_response
    except Exception as e:
        return f"Error generating test suggestions: {e}"

