# additional_features.py
import streamlit as st
import json
import os
from io import StringIO, BytesIO # Import BytesIO for in-memory binary file operations
from schema_utils import compare_schemas # Import compare_schemas for raw diff download
from analysis_enhancements import get_risk_score, get_regression_test_suggestions # NEW: Import new analysis functions

# New imports for multi-format export
import pandas as pd # Already used, but explicitly mentioning for Excel
import re # For regex operations in text cleaning


# Define a directory to store historical drift reports (must match features.py)
HISTORY_DIR = "schema_drift_history"


# --- Helper function to break long "words" (strings without spaces) - No longer needed if PDF is removed, but kept for safety
# def break_long_strings(text, max_len=90):
#     """
#     Inserts spaces into very long strings (without natural spaces) to help FPDF
#     with word wrapping, preventing "Not enough horizontal space" errors.
#     """
#     words = text.split(' ')
#     result_words = []
#     for word in words:
#         if len(word) > max_len:
#             # Break the long word into chunks, inserting a space
#             chunked_word = [word[i:i+max_len] for i in range(0, len(word), max_len)]
#             result_words.append(' '.join(chunked_word))
#         else:
#             result_words.append(word)
#     return ' '.join(result_words)


def render_output_section():
    """Renders the AI-generated schema drift report and download options."""
    # --- Custom CSS for Interactive Diff Viewer and Metric Cards ---
    st.markdown("""
    <style>
    /* Metric Card Styles (already existing, ensuring they are here) */
    .metrics-grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .custom-metric-card {
        background-color: #2d3748; /* Darker card background */
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #4a5568; /* Subtle border */
        position: relative;
        overflow: hidden;
    }
    .custom-metric-content {
        flex-grow: 1;
    }
    .custom-metric-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #63b3ed; /* Light blue for values */
        margin-bottom: 0.2em;
    }
    .custom-metric-label {
        font-size: 0.9em;
        color: #a0aec0; /* Subtler gray for labels */
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .custom-metric-label i {
        margin-right: 0.5em;
        color: #4299e1; /* Icon color */
    }
    .custom-metric-delta {
        font-size: 1.2em;
        font-weight: bold;
        padding: 0.3em 0.6em;
        border-radius: 6px;
        position: absolute;
        top: 10px;
        right: 10px;
        text-align: center;
        min-width: 40px;
    }
    .delta-positive { background-color: #22543d; color: #68d391; } /* Green */
    .delta-negative { background-color: #63171b; color: #fc8181; } /* Red */
    .delta-neutral { background-color: #2a4365; color: #a0aec0; } /* Gray-blue */

    /* Card type specific colors */
    .custom-metric-card-added { border-left: 5px solid #68d391; }
    .custom-metric-card-deleted { border-left: 5px solid #fc8181; }
    .custom-metric-card-modified { border-left: 5px solid #ecc94b; }
    .custom-metric-card-info { border-left: 5px solid #4299e1; }


    /* --- Interactive Diff Viewer Styles --- */
    .diff-viewer-container {
        font-family: 'Fira Code', 'Cascadia Code', monospace;
        background-color: #1a202c;
        border: 1px solid #4a5568;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        max-height: 700px; /* Limit height for scroll */
        overflow-y: auto; /* Scroll for overflowing content */
    }
    .diff-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1.5rem;
    }
    .diff-table th, .diff-table td {
        padding: 10px 15px;
        border: 1px solid #4a5568; /* Table borders */
        text-align: left;
        vertical-align: top;
        font-size: 0.9em;
    }
    .diff-table th {
        background-color: #2d3748; /* Header background */
        color: #e2e8f0;
        font-weight: 600;
    }
    .diff-table tr:nth-child(even) {
        background-color: #1f2a3a; /* Zebra stripping */
    }
    .diff-table tr:nth-child(odd) {
        background-color: #1a202c;
    }

    /* Diff Colors */
    .diff-added { background-color: rgba(78, 196, 117, 0.2); color: #68d391; } /* Light Green */
    .diff-deleted { background-color: rgba(239, 68, 68, 0.2); color: #fc8181; } /* Light Red */
    .diff-modified { background-color: rgba(251, 191, 36, 0.2); color: #ecc94b; } /* Light Yellow/Orange */
    .diff-renamed { background-color: rgba(99, 179, 237, 0.2); color: #63b3ed; } /* Light Blue */

    /* Label Colors */
    .diff-label { font-weight: bold; }
    .diff-added-label { color: #68d391; }
    .diff-deleted-label { color: #fc8181; }
    .diff-modified-label { color: #ecc94b; }
    .diff-renamed-label { color: #63b3ed; }

    /* Icons within diff */
    .diff-icon {
        margin-right: 8px;
        font-size: 1.1em;
    }

    /* Streamlit Expander overrides for a custom look */
    .streamlit-expanderHeader {
        background-color: #2d3748; /* Darker header for expanders */
        color: #e2e8f0 !important; /* Text color */
        font-weight: 600;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #4a5568;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #4a5568; /* Hover state for expander header */
    }
    .streamlit-expanderContent {
        background-color: #1a202c; /* Content area background */
        border: 1px solid #4a5568;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
    }
    .streamlit-expanderHeader .icon-arrow_right,
    .streamlit-expanderHeader .icon-arrow_down {
        color: #63b3ed !important; /* Make arrow icon blue */
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown("<h2>AI-Generated Schema Drift Report</h2>", unsafe_allow_html=True)

    # Create tabs for current report, historical reports, and the new Interactive Diff Viewer
    tab_current, tab_history, tab_diff_viewer = st.tabs(["📊 Current Report", "📜 History/Audit Log", "🔍 Interactive Diff Viewer"])

    with tab_current:
        if st.session_state.schema_diff_report:
            # --- Drift Summary Section - Custom Metric Boxes ---
            st.markdown("<h3><i class='fas fa-chart-bar'></i> Drift Summary Overview</h3>", unsafe_allow_html=True)
            st.info("Here's a quick overview of the structural changes detected between your schema versions. Understanding these key metrics helps you grasp the scope of schema evolution at a glance. ✨")

            metrics = st.session_state.diff_summary_metrics
            
            # Helper function to render a custom styled metric card HTML
            def get_metric_card_html(label, value, icon, card_type="info", delta=None):
                delta_html = ""
                if delta is not None:
                    delta_class = ""
                    if delta > 0:
                        delta_class = "delta-positive"
                    elif delta < 0:
                        delta_class = "delta-negative"
                    else: # delta == 0
                        delta_class = "delta-neutral" 

                    display_delta_value = str(abs(delta)) # Always display absolute value for delta
                    if delta > 0:
                        display_delta_value = f"+{display_delta_value}" 
                    elif delta < 0:
                        display_delta_value = f"-{display_delta_value}"
                    
                    # Ensure 0 value is displayed as "0" to avoid "-0"
                    if delta == 0:
                        display_delta_value = "0"

                    delta_html = f'<div class="custom-metric-delta {delta_class}">{display_delta_value}</div>'

                # Using our defined custom classes
                return f"""
                    <div class="custom-metric-card custom-metric-card-{card_type}">
                        <div class="custom-metric-content">
                            <div class="custom-metric-value">{value}</div>
                            <div class="custom-metric-label"><i class="{icon}"></i> {label}</div>
                        </div>
                        {delta_html}
                    </div>
                """

            # Container for the grid of metric cards
            st.markdown('<div class="metrics-grid-container">', unsafe_allow_html=True)
            
            # Row 1: Overall Table Counts
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(get_metric_card_html("OLD TABLES", metrics.get("total_tables_old", 0), "fas fa-database", card_type="info"), unsafe_allow_html=True)
            with col2:
                st.markdown(get_metric_card_html("NEW TABLES", metrics.get("total_tables_new", 0), "fas fa-leaf", card_type="info"), unsafe_allow_html=True)
            with col3:
                st.markdown(get_metric_card_html("MODIFIED TABLES", metrics.get("modified_table_count", 0), "fas fa-sync-alt", card_type="modified"), unsafe_allow_html=True)

            # Row 2: Table Changes (Added/Deleted)
            col4, col5, col6 = st.columns(3)
            with col4:
                st.markdown(get_metric_card_html("TABLES ADDED", metrics.get("added_table_count", 0), "fas fa-plus-square", 
                                          card_type="added", delta=metrics.get("added_table_count", 0)), unsafe_allow_html=True)
            with col5:
                st.markdown(get_metric_card_html("TABLES DELETED", metrics.get("deleted_table_count", 0), "fas fa-minus-square", 
                                          card_type="deleted", delta=-metrics.get("deleted_table_count", 0)), unsafe_allow_html=True)
            with col6:
                st.markdown(get_metric_card_html("COLUMNS ADDED", metrics.get("added_column_count", 0), "fas fa-plus-circle", 
                                          card_type="added", delta=metrics.get("added_column_count", 0)), unsafe_allow_html=True)
            
            # Row 3: Remaining Column Changes (including new Renamed Columns)
            col7, col8, col9 = st.columns(3) # Added a third column for renamed
            with col7:
                st.markdown(get_metric_card_html("COLUMNS DELETED", metrics.get("deleted_column_count", 0), "fas fa-times-circle", 
                                          card_type="deleted", delta=-metrics.get("deleted_column_count", 0)), unsafe_allow_html=True)
            with col8:
                st.markdown(get_metric_card_html("COLUMNS MODIFIED", metrics.get("modified_column_count", 0), "fas fa-pencil-alt", card_type="modified"), unsafe_allow_html=True)
            with col9: # New metric for renamed columns
                st.markdown(get_metric_card_html("COLUMNS RENAMED", metrics.get("renamed_column_count", 0), "fas fa-exchange-alt", 
                                          card_type="modified", delta=metrics.get("renamed_column_count", 0)), unsafe_allow_html=True)


            st.markdown('</div>', unsafe_allow_html=True) # Close the metrics-grid-container div


            st.markdown("---") # Separator between summary and AI report

            # --- AI-Generated Report ---
            st.markdown("<h3><i class='fas fa-robot'></i> Detailed AI Analysis</h3>", unsafe_allow_html=True)
            st.markdown(st.session_state.schema_diff_report)
            st.markdown("<p style='text-align: right; font-size: 0.8em; color: var(--text-medium);'>Powered by Google Gemini API. Interpret results as AI-generated suggestions.</p>", unsafe_allow_html=True)

            # --- New: Impact-Aware Risk Scoring ---
            st.markdown("---")
            st.markdown("<h3><i class='fas fa-exclamation-triangle'></i> Impact-Aware Risk Score</h3>", unsafe_allow_html=True)
            # Ensure schema_diff_details is available for risk scoring
            schema_diff_details = st.session_state.get("schema_diff_details", compare_schemas(
                st.session_state.get("parsed_old_schema", {}),
                st.session_state.get("parsed_new_schema", {})
            ))
            risk_score_output = get_risk_score(schema_diff_details)
            st.markdown(risk_score_output)


            # --- New: Automated Regression Test Suggestions ---
            st.markdown("---")
            st.markdown("<h3><i class='fas fa-vial'></i> Automated Regression Test Suggestions</h3>", unsafe_allow_html=True)
            test_suggestions_output = get_regression_test_suggestions(
                schema_diff_details,
                st.session_state.get("parsed_old_schema", {}),
                st.session_state.get("parsed_new_schema", {})
            )
            st.markdown(test_suggestions_output)


            st.markdown("---")
            st.markdown("<h3><i class='fas fa-download'></i> Download Report</h3>", unsafe_allow_html=True)
            
            # Download buttons row for better layout
            dl_col1, dl_col2, dl_col3 = st.columns(3) # Reduced to 3 columns

            with dl_col1: # Markdown (already existing)
                st.download_button(
                    label="⬇️ Download Markdown",
                    data=st.session_state.schema_diff_report.encode('utf-8'),
                    file_name="schema_drift_report.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="download_report_md_btn"
                )

            with dl_col2: # JSON (already existing)
                try:
                    # Re-calculate schema_diff details for raw download to ensure it's fresh
                    current_schema_diff_for_download = compare_schemas(
                        st.session_state.get("parsed_old_schema", {}),
                        st.session_state.get("parsed_new_schema", {})
                    )
                    raw_diff_json_content = {
                        "old_schema_parsed": st.session_state.get("parsed_old_schema", {}),
                        "new_schema_parsed": st.session_state.get("parsed_new_schema", {}),
                        "schema_diff_details": current_schema_diff_for_download
                    }
                    json_string = json.dumps(raw_diff_json_content, indent=2).encode('utf-8')
                    
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json_string,
                        file_name="schema_diff_raw.json",
                        mime="application/json",
                        use_container_width=True,
                        key="download_raw_diff_json_btn"
                    )
                except Exception as e:
                    st.error(f"Error preparing raw diff JSON for download: {e}")
                    st.info("Ensure schemas were parsed successfully to download raw diff.")

            with dl_col3: # Moved Excel to the third column now
                def generate_excel_report(summary_metrics, schema_diff_details):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Sheet 1: Summary Metrics
                        summary_df = pd.DataFrame(summary_metrics.items(), columns=['Metric', 'Value'])
                        summary_df.to_excel(writer, sheet_name='Summary Metrics', index=False)

                        # Sheet 2: Detailed Changes (Flattened)
                        all_changes = []
                        
                        # Added Tables
                        for table_name in schema_diff_details.get("added_tables", []):
                            all_changes.append({"Change Type": "Added Table", "Table": table_name, "Column": "", "Old Property": "", "New Property": ""})
                        
                        # Deleted Tables
                        for table_name in schema_diff_details.get("deleted_tables", []):
                            all_changes.append({"Change Type": "Deleted Table", "Table": table_name, "Column": "", "Old Property": "", "New Property": ""})
                        
                        # Modified Tables details
                        for table_name, t_diff in schema_diff_details.get("modified_tables", {}).items():
                            for col_name in t_diff.get("added_columns", []):
                                # Get actual type from new schema, if available
                                new_col_info = st.session_state.get("parsed_new_schema", {}).get(table_name, {}).get(col_name, {})
                                all_changes.append({
                                    "Change Type": "Added Column",
                                    "Table": table_name,
                                    "Column": col_name,
                                    "Old Property": "N/A",
                                    "New Property": f"Type: {new_col_info.get('type', 'UNKNOWN')}"
                                })
                            
                            for col_name in t_diff.get("deleted_columns", []):
                                # Get actual type from old schema, if available
                                old_col_info = st.session_state.get("parsed_old_schema", {}).get(table_name, {}).get(col_name, {})
                                all_changes.append({
                                    "Change Type": "Deleted Column",
                                    "Table": table_name,
                                    "Column": col_name,
                                    "Old Property": f"Type: {old_col_info.get('type', 'UNKNOWN')}",
                                    "New Property": "N/A"
                                })

                            for old_name, rename_info in t_diff.get("renamed_columns", {}).items():
                                all_changes.append({
                                    "Change Type": "Renamed Column",
                                    "Table": table_name,
                                    "Column": f"{old_name} -> {rename_info['new_name']}",
                                    "Old Property": f"Type: {rename_info['old_type']}",
                                    "New Property": f"Type: {rename_info['new_type']}"
                                })

                            for col_name, modified_props in t_diff.get("modified_columns", {}).items():
                                for prop_key, prop_values in modified_props.items():
                                    all_changes.append({
                                        "Change Type": "Modified Property",
                                        "Table": table_name,
                                        "Column": col_name,
                                        "Old Property": f"{prop_key}: {prop_values['old_value']}",
                                        "New Property": f"{prop_key}: {prop_values['new_value']}"
                                    })
                        
                        changes_df = pd.DataFrame(all_changes)
                        if not changes_df.empty: # Only write if there are changes
                            changes_df.to_excel(writer, sheet_name='Detailed Changes', index=False)

                    processed_data = output.getvalue()
                    return processed_data

                if st.session_state.schema_diff_report:
                    excel_bytes = generate_excel_report(
                        st.session_state.diff_summary_metrics,
                        compare_schemas(st.session_state.parsed_old_schema, st.session_state.parsed_new_schema)
                    )
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_bytes,
                        file_name="schema_drift_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="download_report_excel_btn"
                    )
                else:
                    st.markdown("<div style='height: 36px; display: flex; align-items: center; justify-content: center; color: var(--text-medium); font-size: 0.9em;'>Generate report for Excel</div>", unsafe_allow_html=True)


        else:
            st.info("Paste your schema versions above and click 'Compare Schemas & Analyze Drift' to generate a report.")

    with tab_history:
        st.markdown("<h3><i class='fas fa-history'></i> Historical Drift Reports</h3>", unsafe_allow_html=True)
        st.info("Explore past schema drift analyses. Select a report from the dropdown to view its details.")

        # Check if history directory exists and list files
        if os.path.exists(HISTORY_DIR):
            history_files = sorted([f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')], reverse=True)
            
            if history_files:
                # Create user-friendly labels for dropdown
                report_options = {f"Report from {f.replace('drift_report_', '').replace('.json', '').replace('_', ' at ').replace('-', '/')}" : f for f in history_files}
                
                selected_report_label = st.selectbox(
                    "Select a historical report:",
                    options=list(report_options.keys()),
                    key="history_report_selector"
                )

                if selected_report_label:
                    selected_filename = report_options[selected_report_label]
                    selected_filepath = os.path.join(HISTORY_DIR, selected_filename)

                    try:
                        with open(selected_filepath, "r", encoding="utf-8") as f:
                            historical_data = json.load(f)
                        
                        st.markdown("---")
                        st.markdown(f"<h4>Viewing Report from: {historical_data.get('timestamp', 'N/A')}</h4>", unsafe_allow_html=True)
                        
                        # Display Raw Schemas
                        st.subheader("Raw Schema Inputs")
                        col_old_raw, col_new_raw = st.columns(2)
                        with col_old_raw:
                            st.text_area("Old Schema (Raw)", historical_data.get("old_schema_raw", "N/A"), height=200, key=f"hist_old_raw_{selected_filename}")
                        with col_new_raw:
                            st.text_area("New Schema (Raw)", historical_data.get("new_schema_raw", "N/A"), height=200, key=f"hist_new_raw_{selected_filename}")

                        # Display Parsed Schemas (optional, in an expander)
                        with st.expander("Parsed Schemas (JSON)"):
                            col_old_parsed, col_new_parsed = st.columns(2)
                            with col_old_parsed:
                                st.json(historical_data.get("parsed_old_schema", {}))
                            with col_new_parsed:
                                st.json(historical_data.get("parsed_new_schema", {}))
                        
                        # Display Summary Metrics
                        st.subheader("Summary Metrics")
                        hist_metrics = historical_data.get("summary_metrics", {})
                        
                        # Re-use the custom metric card HTML generation for consistency
                        # Re-initialize the helper function as it's within a function scope
                        def get_metric_card_html_hist(label, value, icon, card_type="info", delta=None):
                            delta_html = ""
                            if delta is not None:
                                delta_class = ""
                                if delta > 0:
                                    delta_class = "delta-positive"
                                elif delta < 0:
                                    delta_class = "delta-negative"
                                else: # delta == 0
                                    delta_class = "delta-neutral" 

                                display_delta_value = str(abs(delta)) # Always display absolute value for delta
                                if delta > 0:
                                    display_delta_value = f"+{display_delta_value}" 
                                elif delta < 0:
                                    display_delta_value = f"-{display_delta_value}"
                                
                                # Ensure 0 value is displayed as "0" to avoid "-0"
                                if delta == 0:
                                    display_delta_value = "0"

                                delta_html = f'<div class="custom-metric-delta {delta_class}">{display_delta_value}</div>'

                            return f"""
                                <div class="custom-metric-card custom-metric-card-{card_type}">
                                    <div class="custom-metric-content">
                                        <div class="custom-metric-value">{value}</div>
                                        <div class="custom-metric-label"><i class="{icon}"></i> {label}</div>
                                    </div>
                                    {delta_html}
                                </div>
                            """

                        st.markdown('<div class="metrics-grid-container">', unsafe_allow_html=True)
                        
                        # Row 1: Overall Table Counts
                        colh1, colh2, colh3 = st.columns(3)
                        with colh1:
                            st.markdown(get_metric_card_html_hist("OLD TABLES", hist_metrics.get("total_tables_old", 0), "fas fa-database", card_type="info"), unsafe_allow_html=True)
                        with colh2:
                            st.markdown(get_metric_card_html_hist("NEW TABLES", hist_metrics.get("total_tables_new", 0), "fas fa-leaf", card_type="info"), unsafe_allow_html=True)
                        with colh3:
                            st.markdown(get_metric_card_html_hist("MODIFIED TABLES", hist_metrics.get("modified_table_count", 0), "fas fa-sync-alt", card_type="modified"), unsafe_allow_html=True)

                        # Row 2: Table Changes (Added/Deleted)
                        colh4, colh5, colh6 = st.columns(3)
                        with colh4:
                            st.markdown(get_metric_card_html_hist("TABLES ADDED", hist_metrics.get("added_table_count", 0), "fas fa-plus-square", 
                                                    card_type="added", delta=hist_metrics.get("added_table_count", 0)), unsafe_allow_html=True)
                        with colh5:
                            st.markdown(get_metric_card_html_hist("TABLES DELETED", hist_metrics.get("deleted_table_count", 0), "fas fa-minus-square", 
                                                    card_type="deleted", delta=-hist_metrics.get("deleted_table_count", 0)), unsafe_allow_html=True)
                        with colh6:
                            st.markdown(get_metric_card_html_hist("COLUMNS ADDED", hist_metrics.get("added_column_count", 0), "fas fa-plus-circle", 
                                                    card_type="added", delta=hist_metrics.get("added_column_count", 0)), unsafe_allow_html=True)
                        
                        # Row 3: Remaining Column Changes (including new Renamed Columns)
                        colh7, colh8, colh9 = st.columns(3)
                        with colh7:
                            st.markdown(get_metric_card_html_hist("COLUMNS DELETED", hist_metrics.get("deleted_column_count", 0), "fas fa-times-circle", 
                                                    card_type="deleted", delta=-hist_metrics.get("deleted_column_count", 0)), unsafe_allow_html=True)
                        with colh8:
                            st.markdown(get_metric_card_html_hist("COLUMNS MODIFIED", hist_metrics.get("modified_column_count", 0), "fas fa-pencil-alt", card_type="modified"), unsafe_allow_html=True)
                        with colh9:
                            st.markdown(get_metric_card_html_hist("COLUMNS RENAMED", hist_metrics.get("renamed_column_count", 0), "fas fa-exchange-alt", 
                                                    card_type="modified", delta=hist_metrics.get("renamed_column_count", 0)), unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)


                        # Display AI Report
                        st.subheader("AI-Generated Report")
                        st.markdown(historical_data.get("ai_report_markdown", "No AI report found for this entry."))

                        # Option to download the historical report (as Markdown or original JSON)
                        st.markdown("---")
                        st.subheader("Download Historical Report")
                        col_hist_dl_md, col_hist_dl_json = st.columns(2)
                        with col_hist_dl_md:
                            st.download_button(
                                label="⬇️ Download Markdown",
                                data=historical_data.get("ai_report_markdown", "").encode('utf-8'),
                                file_name=f"historical_report_{historical_data.get('timestamp', 'N/A')}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                        with col_hist_dl_json:
                            st.download_button(
                                label="⬇️ Download Full JSON",
                                data=json.dumps(historical_data, indent=2).encode('utf-8'),
                                file_name=f"historical_data_{historical_data.get('timestamp', 'N/A')}.json",
                                mime="application/json",
                                use_container_width=True
                            )


                    except Exception as e:
                        st.error(f"Error loading historical report: {e}")
                        st.info("The selected file might be corrupted or in an invalid format.")
            else:
                st.info("No historical reports found yet. Generate a report in the 'Current Report' tab to save it.")
        else:
            st.info(f"The history directory '{HISTORY_DIR}' does not exist yet. Generate a report to create it.")

    with tab_diff_viewer:
        st.markdown("<h3><i class='fas fa-code-compare'></i> Interactive Schema Diff Viewer</h3>", unsafe_allow_html=True)
        st.info("Visually inspect schema changes with color-coded highlighting for added, deleted, modified, and renamed elements. Expand sections to see details.")

        if st.session_state.schema_diff_report:
            # Re-fetch schema_diff_details to ensure it's up-to-date
            schema_diff_details = st.session_state.get("schema_diff_details", compare_schemas(
                st.session_state.get("parsed_old_schema", {}),
                st.session_state.get("parsed_new_schema", {})
            ))

            # Helper function to render a table row for diff
            def render_diff_row(label, old_val, new_val, diff_type, old_type="", new_type=""):
                # Determine cell classes based on diff_type and add icons
                old_cell_class = "diff-cell"
                new_cell_class = "diff-cell"
                label_class = "diff-label"
                icon_html = ""
                tooltip_text = ""

                if diff_type == "added":
                    new_cell_class += " diff-added"
                    label_class += " diff-added-label"
                    icon_html = '<i class="fas fa-plus diff-icon"></i>'
                    tooltip_text = "This element was added."
                elif diff_type == "deleted":
                    old_cell_class += " diff-deleted"
                    label_class += " diff-deleted-label"
                    icon_html = '<i class="fas fa-minus diff-icon"></i>'
                    tooltip_text = "This element was deleted."
                elif diff_type == "modified":
                    old_cell_class += " diff-modified"
                    new_cell_class += " diff-modified"
                    label_class += " diff-modified-label"
                    icon_html = '<i class="fas fa-edit diff-icon"></i>'
                    tooltip_text = "Properties of this element were modified."
                elif diff_type == "renamed":
                    old_cell_class += " diff-renamed"
                    new_cell_class += " diff-renamed"
                    label_class += " diff-renamed-label"
                    icon_html = '<i class="fas fa-exchange-alt diff-icon"></i>'
                    tooltip_text = "This element was likely renamed."


                # Construct content for cells
                old_content = old_val if old_val else "N/A"
                new_content = new_val if new_val else "N/A"

                if diff_type == "renamed":
                    # For renamed, old_val is old name, new_val is new name
                    # old_type and new_type come separately
                    return f"""
                        <tr>
                            <td class="{label_class}" title="{tooltip_text}">{icon_html} {label}</td>
                            <td class="{old_cell_class}">{old_val} ({old_type})</td>
                            <td class="{new_cell_class}">{new_val} ({new_type})</td>
                        </tr>
                    """
                elif diff_type == "modified":
                     return f"""
                        <tr>
                            <td class="{label_class}" title="{tooltip_text}">{icon_html} {label}</td>
                            <td class="{old_cell_class}">{old_val}</td>
                            <td class="{new_cell_class}">{new_val}</td>
                        </tr>
                    """
                else: # added, deleted, or unmodified
                    return f"""
                        <tr>
                            <td class="{label_class}" title="{tooltip_text}">{icon_html} {label}</td>
                            <td class="{old_cell_class}">{old_content}</td>
                            <td class="{new_cell_class}">{new_content}</td>
                        </tr>
                    """

            diff_html = ""

            # --- Table Diff Section ---
            # Use st.expander for collapsibility
            with st.expander("Table-Level Changes", expanded=True):
                diff_html_tables = ""
                diff_html_tables += "<table class='diff-table'>"
                diff_html_tables += """
                    <thead>
                        <tr>
                            <th>Change Type</th>
                            <th>Table Name (Old)</th>
                            <th>Table Name (New)</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for table_name in schema_diff_details["added_tables"]:
                    diff_html_tables += render_diff_row("Added", "", table_name, "added")
                for table_name in schema_diff_details["deleted_tables"]:
                    diff_html_tables += render_diff_row("Deleted", table_name, "", "deleted")
                
                # Placeholder for Modified Tables (will be detailed below)
                if schema_diff_details["modified_tables"]:
                    for table_name in schema_diff_details["modified_tables"]:
                        diff_html_tables += render_diff_row("Modified", table_name, table_name, "modified")
                diff_html_tables += "</tbody></table>"
                
                if not schema_diff_details["added_tables"] and \
                   not schema_diff_details["deleted_tables"] and \
                   not schema_diff_details["modified_tables"]:
                    diff_html_tables = "<p class='placeholder-text'>No table-level changes detected.</p>"

                st.markdown(f"<div class='diff-viewer-container'>{diff_html_tables}</div>", unsafe_allow_html=True)
            
            # --- Detailed Column Diff for Modified Tables ---
            if schema_diff_details["modified_tables"]:
                with st.expander("Detailed Column Changes in Modified Tables", expanded=True):
                    for table_name, table_diff in schema_diff_details["modified_tables"].items():
                        st.markdown(f"<h5>Table: <code>{table_name}</code></h5>", unsafe_allow_html=True)
                        diff_html_columns = "<table class='diff-table'>"
                        diff_html_columns += """
                            <thead>
                                <tr>
                                    <th>Column Change</th>
                                    <th>Old Value/Property</th>
                                    <th>New Value/Property</th>
                                </tr>
                            </thead>
                            <tbody>
                        """
                        # Added Columns
                        for col_name in table_diff["added_columns"]:
                            new_col_props = st.session_state.parsed_new_schema[table_name][col_name]
                            diff_html_columns += render_diff_row(f"Added: {col_name}", "", f"Type: {new_col_props['type']}", "added")
                        
                        # Deleted Columns
                        for col_name in table_diff["deleted_columns"]:
                            old_col_props = st.session_state.parsed_old_schema[table_name][col_name]
                            diff_html_columns += render_diff_row(f"Deleted: {col_name}", f"Type: {old_col_props['type']}", "", "deleted")

                        # Renamed Columns
                        for old_name, rename_info in table_diff["renamed_columns"].items():
                            diff_html_columns += render_diff_row(
                                "Renamed",
                                old_name,
                                rename_info["new_name"],
                                "renamed",
                                old_type=rename_info["old_type"],
                                new_type=rename_info["new_type"]
                            )
                        
                        # Modified Columns
                        for col_name, mod_props in table_diff["modified_columns"].items():
                            for prop_key, prop_values in mod_props.items():
                                diff_html_columns += render_diff_row(
                                    f"Modified: {col_name} ({prop_key})",
                                    str(prop_values["old_value"]),
                                    str(prop_values["new_value"]),
                                    "modified"
                                )
                        diff_html_columns += "</tbody></table>"
                        st.markdown(diff_html_columns, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True) # Add space between tables

            else:
                st.info("No detailed column changes in modified tables detected.")

            st.markdown("---") # Separator below diff viewer

            # Download Diff View Content (as HTML for now)
            st.download_button(
                label="⬇️ Download Diff View (HTML)",
                data=f"<div class='diff-viewer-container'>Generated interactive diff will appear here.</div>".encode('utf-8'), # Placeholder data for download
                file_name="schema_diff_view.html",
                mime="text/html",
                use_container_width=True,
                key="download_diff_html_btn"
            )

        else:
            st.info("Generate a schema drift report in the 'Current Report' tab to view the interactive diff.")

