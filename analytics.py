import pandas as pd
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

REQUIRED_COLUMNS = ['Student ID', 'Name', 'Department', 'Semester', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance']
SUBJECTS = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']

# Department and Semester-wise curriculum subject mapping
CURRICULUM = {
    "CSE": {
        "Sem 1": ["Engineering Math-I", "Engineering Physics", "Basic Electrical", "C Programming", "Environmental Sci."],
        "Sem 2": ["Engineering Math-II", "Engineering Chemistry", "Data Structures", "Digital Logic", "Python Programming"],
        "Sem 3": ["Discrete Structures", "Object Oriented Prog.", "Computer Organization", "DBMS", "Software Eng."],
        "Sem 4": ["Design & Analysis of Alg.", "Operating Systems", "Computer Networks", "Theory of Computation", "Microprocessors"],
        "Sem 5": ["Compiler Design", "Web Technologies", "Computer Graphics", "Artificial Intelligence", "Information Security"],
        "Sem 6": ["Cloud Computing", "Machine Learning", "Data Warehousing", "Distributed Systems", "Mobile Computing"],
        "Sem 7": ["Big Data Analytics", "Deep Learning", "Internet of Things", "DevOps Engineering", "Blockchain Tech."],
        "Sem 8": ["Major Project Phase-II", "Industrial Internship", "Cyber Law & Ethics", "Advanced Networking", "Startup Management"]
    },
    "ECE": {
        "Sem 1": ["Engineering Math-I", "Engineering Physics", "Basic Electrical", "C Programming", "Environmental Sci."],
        "Sem 2": ["Engineering Math-II", "Engineering Chemistry", "Electronic Devices", "Network Analysis", "Python Programming"],
        "Sem 3": ["Signals & Systems", "Digital Electronics", "Analog Circuits", "Electromagnetic Fields", "Network Theory"],
        "Sem 4": ["Microprocessors", "Control Systems", "Analog Communication", "Linear Integrated Circuits", "Measurements"],
        "Sem 5": ["Digital Communication", "DSP", "VLSI Design", "Antenna & Wave Prop.", "Embedded Systems"],
        "Sem 6": ["Computer Communication", "Optical Communication", "Wireless Networks", "IC Technology", "RF Circuit Design"],
        "Sem 7": ["Satellite Communication", "Radar & Navigational Aids", "IoT Systems", "MEMS", "Neural Networks"],
        "Sem 8": ["Major Project Phase-II", "Industrial Internship", "Radar Systems", "Biomedical Signal Processing", "Robotics"]
    },
    "IT": {
        "Sem 1": ["Engineering Math-I", "Engineering Physics", "Basic Electrical", "C Programming", "Environmental Sci."],
        "Sem 2": ["Engineering Math-II", "Engineering Chemistry", "Data Structures", "Digital Logic", "Python Programming"],
        "Sem 3": ["Discrete Mathematics", "OOP with Java", "Computer Organization", "DBMS", "Web Essentials"],
        "Sem 4": ["Design & Analysis of Alg.", "Operating Systems", "Computer Networks", "Software Engineering", "Microprocessors"],
        "Sem 5": ["Advanced Web Tech", "Information Security", "Graphics & Multimedia", "Computer Architecture", "Human Computer Interaction"],
        "Sem 6": ["Cloud Computing", "Data Warehousing", "Cyber Security", "Distributed Systems", "Mobile App Development"],
        "Sem 7": ["Big Data Analytics", "IoT Architecture", "Information Retrieval", "DevOps", "Service Oriented Arch."],
        "Sem 8": ["Major Project Phase-II", "Industrial Internship", "E-Commerce & ERP", "Storage Networks", "IT Project Management"]
    },
    "MECH": {
        "Sem 1": ["Engineering Math-I", "Engineering Physics", "Basic Electrical", "Engineering Mechanics", "Environmental Sci."],
        "Sem 2": ["Engineering Math-II", "Engineering Chemistry", "Engineering Graphics", "Basic Electronics", "Workshop Tech."],
        "Sem 3": ["Thermodynamics", "Strength of Materials", "Material Science", "Fluid Mechanics", "Kinematics of Machines"],
        "Sem 4": ["Applied Thermodynamics", "Dynamics of Machinery", "Manufacturing Processes", "Machine Drawing", "Fluid Machines"],
        "Sem 5": ["Design of Machine Elements", "Heat Transfer", "Metrology & Quality Cont.", "Industrial Engineering", "CAD / CAM"],
        "Sem 6": ["Internal Combustion Engines", "Mechatronics", "Dynamics & Vibration", "Automobile Engineering", "Operations Research"],
        "Sem 7": ["Refrigeration & A/C", "Power Plant Engineering", "Finite Element Methods", "Robotics", "Renewable Energy"],
        "Sem 8": ["Major Project Phase-II", "Industrial Internship", "Advanced Manufacturing", "Supply Chain Management", "Plant Maintenance"]
    },
    "AI/ML": {
        "Sem 1": ["Engineering Math-I", "Engineering Physics", "Basic Electrical", "C Programming", "Environmental Sci."],
        "Sem 2": ["Linear Algebra & Calculus", "Engineering Chemistry", "Data Structures", "Statistics for AI", "Python Programming"],
        "Sem 3": ["Discrete Mathematics", "Object Oriented Prog.", "Database Management", "Algorithms", "Foundations of AI"],
        "Sem 4": ["Machine Learning Basics", "Probability & Random Proc.", "Computer Networks", "Operating Systems", "Data Mining"],
        "Sem 5": ["Deep Learning", "Natural Language Processing", "Computer Vision", "Software Engineering", "Big Data Analytics"],
        "Sem 6": ["Reinforcement Learning", "Neural Networks", "Cloud AI Services", "Web Intelligence", "Time Series Analysis"],
        "Sem 7": ["Generative AI & LLMs", "Edge AI & IoT", "AI Ethics & Governance", "Robotics & Perception", "Knowledge Representation"],
        "Sem 8": ["Major Project Phase-II", "Industrial Internship", "Autonomous Systems", "Quantum Computing Basics", "AI Enterprise Deployment"]
    }
}

def get_semester_subjects(dept_name, semester_name):
    dept_cur = CURRICULUM.get(dept_name, {})
    return dept_cur.get(semester_name, ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"])

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
                median_val = df[subj].median() if not df[subj].dropna().empty else 0
                df[subj] = df[subj].fillna(median_val)
                imputation_log.append(f"Imputed {missing_count} missing value(s) in '{subj}' with median.")

    if 'Attendance' in df.columns:
        att_missing = df['Attendance'].isnull().sum()
        if att_missing > 0:
            mean_val = df['Attendance'].mean() if not df['Attendance'].dropna().empty else 0.0
            df['Attendance'] = df['Attendance'].fillna(mean_val)
            imputation_log.append(f"Imputed {att_missing} missing value(s) in 'Attendance'.")

    report["imputation_log"] = imputation_log

    for subj in SUBJECTS:
        if subj in df.columns:
            df[subj] = df[subj].clip(0, 100)
    if 'Attendance' in df.columns:
        df['Attendance'] = df['Attendance'].clip(0, 100)

    for meta_col in ['Student ID', 'Name', 'Department', 'Semester']:
        if meta_col in df.columns:
            df[meta_col] = df[meta_col].fillna("Unknown").astype(str).str.strip()

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
        return 'Pass' if (row['Average Marks'] >= 45 and row['Attendance'] >= 60) else 'Fail'

    df['Status'] = df.apply(determine_status, axis=1)
    return df, report

def get_summary_kpis(df):
    total_students = len(df)
    if total_students == 0:
        return {"total_students": 0, "class_average": 0.0, "highest_score": 0.0, "lowest_score": 0.0, "pass_count": 0, "pass_percentage": 0.0, "fail_count": 0}
    
    class_average = df['Average Marks'].mean()
    highest_score = df['Average Marks'].max()
    lowest_score = df['Average Marks'].min()
    pass_count = (df['Status'] == 'Pass').sum()
    pass_percentage = (pass_count / total_students) * 100
    
    return {
        "total_students": total_students,
        "class_average": round(class_average, 2),
        "highest_score": round(highest_score, 2),
        "lowest_score": round(lowest_score, 2),
        "pass_count": int(pass_count),
        "pass_percentage": round(pass_percentage, 2),
        "fail_count": int(total_students - pass_count)
    }

def get_top_students(df, n=5):
    if df.empty: return pd.DataFrame()
    return df.sort_values(by=['Average Marks', 'Student ID'], ascending=[False, True]).head(n)

def generate_department_semester_pdf(department_name, semester_name, dept_sem_df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1f77b4'), spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#555555'), spaceAfter=10)
    
    sem_subjects = get_semester_subjects(department_name, semester_name)
    
    elements.append(Paragraph(f"Academic Report: {department_name} - {semester_name}", title_style))
    elements.append(Paragraph(f"Subjects: {', '.join(sem_subjects)} | Total Students: {len(dept_sem_df)}", subtitle_style))
    elements.append(Spacer(1, 6))
    
    table_data = [['ID', 'Name', 'Sub1', 'Sub2', 'Sub3', 'Sub4', 'Sub5', 'Att%', 'Avg%', 'Grade', 'Status']]
    for _, row in dept_sem_df.iterrows():
        table_data.append([
            str(row['Student ID']), str(row['Name']),
            str(row['Subject 1']), str(row['Subject 2']), str(row['Subject 3']), str(row['Subject 4']), str(row['Subject 5']),
            f"{row['Attendance']}%", f"{round(row['Average Marks'], 1)}%", str(row['Grade']), str(row['Status'])
        ])
        
    t = Table(table_data, colWidths=[52, 110, 42, 42, 42, 42, 42, 45, 45, 42, 48])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
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
