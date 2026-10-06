# Student Performance Analytics System

## 1. Project Title & Student Details
* **Project Title:** Student Performance Analytics System (BTech Curriculum Edition)
* **Technology Stack:** Python 3.x, NumPy, Pandas
* **Target Audience:** Engineering Students & Academic Evaluators

## 2. Objective & Problem Statement
Academic institutions manage diverse student records across core technical disciplines (Python, SQL, C++, OOP, IoT). Manually calculating aggregate totals, averages, assigning standardized grading scales, and filtering department-wise statistics is cumbersome. 
This system automates end-to-end data ingestion, missing-value imputation, vectorized NumPy numerical calculations, and provides an interactive terminal dashboard for comprehensive performance evaluation.

## 3. Technologies Used
* **Python:** Core procedural and object-oriented logic, functions, loops, conditions, and user interaction loops.
* **Pandas:** High-performance data structure handling, CSV reading, grouping, and filtering operations.
* **NumPy:** Fast vectorized array operations for computing statistical summaries and metrics.

## 4. Dataset Description (`students.csv`)
* **Records:** 25 comprehensive student records spanning multiple BTech departments.
* **Fields Included:** `Student ID`, `Name`, `Department`, `Python`, `SQL`, `C++`, `OOP`, `IOT`, and `Attendance`.
* **Data Integrity:** Designed with intentional edge cases (missing marks and attendance data) to rigorously test imputation routines and error-handling functions.

## 5. Step-by-Step Implementation Explanation
1. **Data Loading & Cleaning (`load_and_clean_data`):** Validates file existence, coerces data types, and imputes missing subject marks using column medians and attendance using means.
2. **Vectorized Computation (`compute_analytics`):** Leverages NumPy arrays to compute total scores, percentages, and evaluates pass/fail criteria and grade assignments.
3. **Interactive Dashboard (`display_dashboard`):** Provides a clean, menu-driven CLI interface allowing users to view overall summaries, subject breakdowns, department statistics, top performers, and student searches.
4. **Data Export (`processed_student_report.csv`):** Enables seamless export of calculated results back to CSV format.
