import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

import analytics

# Page Configuration
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

# Ensure sample_data directory exists and has 50 sample students if missing
os.makedirs("sample_data", exist_ok=True)
sample_csv_path = "sample_data/students.csv"

if not os.path.exists(sample_csv_path):
    np.random.seed(42)
    sample_data_dict = {
        'Student ID': [f"S{101+i}" for i in range(50)],
        'Name': [
            "Aarav Sharma", "Diya Patel", "Rohan Verma", "Ananya Iyer", "Kabir Singh",
            "Neha Gupta", "Vikram Malhotra", "Pooja Nair", "Aditya Joshi", "Sneha Rao",
            "Rahul Kulkarni", "Priya Deshmukh", "Amit Patil", "Kavya Reddy", "Siddharth Choudhury",
            "Meera Mehta", "Kiran Shah", "Divya Bose", "Arjun Das", "Ankita Menon",
            "Varun Pillai", "Shruti Shetty", "Manish Nambiar", "Tanvi Verghese", "Nikhil Ranganathan",
            "Akshay Desai", "Pallavi Jadhav", "Karthik Shinde", "Swathi More", "Deepak Sharma",
            "Pranav Patel", "Ritu Verma", "Vishal Iyer", "Nisha Singh", "Sanjay Gupta",
            "Geeta Malhotra", "Abhishek Nair", "Komal Joshi", "Harsh Rao", "Poonam Kulkarni",
            "Tarun Deshmukh", "Bhavna Patil", "Sachin Reddy", "Meghana Choudhury", "Akash Mehta",
            "Rachana Shah", "Naveen Bose", "Jyoti Das", "Yash Menon", "Monika Pillai"
        ],
        'Department': [
            "CSE", "ECE", "IT", "MECH", "AI/ML", "CSE", "ECE", "IT", "MECH", "AI/ML",
            "CSE", "ECE", "IT", "MECH", "AI/ML", "CSE", "ECE", "IT", "MECH", "AI/ML",
            "CSE", "ECE", "IT", "MECH", "AI/ML", "CSE", "ECE", "IT", "MECH", "AI/ML",
            "CSE", "ECE", "IT", "MECH", "AI/ML", "CSE", "ECE", "IT", "MECH", "AI/ML",
            "CSE", "ECE", "IT", "MECH", "AI/ML", "CSE", "ECE", "IT", "MECH", "AI/ML"
        ],
        'Python': np.random.randint(40, 99, size=50),
        'SQL': np.random.randint(38, 98, size=50),
        'C++': np.random.randint(35, 96, size=50),
        'OOP': np.random.randint(40, 99, size=50),
        'IOT': np.random.randint(35, 97, size=50),
        'Attendance': np.round(np.random.uniform(55.0, 100.0, size=50), 1)
    }
    pd.DataFrame(sample_data_dict).to_csv(sample_csv_path, index=False)

st.sidebar.title("🎓 Performance Analytics")
st.sidebar.markdown("*BTech Student Performance Dashboard*")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Data Management")
upload_option = st.sidebar.radio(
    "Choose Data Source:",
    ("Upload CSV File", "Use Sample Dataset (50 Students)")
)

def load_default_sample():
    try:
        df_sample = pd.read_csv(sample_csv_path)
        processed, rep = analytics.clean_and_process_data(df_sample)
        st.session_state.processed_df = processed
        st.session_state.report = rep
        st.session_state.data_source = "Sample Dataset (50 Students)"
        st.sidebar.success("Loaded 50 sample students successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading sample dataset: {e}")

if upload_option == "Use Sample Dataset (50 Students)":
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
    st.markdown("Welcome! Please load the built-in 50-student sample dataset or upload your CSV file to view all student records, department directories, and download PDF reports.")
    if st.button("🚀 Load 50 Sample Students Now", type="primary"):
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
        st.subheader("Subject-Wise Academic Performance")
        subjects = analytics.SUBJECTS
        subj_stats = [{"Subject": s, "Average": round(df[s].mean(), 2), "Highest": df[s].max(), "Lowest": df[s].min()} for s in subjects if s in df.columns]
        st.dataframe(pd.DataFrame(subj_stats), use_container_width=True)

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
        st.markdown("View all students sorted by their departments, check their Student IDs and names, and download official department PDF reports.")
        
        departments = sorted(df['Department'].unique().tolist())
        selected_dept = st.selectbox("Select Department:", departments)
        
        dept_df = df[df['Department'] == selected_dept].sort_values(by='Student ID')
        
        st.markdown(f"### {selected_dept} Department Students ({len(dept_df)} records)")
        display_cols = ['Student ID', 'Name', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
        st.dataframe(dept_df[display_cols].reset_index(drop=True), use_container_width=True)
        
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
        display_cols = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Average Marks', 'Grade', 'Status']
        st.dataframe(top_5[display_cols].reset_index(drop=True), use_container_width=True)

    elif page == "🔍 Student Search":
        st.subheader("Student Search Explorer")
        query = st.text_input("Enter Student Name or ID:")
        if query.strip():
            mask = df['Name'].str.lower().str.contains(query.lower()) | df['Student ID'].str.lower().str.contains(query.lower())
            st.dataframe(df[mask], use_container_width=True)

    elif page == "📋 Records Explorer & Export":
        st.subheader("All Records Explorer & CSV Export")
        display_cols = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
        st.dataframe(df[display_cols], use_container_width=True)
        csv_data = df[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("Download Complete CSV Report", data=csv_data, file_name="processed_student_report.csv", mime="text/csv")
