# main.py
import streamlit as st
import json # Only for initial session state defaults
from styling import apply_custom_css
from features import render_input_section, generate_drift_report
from additional_features import render_output_section

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Intelligent Schema Drift & Impact Analyzer",
    page_icon="🔍", # Using an icon for the browser tab
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Apply Custom CSS ---
apply_custom_css()

# --- Session State Initialization ---
# Initialize session states that are shared across modules
if 'old_schema_input' not in st.session_state:
    st.session_state.old_schema_input = """
-- Version 1 of the Users table schema
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Version 1 of the Products table schema
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
);
"""

if 'new_schema_input' not in st.session_state:
    st.session_state.new_schema_input = """
-- Version 2 of the Users table schema
CREATE TABLE Users (
    user_id UUID PRIMARY KEY, -- Data type changed, new UUID type
    full_name VARCHAR(100) NOT NULL, -- Renamed from username, length increased
    email_address VARCHAR(120) UNIQUE, -- Renamed from email, length increased
    signup_date DATE, -- Renamed from created_at, data type changed
    is_active BOOLEAN DEFAULT TRUE -- New column added
);

-- Version 2 of the Products table schema (no changes in this version)
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    base_price DECIMAL(12, 4) NOT NULL, -- Renamed from price, precision increased
    description TEXT -- New column added
);

-- New table added in version 2
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id UUID,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    shipping_address VARCHAR(255), -- New column
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

if 'schema_diff_report' not in st.session_state:
    st.session_state.schema_diff_report = "" # Stores the AI-generated diff report
if 'parsed_old_schema' not in st.session_state:
    st.session_state.parsed_old_schema = {} # Stores the parsed old schema dict
if 'parsed_new_schema' not in st.session_state:
    st.session_state.parsed_new_schema = {} # Stores the parsed new schema dict
if 'diff_summary_metrics' not in st.session_state:
    st.session_state.diff_summary_metrics = {} # Stores summary counts for metrics


# --- Main Application Flow ---

# Hero Section - New vibrant entrance
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title"><i class="fas fa-magic"></i> AI-Powered Schema Drift Analyzer</h1>
        <p class="hero-subtitle">Instantly compare database schema versions & predict impact on your data pipelines.</p>
        <p class="hero-tagline"><strong>Effortless data governance, intelligent insights.</strong></p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---") # Visual separator


# Render Input Section (from features.py)
render_input_section()

st.markdown("---") # Visual separator

# Render Output Section (from additional_features.py)
render_output_section()

st.markdown("---") # Visual separator
st.caption("Intelligent Schema Drift & Impact Analyzer | Built with Streamlit & Google Gemini API")
