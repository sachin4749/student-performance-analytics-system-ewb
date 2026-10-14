# 🎓 Student Performance Analytics System (EWB Virtual Internship Project)

> **A professional, full-stack, multi-semester BTech Student Performance Analytics web application built using Python, Streamlit, Pandas, NumPy, Plotly, and ReportLab. Designed for institutional grade evaluation, branch-specific curriculum tracking, attendance monitoring, and instant automated PDF report generation.**

---

## 📋 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Core Capabilities & Features](#-core-capabilities--features)
3. [System Architecture & Data Schema](#-system-architecture--data-schema)
4. [Step-by-Step User Guide (How to Use)](#-step-by-step-user-guide-how-to-use-the-app)
5. [Technology Stack](#️-technology-stack)
6. [Project File Structure](#-project-file-structure)
7. [Local Installation & Setup Guide](#️-step-by-step-local-installation-instructions)
8. [Cloud Deployment Guide (Streamlit Community Cloud)](#-step-by-step-deployment-guide-streamlit-community-cloud)
9. [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🌟 Executive Summary

The **Student Performance Analytics System** is an end-to-end institutional management dashboard built during the EWB Virtual Internship. It transitions traditional manual command-line grading and attendance checking into a modern, interactive, web-accessible dashboard. Spanning across **8 Semesters** and 5 core engineering departments (**CSE, ECE, IT, MECH, AI/ML**), this system offers robust data cleaning, student identification lookups (using IDs like `S123`, `S254`, `S345`, `S564`), multi-criteria searching, and on-the-fly PDF generation powered by ReportLab.

---

## 🚀 Core Capabilities & Features

### 1. 🏠 Interactive Overview Dashboard
- **Institutional KPIs:** Instantly computes Total Student Records, Class Average Scores, Highest Achieved Marks, Lowest Scores, and overall Pass/Fail ratios.
- **Visual Analytics:** Interactive Plotly charts displaying Grade Distributions (`A+`, `A`, `B+`, `B`, `C`, `F`) and Pass vs. Fail proportions.

### 2. 📚 Multi-Semester & Department Curriculum Mapping
- **Branch-Specific Subjects:** Automatically maps subject codes (`Subject 1` to `Subject 5`) to real-world curriculum names based on the department and semester chosen (e.g., *Python & Data Structures* for CSE Sem 2, *Machine Learning & Deep Learning* for AI/ML Sem 5, *Thermodynamics* for MECH Sem 3).

### 3. 📂 Semester Student Directory & PDF Report Generator
- **Detailed Rosters:** View branch and semester-specific student directories complete with exact Student IDs (e.g., `S123`, `S254`, `S345`, `S564`), full names, subject marks, attendance percentages, and calculated grades.
- **Automated PDF Export:** Click the **"📥 Download Department PDF Report"** button to export professional, beautifully formatted PDF reports instantly using ReportLab.

### 4. 🏆 Advanced Top Performers & Multi-Criteria Search
- **Top 5 Filtering:** Dynamically filter and view top-performing students based on Department and Semester selections.
- **Smart Search Engine:** Case-insensitive partial name and Student ID search functionality (testable using sample IDs like `S123`, `S345`, etc.).

### 5. 🛡️ Robust Data Validation & Imputation Engine
- **Schema Validation:** Automatically checks uploaded CSV files for required columns (`Student ID`, `Name`, `Department`, `Semester`, `Subject 1`, `Subject 2`, `Subject 3`, `Subject 4`, `Subject 5`, `Attendance`).
- **Smart Imputation:** Automatically handles missing values by imputing subject marks with the **median** and attendance with the **mean**, while clipping out-of-range values (0–100 scale).

---

## 📊 System Architecture & Data Schema

The application follows a modular separation of concerns:
- `app.py`: Handles the Streamlit user interface, sidebar state management, multi-page routing, and interactive Plotly charts.
- `analytics.py`: Manages the backend data ingestion, validation rules, imputation logic, grading algorithms, and ReportLab PDF layout engine.

### Sample Data Schema Table:
| Column Name | Data Type | Description / Example Values |
| :--- | :--- | :--- |
| `Student ID` | String | Unique identifier (e.g., `S123`, `S254`, `S345`, `S564`) |
| `Name` | String | Student Full Name (e.g., `Aarav Sharma`) |
| `Department` | String | Engineering Branch (`CSE`, `ECE`, `IT`, `MECH`, `AI/ML`) |
| `Semester` | String | Academic Semester (`Sem 1` through `Sem 8`) |
| `Subject 1-5` | Integer | Numeric marks scored out of 100 |
| `Attendance` | Float | Percentage of student attendance (0.0 to 100.0) |

---

## 📖 Step-by-Step User Guide (How to Use the App)

Follow these simple instructions to operate the dashboard seamlessly:

- **Step 1: Data Ingestion**
  - Launch the app and use the sidebar radio buttons to either **"Load Multi-Semester Sample Dataset"** (pre-loaded with records spanning across Semesters 1–8 with student IDs like `S123`, `S254`, `S345`, `S564`) or **Upload your own custom `.csv` file**.
- **Step 2: Review Overview Metrics**
  - Navigate to **"🏠 Overview Dashboard"** to examine high-level institutional pass rates, grade distributions, and performance distributions.
- **Step 3: Analyze Subject Performance**
  - Go to **"📊 Subject-Wise Performance"**, choose your target Department and Semester, and analyze relative subject averages, highest marks, lowest marks, and box-plot distributions.
- **Step 4: Check Directory & Download PDFs**
  - Access **"📂 Semester Student Directory & PDF"**, filter by branch and semester to verify student rosters and IDs (`S123`, `S564`), and click **"📥 Download PDF Report"** to save the official document.
- **Step 5: Search & Export**
  - Use **"🔍 Student Search"** to query individual student metrics using IDs like `S123` or names, or visit **"📋 Records Explorer & Export"** to download the clean processed data as a CSV.

---

## 🛠️ Technology Stack

- **Core Language:** Python 3.10+
- **Web Interface Framework:** Streamlit (`>=1.32.0`)
- **Data Manipulation & Analysis:** Pandas (`>=2.0.0`), NumPy (`>=1.24.0`)
- **Data Visualization:** Plotly Express (`>=5.18.0`)
- **PDF Generation Engine:** ReportLab (`>=4.0.0`)
- **Version Control & Hosting:** Git, GitHub, Streamlit Community Cloud

---

## 📂 Project File Structure

```text
student-performance-analytics-system-ewb/
├── app.py                # Main Streamlit web application & router
├── analytics.py          # Data cleaning, statistics, & ReportLab PDF generator
├── requirements.txt      # Python runtime dependencies
├── README.md             # Comprehensive project documentation
├── .gitignore            # Git exclusion rules for virtual environments
└── sample_data/
    └── students.csv      # Built-in multi-semester dataset (with IDs like S123, S254, S345, S564)
