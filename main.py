import pandas as pd
import numpy as np
import os

def load_and_clean_data(file_path):
    """Loads dataset and applies robust data cleaning and missing-value imputation."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: '{file_path}' not found in directory.")
        
        df = pd.read_csv(file_path)
        
        # Define academic subjects
        subjects = ['Python', 'SQL', 'C++', 'OOP', 'IOT']
        
        # Convert to numeric, forcing errors to NaN
        for col in subjects + ['Attendance']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Impute missing marks with subject median and attendance with mean
        for col in subjects:
            df[col].fillna(df[col].median(), inplace=True)
        df['Attendance'].fillna(df['Attendance'].mean(), inplace=True)
        
        print("[INFO] Dataset successfully loaded and cleaned.")
        return df, subjects
    except Exception as e:
        print(f"[ERROR] Failed to process dataset: {e}")
        exit(1)

def compute_analytics(df, subjects):
    """Computes total, average, grades, pass/status using Pandas & NumPy vectorization."""
    # NumPy matrix calculations for marks
    marks_matrix = df[subjects].to_numpy()
    
    df['Total Marks'] = np.sum(marks_matrix, axis=1)
    df['Max Possible'] = len(subjects) * 100
    df['Average Marks'] = np.mean(marks_matrix, axis=1)
    
    # Grading Rule Function
    def assign_grade(avg):
        if avg >= 85: return 'A+'
        elif avg >= 75: return 'A'
        elif avg >= 65: return 'B+'
        elif avg >= 55: return 'B'
        elif avg >= 45: return 'C'
        else: return 'F'

    df['Grade'] = df['Average Marks'].apply(assign_grade)
    
    # Pass/Fail Condition: Average >= 45 and Attendance >= 60%
    df['Status'] = np.where((df['Average Marks'] >= 45) & (df['Attendance'] >= 60), 'PASS', 'FAIL')
    
    return df

def display_dashboard(df, subjects):
    """Displays a clean interactive terminal dashboard with advanced analytical insights."""
    while True:
        print("\n" + "="*70)
        print("          BTECH STUDENT PERFORMANCE ANALYTICS SYSTEM          ")
        print("="*70)
        print("1. View Overall Class Summary & Statistics")
        print("2. View Subject-Wise Performance Breakdown")
        print("3. View Department-Wise Analytics")
        print("4. View Top 5 Performing Students")
        print("5. Search Student by Name or ID")
        print("6. Export Processed Report to CSV")
        print("7. Exit System")
        print("="*70)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\n--- OVERALL CLASS SUMMARY ---")
            print(f"Total Students Evaluated : {len(df)}")
            print(f"Overall Class Average    : {df['Average Marks'].mean():.2f}%")
            print(f"Highest Average Score    : {df['Average Marks'].max():.2f}%")
            print(f"Lowest Average Score     : {df['Average Marks'].min():.2f}%")
            passed = (df['Status'] == 'PASS').sum()
            failed = (df['Status'] == 'FAIL').sum()
            print(f"Passed Students          : {passed} ({passed/len(df)*100:.1f}%)")
            print(f"Failed Students          : {failed} ({failed/len(df)*100:.1f}%)")
            print("\nGrade Distribution:")
            print(df['Grade'].value_counts().sort_index().to_string())
            
        elif choice == '2':
            print("\n--- SUBJECT-WISE PERFORMANCE ANALYSIS ---")
            for sub in subjects:
                mean_val = df[sub].mean()
                max_val = df[sub].max()
                min_val = df[sub].min()
                print(f"• {sub:8s} -> Avg: {mean_val:.2f} | Max: {max_val} | Min: {min_val}")
                
        elif choice == '3':
            print("\n--- DEPARTMENT-WISE ANALYTICS ---")
            dept_grouped = df.groupby('Department')['Average Marks'].agg(['count', 'mean', 'max', 'min']).reset_index()
            dept_grouped.columns = ['Department', 'Total Students', 'Avg Score', 'Max Score', 'Min Score']
            print(dept_grouped.to_string(index=False))
            
        elif choice == '4':
            print("\n--- TOP 5 PERFORMING STUDENTS ---")
            top_5 = df.nlargest(5, 'Average Marks')[['Student ID', 'Name', 'Department', 'Average Marks', 'Grade', 'Status']]
            print(top_5.to_string(index=False))
            
        elif choice == '5':
            query = input("\nEnter Student Name or ID to search: ").strip().lower()
            result = df[df['Name'].str.lower().str.contains(query) | df['Student ID'].astype(str).str.contains(query)]
            if not result.empty:
                print(f"\nFound {len(result)} matching record(s):")
                print(result[['Student ID', 'Name', 'Department', 'Average Marks', 'Grade', 'Status']].to_string(index=False))
            else:
                print("\n[RESULT] No matching student found.")
                
        elif choice == '6':
            export_path = "processed_student_report.csv"
            df.to_csv(export_path, index=False)
            print(f"\n[SUCCESS] Report exported successfully as '{export_path}'.")
            
        elif choice == '7':
            print("\nExiting system. Thank you!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 7.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    file_name = "students.csv"
    raw_df, subjects = load_and_clean_data(file_name)
    processed_df = compute_analytics(raw_df, subjects)
    display_dashboard(processed_df, subjects)
