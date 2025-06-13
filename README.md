

# 🧠 Intelligent Schema Drift & Impact Analyzer

## 📌 Overview

The **Intelligent Schema Drift & Impact Analyzer** is a **Streamlit-based web application** designed to help data professionals understand, analyze, and manage changes in their database schemas. It leverages **Google's Gemini AI** 🤖 to provide in-depth analysis of schema drift, assess potential impacts on downstream systems, and suggest automated regression tests.

This tool simplifies the often-complex process of identifying and mitigating risks associated with schema evolution in data environments. 🚀

---

## ✨ Features

* 🔍 **Schema Comparison**
  Compare two versions (old and new) of your database schemas — supports both **SQL CREATE TABLE statements** and a custom **JSON schema format**.

* 🧠 **AI-Powered Drift Analysis**
  Uses **Google Gemini AI** to generate a comprehensive, human-readable report detailing schema changes, potential impacts, and remediation steps.

* 📊 **Drift Summary Metrics**
  Get a quick overview via custom metric cards — added/deleted tables, renamed/modified columns, and more.

* 🚨 **Impact-Aware Risk Scoring**
  AI-generated risk score prioritizing attention to **high-impact alterations**.

* 🧪 **Automated Regression Test Suggestions**
  AI-powered test recommendations tailored to the schema changes for better QA.

* 🧾 **Interactive Schema Diff Viewer**
  Collapsible and color-coded HTML tables to clearly inspect additions, deletions, modifications, and renames.

* 🕓 **Historical Reports**
  View/download **past schema drift analysis reports** for auditing and version tracking.

* 📥 **Multi-Format Export**
  Export the report as **Markdown**, **JSON**, or **Excel**.

---

## ⚙️ How to Use

### 1️⃣ Setup

**🔧 Prerequisites:**

* Python 3.8+
* pip

**📦 Installation Steps:**

```bash
# Clone the repository
git clone <your-repo-url>

# Navigate into the project
cd your-project-directory

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

📝 *Ensure `requirements.txt` includes:*

```
streamlit
google-generativeai
pandas
fpdf2
requests
openpyxl
```

---

### 2️⃣ Configure Gemini API

* Get your **API key** from [Google AI Studio](https://makersuite.google.com/).
* Create a `.env` file in your root directory:

```env
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

---

### 3️⃣ Run the App

```bash
streamlit run main.py
```

This opens the app in your browser at [http://localhost:8501](http://localhost:8501) 🌐

---

### 4️⃣ Analyzing Schema Drift

* **Input Schemas:**
  Paste your **Old Schema** and **New Schema** in the app UI. Supported formats:

  * SQL `CREATE TABLE` statements ✅
  * JSON schema arrays ✅

* **Click**: 🚀 *"Compare Schemas & Analyze Drift"*

* **Output Includes:**

  * 📋 Executive summary
  * ➕➖ Modified/Added/Deleted columns/tables
  * 🧠 Impact & risk report
  * 🛠 Remediation suggestions
  * 📜 AI-powered test case ideas
  * 📊 Interactive diff table

* **Download Options:**

  * 📄 Markdown
  * 🧾 JSON
  * 📊 Excel

---

## 🛠 Supported Schema Input Formats

### 📌 A. SQL `CREATE TABLE` Statements

```sql
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    registration_date DATE
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
);
```

---

### 📌 B. JSON Schema Array

```json
[
  {
    "table_name": "Products",
    "columns": [
      {"name": "product_id", "type": "INT", "is_pk": true},
      {"name": "product_name", "type": "VARCHAR(255)"},
      {"name": "price", "type": "DECIMAL(10,2)"}
    ]
  },
  {
    "table_name": "Sales",
    "columns": [
      {"name": "sale_id", "type": "INT", "is_pk": true},
      {"name": "product_id", "type": "INT"},
      {"name": "sale_date", "type": "DATE"}
    ]
  }
]
```

---

## 🤖 AI Capabilities (Powered by Gemini)

* 🧠 **Interpret Schema Differences** into human-friendly insights
* ⚠️ **Assess Impact** on ETL jobs, dashboards, apps
* 🛠 **Suggest Remediations** to fix or adapt to changes
* ✅ **Recommend Regression Tests** based on changes

---

## 🗂️ Project Structure

```plaintext
main.py                  # Streamlit entry point
schema_utils.py          # Schema parsing & comparison logic
analysis_enhancements.py # AI risk score + test suggestion logic
additional_features.py   # Report rendering + history
gemini_utils.py          # Google Gemini API interactions
.env                     # Stores your API key (excluded from Git)
requirements.txt         # Python dependencies
schema_drift_history/    # Stores previous reports
```

---

## 🚀 Future Enhancements

* 🧩 Advanced SQL parsing (supporting more dialects like PostgreSQL, Oracle)
* 🔄 Git integration to auto-fetch schema diffs from repo commits
* 📡 Metadata integration (e.g., DataHub, Amundsen) for richer impact analysis
* 🧍‍♂️ Multi-user support with authentication & access control
* 🧭 Side-by-side schema code diff viewer (IDE-style)
* 📦 Export reports to PDF or integrate with Slack/Teams

---
