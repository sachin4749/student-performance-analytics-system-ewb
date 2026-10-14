import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

import analytics

# Page Configuration
st.set_page_config(
    page_title="Performance Analytics System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None
if "report" not in st.session_state:
    st.session_state.report = None
if "data_source" not in st.session_state:
    st.session_state.data_source = None

# Sidebar Navigation & Upload
st.sidebar.title("🎓 Performance Analytics")
st.sidebar.markdown("*BTech Student Performance Dashboard*")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Data Management")
upload_option = st.sidebar.radio(
    "Choose Data Source:",
    ("Upload CSV File", "Use Sample Dataset")
)

sample_csv_path = "sample_data/students.csv"

def load_default_sample():
    try:
        df_sample = pd.read_csv(sample_csv_path)
        processed, rep = analytics.clean_and_process_data(df_sample)
        st.session_state.processed_df = processed
        st.session_state.report = rep
        st.session_state.data_source = "Sample Dataset"
        st.sidebar.success("Sample dataset loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading sample dataset: {e}")

if upload_option == "Use Sample Dataset":
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
        except ValueError as ve:
            st.sidebar.error(f"Validation Error: {ve}")
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
        "🏆 Top 5 Students",
        "🔍 Student Search",
        "📋 Records Explorer & Export"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Performance Analytics System v1.0**\n"
    "Built with Python, Pandas, NumPy & Streamlit."
)

# Main Application Logic
df = st.session_state.processed_df
report = st.session_state.report

if df is None:
    # Welcome Screen
    st.title("🎓 Performance Analytics System")
    st.markdown("### BTech Student Performance Analytics Dashboard")
    st.markdown("Welcome! Please upload a student CSV dataset using the sidebar or load the built-in sample dataset to begin analyzing student academic records, subject distributions, departmental performance, and individual student profiles.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Getting Started**\n1. Select **Use Sample Dataset** or upload your own CSV file in the sidebar.\n2. Explore interactive metrics, charts, department summaries, and top performer rankings.\n3. Search for individual records and export processed reports.")
    with col2:
        st.warning("📋 **Required CSV Columns**\n`Student ID`, `Name`, `Department`, `Python`, `SQL`, `C++`, `OOP`, `IOT`, `Attendance`")
        if st.button("🚀 Load Sample Dataset Now", type="primary"):
            load_default_sample()
            st.rerun()
            
else:
    # Header Info
    st.title("Performance Analytics System")
    st.markdown("*BTech Student Performance Analytics Dashboard*")
    if st.session_state.data_source:
        st.caption(f"Active Data Source: **{st.session_state.data_source}** ({len(df)} records loaded)")

    # Data Quality Expander
    if report:
        with st.expander("🔍 Data Quality & Processing Summary", expanded=False):
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                st.metric("Total Records Processed", report["records_processed"])
                if report["missing_columns"]:
                    st.error(f"Missing Columns: {report['missing_columns']}")
                else:
                    st.success("All required columns validated successfully.")
            with col_q2:
                if report["imputation_log"]:
                    st.write("**Imputation Notes:**")
                    for log in report["imputation_log"]:
                        st.write(f"- {log}")
                else:
                    st.write("No missing values required imputation.")
                
                if report["invalid_ranges_log"]:
                    st.write("**Range Validation Notes:**")
                    for log in report["invalid_ranges_log"]:
                        st.write(f"- {log}")

    # ================= PAGE 1: OVERVIEW DASHBOARD =================
    if page == "🏠 Overview Dashboard":
        st.subheader("Overview Dashboard")
        
        kpis = analytics.get_summary_kpis(df)
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Students", kpis["total_students"])
        c2.metric("Class Average", f"{kpis['class_average']}%")
        c3.metric("Highest Score", f"{kpis['highest_score']}%")
        c4.metric("Lowest Score", f"{kpis['lowest_score']}%")
        c5.metric("Pass Rate", f"{kpis['pass_percentage']}%", f"{kpis['pass_count']} Pass / {kpis['fail_count']} Fail")
        
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### Grade Distribution")
            grade_counts = df['Grade'].value_counts().reindex(['A+', 'A', 'B+', 'B', 'C', 'F']).fillna(0).reset_index()
            grade_counts.columns = ['Grade', 'Count']
            fig_grade = px.bar(
                grade_counts, x='Grade', y='Count',
                color='Grade',
                color_discrete_sequence=px.colors.sequential.Blues_r,
                text='Count',
                title="Student Count by Grade"
            )
            fig_grade.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_grade, use_container_width=True)
            
        with col_chart2:
            st.markdown("#### Pass vs. Fail Status")
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig_status = px.pie(
                status_counts, names='Status', values='Count',
                hole=0.4,
                color='Status',
                color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'},
                title="Overall Pass/Fail Proportion"
            )
            fig_status.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_status, use_container_width=True)
            
        st.markdown("#### Department Average Scores")
        dept_avg = df.groupby('Department')['Average Marks'].mean().reset_index()
        fig_dept = px.bar(
            dept_avg, x='Department', y='Average Marks',
            color='Department',
            text=dept_avg['Average Marks'].round(1),
            title="Average Performance by Department"
        )
        fig_dept.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_dept, use_container_width=True)

    # ================= PAGE 2: SUBJECT-WISE PERFORMANCE =================
    elif page == "📊 Subject-Wise Performance":
        st.subheader("Subject-Wise Academic Performance")
        
        subjects = analytics.SUBJECTS
        subj_stats = []
        for subj in subjects:
            if subj in df.columns:
                subj_stats.append({
                    "Subject": subj,
                    "Average": round(df[subj].mean(), 2),
                    "Highest": df[subj].max(),
                    "Lowest": df[subj].min(),
                    "Median": round(df[subj].median(), 2)
                })
        df_stats = pd.DataFrame(subj_stats)
        
        st.dataframe(df_stats.style.highlight_max(subset=['Average', 'Highest'], color='lightgreen'), use_container_width=True)
        
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("#### Comparative Subject Averages")
            fig_subj_avg = px.bar(
                df_stats, x='Subject', y='Average',
                color='Subject',
                text='Average',
                title="Average Marks Across Subjects"
            )
            fig_subj_avg.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_subj_avg, use_container_width=True)
            
        with col_s2:
            st.markdown("#### Subject Marks Distribution (Box Plot)")
            box_data = df.melt(value_vars=subjects, var_name='Subject', value_name='Marks')
            fig_box = px.box(
                box_data, x='Subject', y='Marks',
                color='Subject',
                title="Spread of Marks per Subject"
            )
            fig_box.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)

    # ================= PAGE 3: DEPARTMENT ANALYTICS =================
    elif page == "🏢 Department Analytics":
        st.subheader("Department-Wise Analytics")
        
        if 'Department' in df.columns:
            dept_grouped = df.groupby('Department').agg(
                Total_Students=('Student ID', 'count'),
                Average_Score=('Average Marks', 'mean'),
                Highest_Score=('Average Marks', 'max'),
                Lowest_Score=('Average Marks', 'min'),
                Pass_Count=('Status', lambda x: (x == 'Pass').sum())
            ).reset_index()
            
            dept_grouped['Pass_Percentage'] = (dept_grouped['Pass_Count'] / dept_grouped['Total_Students'] * 100).round(2)
            dept_grouped['Average_Score'] = dept_grouped['Average_Score'].round(2)
            
            st.dataframe(dept_grouped, use_container_width=True)
            
            st.markdown("---")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                fig_d_pass = px.bar(
                    dept_grouped, x='Department', y='Pass_Percentage',
                    color='Department',
                    text=dept_grouped['Pass_Percentage'].astype(str) + '%',
                    title="Pass Percentage by Department"
                )
                fig_d_pass.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_d_pass, use_container_width=True)
                
            with col_d2:
                fig_d_score = px.bar(
                    dept_grouped, x='Department', y='Average_Score',
                    color='Department',
                    text='Average_Score',
                    title="Average Score by Department"
                )
                fig_d_score.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_d_score, use_container_width=True)

    # ================= PAGE 4: TOP 5 STUDENTS =================
    elif page == "🏆 Top 5 Students":
        st.subheader("Top Performing Students")
        st.markdown("Ranked by **Average Marks** (with stable tie-breaking on Student ID).")
        
        top_5 = analytics.get_top_students(df, 5)
        
        if top_5.empty:
            st.info("No student records available.")
        else:
            display_cols = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
            st.dataframe(top_5[display_cols].reset_index(drop=True), use_container_width=True)
            
            # Bar chart of top students
            fig_top = px.bar(
                top_5, x='Name', y='Average Marks',
                color='Department',
                text='Average Marks',
                title="Top Students Score Comparison"
            )
            fig_top.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_top, use_container_width=True)

    # ================= PAGE 5: STUDENT SEARCH =================
    elif page == "🔍 Student Search":
        st.subheader("Student Search Explorer")
        st.markdown("Search for students by **Name** or **Student ID** (case-insensitive partial matching).")
        
        search_query = st.text_input("Enter Student Name or ID:", "")
        
        if search_query.strip():
            query_lower = search_query.strip().lower()
            mask = (
                df['Name'].astype(str).str.lower().str.contains(query_lower) |
                df['Student ID'].astype(str).str.lower().str.contains(query_lower)
            )
            search_results = df[mask]
            
            st.markdown(f"Found **{len(search_results)}** matching record(s):")
            if not search_results.empty:
                display_cols = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Total Marks', 'Average Marks', 'Grade', 'Status']
                st.dataframe(search_results[display_cols], use_container_width=True)
            else:
                st.warning("No student matches your search query. Please check the spelling or ID and try again.")
        else:
            st.info("Please enter a search term above to find specific student records.")

    # ================= PAGE 6: RECORDS EXPLORER & EXPORT =================
    elif page == "📋 Records Explorer & Export":
        st.subheader("Student Records Explorer & Export")
        st.markdown("Filter, sort, and explore complete processed student records, then download reports.")
        
        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        
        departments = ['All'] + sorted(df['Department'].unique().tolist())
        selected_dept = col_f1.selectbox("Filter by Department", departments)
        
        grades = ['All'] + sorted(df['Grade'].unique().tolist())
        selected_grade = col_f2.selectbox("Filter by Grade", grades)
        
        statuses = ['All'] + sorted(df['Status'].unique().tolist())
        selected_status = col_f3.selectbox("Filter by Status", statuses)
        
        filtered_df = df.copy()
        if selected_dept != 'All':
            filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
        if selected_grade != 'All':
            filtered_df = filtered_df[filtered_df['Grade'] == selected_grade]
        if selected_status != 'All':
            filtered_df = filtered_df[filtered_df['Status'] == selected_status]
            
        st.markdown(f"Showing **{len(filtered_df)}** of **{len(df)}** records matching active filters.")
        
        display_cols = ['Student ID', 'Name', 'Department', 'Python', 'SQL', 'C++', 'OOP', 'IOT', 'Attendance', 'Total Marks', 'Max Possible', 'Average Marks', 'Grade', 'Status']
        st.dataframe(filtered_df[display_cols], use_container_width=True)
        
        st.markdown("---")
        st.subheader("📥 Download Reports")
        
        col_dl1, col_dl2 = st.columns(2)
        
        # Complete dataset export
        csv_complete = df[display_cols].to_csv(index=False).encode('utf-8')
        col_dl1.download_button(
            label="Download Complete Processed Report (CSV)",
            data=csv_complete,
            file_name="processed_student_report.csv",
            mime="text/csv"
        )
        
        # Filtered dataset export
        csv_filtered = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
        col_dl2.download_button(
            label="Download Filtered Records Report (CSV)",
            data=csv_filtered,
            file_name="filtered_student_report.csv",
            mime="text/csv"
        )
