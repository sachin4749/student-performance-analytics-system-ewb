# 🎓 Student Performance Analytics System (EWB Internship Project)

> **A comprehensive, multi-semester BTech Student Performance Analytics web application built with Python, Streamlit, Pandas, NumPy, Plotly, and ReportLab for institutional academic tracking, department-wise evaluation, and automated PDF reporting.**

---

## 🌟 Executive Summary

The **Student Performance Analytics System** is an advanced academic dashboard engineered to streamline institutional grade evaluation, attendance tracking, and curriculum performance analysis. Spanning across **8 Semesters** and multiple engineering branches (**CSE, ECE, IT, MECH, AI/ML**), this system provides deep insights, robust data cleaning, student directory lookups, and instant departmental PDF report generation.

---

## 🚀 Core Capabilities & Features

### 1. 🏠 Interactive Overview Dashboard
- Real-time institutional KPIs: Total Records, Class Average Score, Highest Score, Lowest Score, and Overall Pass/Fail percentages.
- Visual breakdown of Grade Distributions (`A+` to `F`) and Pass vs. Fail proportions.

### 2. 📚 Multi-Semester & Department Curriculum Mapping
- Dynamic subject mapping for **Semesters 1 through 8** across all engineering branches (e.g., Python, Data Structures, Machine Learning, Thermodynamics, VLSI Design, etc.).
- Filter and analyze curriculum performance specifically by branch and semester.

### 3. 📂 Semester Student Directory & PDF Report Generator
- Branch and semester-wise student lookups displaying exact Student IDs, full names, subject marks, attendance, and pass/fail statuses.
- One-click **Department & Semester PDF Report Generation** powered by **ReportLab** for official documentation.

### 4. 🏆 Advanced Top Performers & Search
- Filter top 5 performing students dynamically by Department and Semester.
- Case-insensitive partial name and Student ID search engine.

### 5. 🛡️ Robust Data Validation & Imputation Engine
- Strict schema verification for required columns (`Student ID`, `Name`, `Department`, `Semester`, `Subject 1-5`, `Attendance`).
- Automated median imputation for missing subject marks and mean imputation for attendance, with bounds checking (0–100 scale).

---

## 📖 Step-by-Step User Guide (How to Use the App)

Follow these simple steps to navigate and utilize the dashboard effectively:

- **Step 1: Load Data**
  - Upon opening the web application, use the sidebar to either **"Load Multi-Semester Sample Dataset"** (pre-loaded with 600 records across 8 semesters and 5 branches) or **Upload your own custom `.csv` file** matching the required schema.
- **Step 2: Explore Overview KPIs**
  - Navigate to **"🏠 Overview Dashboard"** to inspect institutional pass rates, class averages, and grade distributions at a glance.
- **Step 3: Analyze Subject Performance**
  - Go to **"📊 Subject-Wise Performance"**, select your desired Department and Semester, and view relative subject statistics, comparative bar charts, and score spreads (box plots).
- **Step 4: Check Student Directory & Generate PDFs**
  - Click on **"📂 Semester Student Directory & PDF"**, choose the branch and semester to view complete student records and their exact Student IDs. Click the **"📥 Download PDF Report"** button to export an official evaluation report instantly.
- **Step 5: Search & Export Records**
  - Use **"🔍 Student Search"** to look up individual student performance by name or ID, or visit **"📋 Records Explorer & Export"** to download complete processed datasets as CSV files.

---

## 🛠️ Technology Stack

- **Core Language:** Python 3.10+
- **Web Framework:** Streamlit
- **Data Processing & Analytics:** Pandas, NumPy
- **Data Visualization:** Plotly Express & Graph Objects
- **PDF Report Generation:** ReportLab
- **Version Control & Hosting:** GitHub, Streamlit Community Cloud

---

## 📂 Project Architecture

```text
student-performance-analytics-system-ewb/
├── app.py                # Main Streamlit multi-semester web application
├── analytics.py          # Data processing engine, curriculum mapping & ReportLab PDF generator
├── requirements.txt      # Project runtime dependencies
├── README.md             # Project documentation and deployment guide
├── .gitignore            # Exclusions for virtual environments and cache
└── sample_data/
    └── students.csv      # Built-in multi-semester sample dataset (Sem 1 to 8)
