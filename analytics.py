import pandas as pd
import numpy as np

REQUIRED_COLUMNS = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance']
SUBJECTS = ['Python', 'SQL', 'C++', 'OOP', 'IOT']

def validate_columns(df):
    """Check if all required columns are present in the dataframe."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing

def clean_and_process_data(df):
    """
    Cleans the student dataset, handles missing values, validates ranges,
    calculates totals, averages, grades, and pass/fail statuses.
    Returns:
        processed_df: pd.DataFrame with all calculated fields
        report: dict containing data quality metrics and logs
    """
    # Create a copy to avoid modifying original
    df = df.copy()
    
    report = {
        "missing_columns": [],
        "imputation_log": [],
        "invalid_ranges_log": [],
        "records_processed": len(df),
        "data_quality_notes": []
    }
    
    # 1. Validate required columns
    missing_cols = validate_columns(df)
    if missing_cols:
        report["missing_columns"] = missing_cols
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")

    # 2. Convert subject marks and attendance to numeric, coercing errors
    for col in SUBJECTS + ['Attendance']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Handle missing values & imputation
    imputation_log = []
    
    # Subject marks imputation (Median)
    for subj in SUBJECTS:
        if subj in df.columns:
            missing_count = df[subj].isnull().sum()
            if missing_count > 0:
                if df[subj].dropna().empty:
                    # All values are missing
                    df[subj] = df[subj].fillna(0)
                    imputation_log.append(f"Subject '{subj}' has no valid numeric values; imputed with 0.")
                else:
                    median_val = df[subj].median()
                    df[subj] = df[subj].fillna(median_val)
                    imputation_log.append(f"Imputed {missing_count} missing value(s) in '{subj}' with median ({median_val:.2f}).")

    # Attendance imputation (Mean)
    if 'Attendance' in df.columns:
        att_missing = df['Attendance'].isnull().sum()
        if att_missing > 0:
            if df['Attendance'].dropna().empty:
                df['Attendance'] = df['Attendance'].fillna(0.0)
                imputation_log.append("Attendance column has no valid numeric values; imputed with 0.0%.")
            else:
                mean_val = df['Attendance'].mean()
                df['Attendance'] = df['Attendance'].fillna(mean_val)
                imputation_log.append(f"Imputed {att_missing} missing value(s) in 'Attendance' with mean ({mean_val:.2f}%).")

    report["imputation_log"] = imputation_log

    # 4. Range Validation (0-100 for marks and attendance)
    invalid_ranges_log = []
    for subj in SUBJECTS:
        if subj in df.columns:
            invalid_mask = (df[subj] < 0) | (df[subj] > 100)
            invalid_count = invalid_mask.sum()
            if invalid_count > 0:
                invalid_ranges_log.append(f"Found {invalid_count} out-of-range value(s) in '{subj}' (outside 0-100). Clipped to valid bounds.")
                df[subj] = df[subj].clip(0, 100)

    if 'Attendance' in df.columns:
        att_invalid = (df['Attendance'] < 0) | (df['Attendance'] > 100)
        att_inv_count = att_invalid.sum()
        if att_inv_count > 0:
            invalid_ranges_log.append(f"Found {att_inv_count} out-of-range value(s) in 'Attendance' (outside 0-100%). Clipped to valid bounds.")
            df['Attendance'] = df['Attendance'].clip(0, 100)

    report["invalid_ranges_log"] = invalid_ranges_log

    # 5. Handle missing Student ID, Name, Department
    for meta_col in ['Student ID', 'Name', 'Department']:
        if meta_col in df.columns:
            df[meta_col] = df[meta_col].fillna("Unknown").astype(str).str.strip()
            df[meta_col] = df[meta_col].replace('', 'Unknown')

    # 6. Calculations: Total Marks, Max Possible, Average Marks
    df['Total Marks'] = df[SUBJECTS].sum(axis=1)
    df['Max Possible'] = len(SUBJECTS) * 100
    df['Average Marks'] = df['Total Marks'] / len(SUBJECTS)

    # 7. Grade Assignment
    def assign_grade(avg):
        if avg >= 85:
            return 'A+'
        elif avg >= 75:
            return 'A'
        elif avg >= 65:
            return 'B+'
        elif avg >= 55:
            return 'B'
        elif avg >= 45:
            return 'C'
        else:
            return 'F'

    df['Grade'] = df['Average Marks'].apply(assign_grade)

    # 8. Pass/Fail Status (Average >= 45 AND Attendance >= 60)
    def determine_status(row):
        if row['Average Marks'] >= 45 and row['Attendance'] >= 60:
            return 'Pass'
        else:
            return 'Fail'

    df['Status'] = df.apply(determine_status, axis=1)

    return df, report

def get_summary_kpis(df):
    """Calculate KPI metrics for the overview dashboard."""
    total_students = len(df)
    if total_students == 0:
        return {
            "total_students": 0, "class_average": 0.0, "highest_score": 0.0,
            "lowest_score": 0.0, "pass_count": 0, "pass_percentage": 0.0,
            "fail_count": 0, "fail_percentage": 0.0
        }
    
    class_average = df['Average Marks'].mean()
    highest_score = df['Average Marks'].max()
    lowest_score = df['Average Marks'].min()
    pass_count = (df['Status'] == 'Pass').sum()
    fail_count = (df['Status'] == 'Fail').sum()
    pass_percentage = (pass_count / total_students) * 100
    fail_percentage = (fail_count / total_students) * 100
    
    return {
        "total_students": total_students,
        "class_average": round(class_average, 2),
        "highest_score": round(highest_score, 2),
        "lowest_score": round(lowest_score, 2),
        "pass_count": int(pass_count),
        "pass_percentage": round(pass_percentage, 2),
        "fail_count": int(fail_count),
        "fail_percentage": round(fail_percentage, 2)
    }

def get_top_students(df, n=5):
    """Return top N performing students sorted by Average Marks."""
    if df.empty:
        return pd.DataFrame()
    # Sort by Average Marks descending, and Student ID/Name for stable tie-breaking
    sorted_df = df.sort_values(by=['Average Marks', 'Student ID'], ascending=[False, True])
    return sorted_df.head(n)
