import pandas as pd
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

REQUIRED_COLUMNS = ['Student ID', 'Name', 'Department', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance']
SUBJECTS = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']

DEPT_SUBJECT_NAMES = {
    "CSE": ["Python", "Data Structures", "DBMS", "Computer Networks", "Operating Systems"],
    "ECE": ["Signals & Systems", "Microcontrollers", "VLSI Design", "Analog Circuits", "Digital Comm."],
    "IT": ["Web Tech", "Software Eng.", "Cloud Computing", "Cyber Security", "Data Warehousing"],
    "MECH": ["Thermodynamics", "Fluid Mechanics", "Machine Design", "CAD / CAM", "Manufacturing"],
    "AI/ML": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Mining"]
}

def get_department_subjects(dept_name):
    return DEPT_SUBJECT_NAMES.get(dept_name, ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"])

def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing

def clean_and_process_data(df):
    df = df.copy()
    report = {
        "missing_columns": [],
        "imputation_log": [],
        "invalid_ranges_log": [],
        "records_processed": len(df),
        "data_quality_notes": []
    }
    
    missing_cols = validate_columns(df)
    if missing_cols:
        report["missing_columns"] = missing_cols
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")

    for col in SUBJECTS + ['Attendance']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    imputation_log = []
    for subj in SUBJECTS:
        if subj in df.columns:
            missing_count = df[subj].isnull().sum()
            if missing_count > 0:
                if df[subj].dropna().empty:
                    df[subj] = df[subj].fillna(0)
                    imputation_log.append(f"Subject '{subj}' has no valid numeric values; imputed with 0.")
                else:
                    median_val = df[subj].median()
                    df[subj] = df[subj].fillna(median_val)
                    imputation_log.append(f"Imputed {missing_count} missing value(s) in '{subj}' with median ({median_val:.2f}).")

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

    invalid_ranges_log = []
    for subj in SUBJECTS:
        if subj in df.columns:
            invalid_mask = (df[subj] < 0) | (df[subj] > 100)
            invalid_count = invalid_mask.sum()
            if invalid_count > 0:
                invalid_ranges_log.append(f"Found {invalid_count} out-of-range value(s) in '{subj}'. Clipped.")
                df[subj] = df[subj].clip(0, 100)

    if 'Attendance' in df.columns:
        att_invalid = (df['Attendance'] < 0) | (df['Attendance'] > 100)
        att_inv_count = att_invalid.sum()
        if att_inv_count > 0:
            invalid_ranges_log.append(f"Found {att_inv_count} out-of-range value(s) in 'Attendance'. Clipped.")
            df['Attendance'] = df['Attendance'].clip(0, 100)

    report["invalid_ranges_log"] = invalid_ranges_log

    for meta_col in ['Student ID', 'Name', 'Department']:
        if meta_col in df.columns:
            df[meta_col] = df[meta_col].fillna("Unknown").astype(str).str.strip()
            df[meta_col] = df[meta_col].replace('', 'Unknown')

    df['Total Marks'] = df[SUBJECTS].sum(axis=1)
    df['Max Possible'] = len(SUBJECTS) * 100
    df['Average Marks'] = df['Total Marks'] / len(SUBJECTS)

    def assign_grade(avg):
        if avg >= 85: return 'A+'
        elif avg >= 75: return 'A'
        elif avg >= 65: return 'B+'
        elif avg >= 55: return 'B'
        elif avg >= 45: return 'C'
        else: return 'F'

    df['Grade'] = df['Average Marks'].apply(assign_grade)

    def determine_status(row):
        if row['Average Marks'] >= 45 and row['Attendance'] >= 60:
            return 'Pass'
        else:
            return 'Fail'

    df['Status'] = df.apply(determine_status, axis=1)

    return df, report

def get_summary_kpis(df):
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
    
    return {
        "total_students": total_students,
        "class_average": round(class_average, 2),
        "highest_score": round(highest_score, 2),
        "lowest_score": round(lowest_score, 2),
        "pass_count": int(pass_count),
        "pass_percentage": round(pass_percentage, 2),
        "fail_count": int(fail_count),
        "fail_percentage": round((fail_count / total_students) * 100, 2)
    }

def get_top_students(df, n=5):
    if df.empty: return pd.DataFrame()
    return df.sort_values(by=['Average Marks', 'Student ID'], ascending=[False, True]).head(n)

def generate_department_pdf(department_name, dept_df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1f77b4'), spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#555555'), spaceAfter=12
    )
    
    dept_subj = get_department_subjects(department_name)
    
    elements.append(Paragraph(f"Department Performance Report: {department_name}", title_style))
    elements.append(Paragraph(f"Subjects: {', '.join(dept_subj)} | Total Students: {len(dept_df)}", subtitle_style))
    elements.append(Spacer(1, 8))
    
    table_data = [['ID', 'Name', 'Sub1', 'Sub2', 'Sub3', 'Sub4', 'Sub5', 'Att%', 'Avg%', 'Grade', 'Status']]
    
    for _, row in dept_df.iterrows():
        table_data.append([
            str(row['Student ID']),
            str(row['Name']),
            str(row['Subject 1']),
            str(row['Subject 2']),
            str(row['Subject 3']),
            str(row['Subject 4']),
            str(row['Subject 5']),
            f"{row['Attendance']}%",
            f"{round(row['Average Marks'], 1)}%",
            str(row['Grade']),
            str(row['Status'])
        ])
        
    t = Table(table_data, colWidths=[52, 110, 42, 42, 42, 42, 42, 45, 45, 42, 48])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f9f9f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 3),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3),
    ]))
    
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer
