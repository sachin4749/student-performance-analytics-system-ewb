# 🎓 Student Performance Analytics System (EWB Internship Project)

> **A professional, browser-accessible BTech Student Performance Analytics web application built for institutional academic evaluation, department-wise student tracking, and automated PDF reporting.**

---

## 🌟 Executive Summary

The **Student Performance Analytics System** is a robust end-to-end academic dashboard engineered to replace manual CLI tracking with a modern, interactive web interface. Built using **Python**, **Streamlit**, **Pandas**, **NumPy**, **Plotly**, and **ReportLab**, this platform allows educators and evaluators to upload, clean, analyze, and visualize student academic performance across multiple engineering departments instantly.

---

## 🚀 Core Capabilities & Features

### 1. 📊 Interactive Overview Dashboard
- **Real-Time Class KPIs:** Instantly computes Total Students, Class Average Score, Highest Score, Lowest Score, and Overall Pass/Fail percentages.
- **Visual Analytics:** Interactive Plotly charts for Grade Distribution (`A+` to `F`) and Pass/Fail proportions.
- **Department Comparisons:** Comparative bar charts illustrating average scores across various engineering branches.

### 2. 📂 Department Student Directory & ID Lookup
- **Branch-Specific Filtering:** Browse students filtered by specific departments (`CSE`, `ECE`, `IT`, `MECH`, `AI/ML`).
- **Complete Student Records:** View exact **Student IDs**, full names, individual subject marks (`Python`, `SQL`, `C++`, `OOP`, `IOT`), attendance percentages, final averages, assigned grades, and pass/fail statuses without any guesswork.

### 3. 📄 Automated Departmental PDF Report Generation
- **On-the-Fly PDF Export:** Powered by **ReportLab**, users can generate and download official, beautifully formatted **Department PDF Reports** with a single click.
- **Structured Layout:** Each generated PDF includes clean tabular summaries, academic metrics, and student performance statuses tailored for official documentation.

### 4. 📈 Subject-Wise Academic Performance
- Evaluates average, highest, lowest, and median scores across core technical subjects.
- Features comparative bar charts and distribution box plots to identify stronger and weaker curriculum areas.

### 5. 🛡️ Robust Data Cleaning & Imputation Engine
- **Automated Validation:** Enforces strict schema checks for required columns (`Student ID`, `Name`, `Department`, `Python`, `SQL`, `C++`, `OOP`, `IOT`, `Attendance`).
- **Smart Imputation:** Automatically handles missing values by imputing subject marks with the **median** and attendance with the **mean**.
- **Range Enforcement:** Bounds checking (0–100 scale) with detailed data-quality logs explaining any adjustments.

### 6. 🔍 Student Search & Multi-Criteria Filtering
- Case-insensitive partial name and Student ID search engine.
- Multi-parameter filtering by department, grade letter, and pass/fail status.

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
├── app.py                # Main Streamlit web application & multi-page navigation router
├── analytics.py          # Core data cleaning, calculation rules, KPI metrics, and ReportLab PDF engine
├── requirements.txt      # Runtime python dependencies
├── README.md             # Project documentation and deployment manual
├── .gitignore            # Exclusions for virtual environments and caches
└── sample_data/
    └── students.csv      # Built-in 50-student sample dataset for immediate testing
