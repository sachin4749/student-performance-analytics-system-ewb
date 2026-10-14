import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

import analytics

st.set_page_config(
    page_title="Performance Analytics System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "processed_df" not in st.session_state:
    st.session_state.processed_df = None
if "report" not in st.session_state:
    st.session_state.report = None
if "data_source" not in st.session_state:
    st.session_state.data_source = None

os.makedirs("sample_data", exist_ok=True)
sample_csv_path = "sample_data/students.csv"

np.random.seed(42)
departments = ["CSE", "ECE", "IT", "MECH", "AI/ML"]
semesters = [f"Sem {i}" for i in range(1, 9)]
first_names = ["Aarav", "Diya", "Rohan", "Ananya", "Kabir", "Neha", "Vikram", "Pooja", "Aditya", "Sneha", 
               "Rahul", "Priya", "Amit", "Kavya", "Siddharth", "Meera", "Kiran", "Divya", "Arjun", "Ankita"]
last_names = ["Sharma", "Patel", "Verma", "Iyer", "Singh", "Gupta", "Malhotra", "Nair", "Joshi", "Rao"]

rows = []
sid_counter = 101
for dept in departments:
    for sem in semesters:
        for _ in range(15):
            sid = f"S{sid_counter}"
            sid_counter += 1
            name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
            rows.append({
                'Student ID': sid, 'Name': name, 'Department': dept, 'Semester': sem,
                'Subject 1': int(np.random.randint(40, 99)),
                'Subject 2': int(np.random.randint(38, 98)),
                'Subject 3': int(np.random.randint(35, 96)),
                'Subject 4': int(np.random.randint(40, 99)),
                'Subject 5': int(np.random.randint(35, 97)),
                'Attendance': round(float(np.random.uniform(55.0, 100.0)), 1)
            })
pd.DataFrame(rows).to_csv(sample_csv_path, index=False)

st.sidebar.title("🎓 Performance Analytics")
st.sidebar.markdown("*BTech Multi-Semester Dashboard*")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Data Management")
upload_option = st.sidebar.radio(
    "Choose Data Source:",
    ("Upload CSV File", "Use Multi-Semester Sample Dataset")
)

def load_default_sample():
    try:
        df_sample = pd.read_csv(sample_csv_path)
        processed, rep = analytics.clean_and_process_data(df_sample)
        st.session_state.processed_df = processed
        st.session_state.report = rep
        st.session_state.data_source = "Multi-Semester Sample Dataset (8 Semesters)"
        st.sidebar.success("Loaded multi-semester dataset successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading sample dataset: {e}")

if upload_option == "Use Multi-Semester Sample Dataset":
    if st.sidebar.button("Load Sample Data"):
        load_default_sample()
else:
    uploaded_file = st.sidebar.file_uploader("Upload Student Dataset (.csv)", type=["csv"])
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            processed, rep = analytics.clean_and_process_data(df_upload)
            st.session_state.processed_df = processed
            st.session_state.report = rep
            st.session_state.data_source = uploaded_file.name
            st.sidebar.success(f"Successfully processed {uploaded_file.name}!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")

if st.session_state.processed_df is not None:
    if st.sidebar.button("🔄 Reset / Clear Data"):
        st.session_state.processed_df = None
        st.session_state.report = None
        st.session_state.data_source = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview Dashboard",
        "📊 Subject-Wise Performance",
        "🏢 Department & Semester Analytics",
        "📂 Semester Student Directory & PDF",
        "🏆 Top 5 Students",
        "🔍 Student Search",
        "📋 Records Explorer & Export"
    ]
)

df = st.session_state.processed_df
report = st.session_state.report

if df is None:
    st.title("🎓 Performance Analytics System")
    st.markdown("### BTech Multi-Semester Academic Analytics Dashboard")
    st.markdown("Welcome! Please load the built-in multi-semester sample dataset or upload your CSV file.")
    if st.button("🚀 Load Sample Dataset Now", type="primary"):
        load_default_sample()
        st.rerun()
else:
    st.title("Performance Analytics System")
    st.markdown(f"*Active Data Source:* **{st.session_state.data_source}** ({len(df)} records)")

    if page == "🏠 Overview Dashboard":
        st.subheader("Overview Dashboard")
        kpis = analytics.get_summary_kpis(df)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Records", kpis["total_students"])
        c2.metric("Class Average", f"{kpis['class_average']}%")
        c3.metric("Highest Score", f"{kpis['highest_score']}%")
        c4.metric("Lowest Score", f"{kpis['lowest_score']}%")
        c5.metric("Pass Rate", f"{kpis['pass_percentage']}%", f"{kpis['pass_count']} Pass")
        
        st.markdown("---")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### Grade Distribution")
            grade_counts = df['Grade'].value_counts().reindex(['A+', 'A', 'B+', 'B', 'C', 'F']).fillna(0).reset_index()
            grade_counts.columns = ['Grade', 'Count']
            fig_grade = px.bar(grade_counts, x='Grade', y='Count', color='Grade', color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_grade, use_container_width=True)
        with col_c2:
            st.markdown("#### Pass vs Fail Status")
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig_status = px.pie(status_counts, names='Status', values='Count', hole=0.4, color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'})
            st.plotly_chart(fig_status, use_container_width=True)

    elif page == "📊 Subject-Wise Performance":
        st.subheader("📊 Subject-Wise Performance by Semester & Branch")
        
        col_f1, col_f2 = st.columns(2)
        sel_dept = col_f1.selectbox("Select Department:", sorted(df['Department'].unique().tolist()))
        sel_sem = col_f2.selectbox("Select Semester:", [f"Sem {i}" for i in range(1, 9)])
        
        sem_subjects = analytics.get_semester_subjects(sel_dept, sel_sem)
        subset_df = df[(df['Department'] == sel_dept) & (df['Semester'] == sel_sem)]
        
        st.markdown(f"### Curriculum Subjects for {sel_dept} ({sel_sem}): **{', '.join(sem_subjects)}**")
        
        if subset_df.empty:
            st.warning("No records found for the selected Department and Semester combination.")
        else:
            subj_stats = []
            for i, subj_title in enumerate(sem_subjects, 1):
                col_name = f"Subject {i}"
                if col_name in subset_df.columns:
                    s_data = subset_df[col_name]
                    subj_stats.append({
                        "Subject": subj_title,
                        "Average": round(s_data.mean(), 2),
                        "Highest": int(s_data.max()),
                        "Lowest": int(s_data.min()),
                        "Median": round(s_data.median(), 2)
                    })
            df_stats = pd.DataFrame(subj_stats)
            st.dataframe(df_stats.style.highlight_max(subset=['Average', 'Highest'], color='lightgreen'), use_container_width=True)
            
            fig_s = px.bar(df_stats, x='Subject', y='Average', color='Subject', text='Average', title=f"Average Marks - {sel_dept} ({sel_sem})")
            fig_s.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_s, use_container_width=True)

    elif page == "🏢 Department & Semester Analytics":
        st.subheader("Department & Semester-Wise Summary")
        summary_group = df.groupby(['Department', 'Semester']).agg(
            Students=('Student ID', 'count'),
            Avg_Score=('Average Marks', 'mean'),
            Pass_Rate=('Status', lambda x: round((x == 'Pass').sum() / len(x) * 100, 2))
        ).reset_index()
        summary_group['Avg_Score'] = summary_group['Avg_Score'].round(2)
        st.dataframe(summary_group, use_container_width=True)

    elif page == "📂 Semester Student Directory & PDF":
        st.subheader("Semester Student Directory & PDF Report Generator")
        
        c1, c2 = st.columns(2)
        dir_dept = c1.selectbox("Select Department for Directory:", sorted(df['Department'].unique().tolist()), key="dir_dept")
        dir_sem = c2.selectbox("Select Semester:", [f"Sem {i}" for i in range(1, 9)], key="dir_sem")
        
        sem_subjects = analytics.get_semester_subjects(dir_dept, dir_sem)
        dir_subset = df[(df['Department'] == dir_dept) & (df['Semester'] == dir_sem)].sort_values(by='Student ID')
        
        st.info(f"📚 **{dir_dept} - {dir_sem} Subjects:** {', '.join(sem_subjects)}")
        
        if dir_subset.empty:
            st.warning("No student records available for this Department and Semester combination.")
        else:
            display_df = dir_subset[['Student ID', 'Name', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']].copy()
            display_df.columns = ['Student ID', 'Name', sem_subjects[0], sem_subjects[1], sem_subjects[2], sem_subjects[3], sem_subjects[4], 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
            
            st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
            
            st.markdown("---")
            pdf_buf = analytics.generate_department_semester_pdf(dir_dept, dir_sem, dir_subset)
            st.download_button(
                label=f"📥 Download {dir_dept} {dir_sem} PDF Report",
                data=pdf_buf,
                file_name=f"{dir_dept}_{dir_sem}_report.pdf",
                mime="application/pdf",
                type="primary"
            )

    elif page == "🏆 Top 5 Students":
        st.subheader("🏆 Top Performing Students")
        st.markdown("Filter top performers by Department and Semester.")
        
        c_top1, c_top2 = st.columns(2)
        top_dept = c_top1.selectbox("Filter by Department:", ["All Departments"] + sorted(df['Department'].unique().tolist()), key="top_dept")
        top_sem = c_top2.selectbox("Filter by Semester:", ["All Semesters"] + [f"Sem {i}" for i in range(1, 9)], key="top_sem")
        
        filtered_top_df = df.copy()
        if top_dept != "All Departments":
            filtered_top_df = filtered_top_df[filtered_top_df['Department'] == top_dept]
        if top_sem != "All Semesters":
            filtered_top_df = filtered_top_df[filtered_top_df['Semester'] == top_sem]
            
        top_5 = analytics.get_top_students(filtered_top_df, 5)
        
        if top_5.empty:
            st.warning("No student records found for the selected filters.")
        else:
            display_cols = ['Student ID', 'Name', 'Department', 'Semester', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Average Marks', 'Grade', 'Status']
            st.dataframe(top_5[display_cols].reset_index(drop=True), use_container_width=True)
            
            fig_top = px.bar(
                top_5, x='Name', y='Average Marks', color='Department', text='Average Marks',
                title=f"Top Students ({top_dept} | {top_sem})"
            )
            fig_top.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_top, use_container_width=True)

    elif page == "🔍 Student Search":
        st.subheader("Student Search Explorer")
        query = st.text_input("Enter Student Name or ID:")
        if query.strip():
            mask = df['Name'].str.lower().str.contains(query.lower()) | df['Student ID'].str.lower().str.contains(query.lower())
            st.dataframe(df[mask], use_container_width=True)

    elif page == "📋 Records Explorer & Export":
        st.subheader("All Records Explorer & CSV Export")
        display_cols = ['Student ID', 'Name', 'Department', 'Semester', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
        st.dataframe(df[display_cols], use_container_width=True)
        csv_data = df[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("Download Complete CSV Report", data=csv_data, file_name="complete_multisem_student_report.csv", mime="text/csv")
