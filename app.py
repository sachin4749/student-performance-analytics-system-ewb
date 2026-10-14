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
first_names = ["Aarav", "Diya", "Rohan", "Ananya", "Kabir", "Neha", "Vikram", "Pooja", "Aditya", "Sneha", 
               "Rahul", "Priya", "Amit", "Kavya", "Siddharth", "Meera", "Kiran", "Divya", "Arjun", "Ankita",
               "Varun", "Shruti", "Manish", "Tanvi", "Nikhil", "Akshay", "Pallavi", "Karthik", "Swathi", "Deepak"]
last_names = ["Sharma", "Patel", "Verma", "Iyer", "Singh", "Gupta", "Malhotra", "Nair", "Joshi", "Rao",
              "Kulkarni", "Deshmukh", "Patil", "Reddy", "Choudhury", "Mehta", "Shah", "Bose", "Das", "Menon"]

rows = []
sid_counter = 101
for dept in departments:
    for _ in range(45):
        sid = f"S{sid_counter}"
        sid_counter += 1
        name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
        rows.append({
            'Student ID': sid, 'Name': name, 'Department': dept,
            'Subject 1': int(np.random.randint(40, 99)),
            'Subject 2': int(np.random.randint(38, 98)),
            'Subject 3': int(np.random.randint(35, 96)),
            'Subject 4': int(np.random.randint(40, 99)),
            'Subject 5': int(np.random.randint(35, 97)),
            'Attendance': round(float(np.random.uniform(55.0, 100.0)), 1)
        })
pd.DataFrame(rows).to_csv(sample_csv_path, index=False)

st.sidebar.title("🎓 Performance Analytics")
st.sidebar.markdown("*BTech Student Performance Dashboard*")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Data Management")
upload_option = st.sidebar.radio(
    "Choose Data Source:",
    ("Upload CSV File", "Use Sample Dataset (225 Students / 45 per Dept)")
)

def load_default_sample():
    try:
        df_sample = pd.read_csv(sample_csv_path)
        processed, rep = analytics.clean_and_process_data(df_sample)
        st.session_state.processed_df = processed
        st.session_state.report = rep
        st.session_state.data_source = "Sample Dataset (225 Students)"
        st.sidebar.success("Loaded 225 sample students successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading sample dataset: {e}")

if upload_option == "Use Sample Dataset (225 Students / 45 per Dept)":
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
        "🏢 Department Analytics",
        "📂 Department Student Directory",
        "🏆 Top 5 Students",
        "🔍 Student Search",
        "📋 Records Explorer & Export"
    ]
)

df = st.session_state.processed_df
report = st.session_state.report

if df is None:
    st.title("🎓 Performance Analytics System")
    st.markdown("### BTech Student Performance Analytics Dashboard")
    st.markdown("Welcome! Please load the built-in 225-student sample dataset (45 students across CSE, ECE, IT, MECH, and AI/ML with department-specific subjects) or upload your CSV file.")
    if st.button("🚀 Load 225 Sample Students Now", type="primary"):
        load_default_sample()
        st.rerun()
else:
    st.title("Performance Analytics System")
    st.markdown(f"*Active Data Source:* **{st.session_state.data_source}** ({len(df)} records)")

    if page == "🏠 Overview Dashboard":
        st.subheader("Overview Dashboard")
        kpis = analytics.get_summary_kpis(df)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Students", kpis["total_students"])
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
        st.subheader("📊 Subject-Wise Academic Performance")
        st.markdown("Analyze curriculum performance across different engineering branches with their relative subjects.")
        
        all_depts = sorted(df['Department'].unique().tolist())
        selected_subj_dept = st.selectbox("Select Department to View Subject Performance:", all_depts, key="subj_dept_select")
        
        dept_subj_names = analytics.get_department_subjects(selected_subj_dept)
        dept_subset = df[df['Department'] == selected_subj_dept]
        
        subj_stats = []
        for i, subj_title in enumerate(dept_subj_names, 1):
            col_name = f"Subject {i}"
            if col_name in dept_subset.columns:
                subj_data = dept_subset[col_name]
                subj_stats.append({
                    "Subject Name": subj_title,
                    "Average Marks": round(subj_data.mean(), 2),
                    "Highest Mark": int(subj_data.max()),
                    "Lowest Mark": int(subj_data.min()),
                    "Median Mark": round(subj_data.median(), 2)
                })
        
        df_subj_stats = pd.DataFrame(subj_stats)
        st.markdown(f"### {selected_subj_dept} Department Subject Statistics")
        st.dataframe(df_subj_stats.style.highlight_max(subset=['Average Marks', 'Highest Mark'], color='lightgreen'), use_container_width=True)
        
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"#### {selected_subj_dept} - Comparative Subject Averages")
            fig_subj_avg = px.bar(
                df_subj_stats, x='Subject Name', y='Average Marks',
                color='Subject Name', text='Average Marks',
                title=f"Average Marks in {selected_subj_dept}"
            )
            fig_subj_avg.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_subj_avg, use_container_width=True)
            
        with col_s2:
            st.markdown(f"#### {selected_subj_dept} - Subject Spread (Box Plot)")
            box_records = []
            for i, subj_title in enumerate(dept_subj_names, 1):
                col_name = f"Subject {i}"
                if col_name in dept_subset.columns:
                    for val in dept_subset[col_name]:
                        box_records.append({"Subject": subj_title, "Marks": val})
            df_box = pd.DataFrame(box_records)
            fig_box = px.box(
                df_box, x='Subject', y='Marks', color='Subject',
                title=f"Marks Distribution in {selected_subj_dept}"
            )
            fig_box.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)

    elif page == "🏢 Department Analytics":
        st.subheader("Department-Wise Summary")
        dept_grouped = df.groupby('Department').agg(
            Total_Students=('Student ID', 'count'),
            Average_Score=('Average Marks', 'mean'),
            Pass_Count=('Status', lambda x: (x == 'Pass').sum())
        ).reset_index()
        dept_grouped['Pass_Percentage'] = (dept_grouped['Pass_Count'] / dept_grouped['Total_Students'] * 100).round(2)
        dept_grouped['Average_Score'] = dept_grouped['Average_Score'].round(2)
        st.dataframe(dept_grouped, use_container_width=True)

    elif page == "📂 Department Student Directory":
        st.subheader("Department Student Directory & PDF Reports")
        departments = sorted(df['Department'].unique().tolist())
        selected_dept = st.selectbox("Select Department:", departments)
        
        dept_subjects = analytics.get_department_subjects(selected_dept)
        st.info(f"📚 **Curriculum Subjects for {selected_dept}:** {', '.join(dept_subjects)}")
        
        dept_df = df[df['Department'] == selected_dept].sort_values(by='Student ID')
        
        display_df = dept_df[['Student ID', 'Name', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']].copy()
        display_df.columns = ['Student ID', 'Name', dept_subjects[0], dept_subjects[1], dept_subjects[2], dept_subjects[3], dept_subjects[4], 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
        
        st.markdown(f"### {selected_dept} Department Students ({len(dept_df)} records)")
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
        
        st.markdown("---")
        pdf_buffer = analytics.generate_department_pdf(selected_dept, dept_df)
        st.download_button(
            label=f"📥 Download {selected_dept} Department PDF Report",
            data=pdf_buffer,
            file_name=f"{selected_dept}_department_report.pdf",
            mime="application/pdf",
            type="primary"
        )

    elif page == "🏆 Top 5 Students":
        st.subheader("Top Performing Students")
        top_5 = analytics.get_top_students(df, 5)
        display_cols = ['Student ID', 'Name', 'Department', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Average Marks', 'Grade', 'Status']
        st.dataframe(top_5[display_cols].reset_index(drop=True), use_container_width=True)

    elif page == "🔍 Student Search":
        st.subheader("Student Search Explorer")
        query = st.text_input("Enter Student Name or ID:")
        if query.strip():
            mask = df['Name'].str.lower().str.contains(query.lower()) | df['Student ID'].str.lower().str.contains(query.lower())
            st.dataframe(df[mask], use_container_width=True)

    elif page == "📋 Records Explorer & Export":
        st.subheader("All Records Explorer & CSV Export")
        display_cols = ['Student ID', 'Name', 'Department', 'Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
        st.dataframe(df[display_cols], use_container_width=True)
        csv_data = df[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("Download Complete CSV Report", data=csv_data, file_name="processed_student_report.csv", mime="text/csv")
