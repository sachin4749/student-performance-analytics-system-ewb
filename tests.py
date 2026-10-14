import unittest
import pandas as pd
import numpy as np
import analytics

class TestPerformanceAnalytics(unittest.TestCase):
    
    def setUp(self):
        # Create sample valid dataframe
        self.valid_data = pd.DataFrame({
            'Student ID': ['S001', 'S002', 'S003'],
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Department': ['CSE', 'ECE', 'CSE'],
            'Python': [90, 40, 70],
            'SQL': [85, 45, 65],
            'C++': [80, 50, 60],
            'OOP': [95, 35, 75],
            'IOT': [88, 48, 72],
            'Attendance': [90.0, 55.0, 80.0]
        })

    def test_validate_columns_success(self):
        missing = analytics.validate_columns(self.valid_data)
        self.assertEqual(len(missing), 0)

    def test_validate_columns_missing(self):
        incomplete_df = self.valid_data.drop(columns=['Python'])
        missing = analytics.validate_columns(incomplete_df)
        self.assertIn('Python', missing)

    def test_clean_and_process_calculations(self):
        processed, report = analytics.clean_and_process_data(self.valid_data)
        
        # Check Alice's total marks (90+85+80+95+88 = 438)
        alice_row = processed[processed['Student ID'] == 'S001'].iloc[0]
        self.assertEqual(alice_row['Total Marks'], 438)
        self.assertEqual(alice_row['Average Marks'], 43.8 * 10 / 5 if False else 438/5)
        self.assertEqual(alice_row['Grade'], 'A') # 87.6 >= 75 and < 85 -> A
        self.assertEqual(alice_row['Status'], 'Pass') # Avg 87.6 >= 45 and Att 90 >= 60

    def test_pass_fail_conditions(self):
        # Bob: Avg = (40+45+50+35+48)/5 = 43.6 (<45) and Att = 55.0 (<60) -> Fail
        # Charlie: Avg = (70+65+60+75+72)/5 = 68.4 (>=45) and Att = 80.0 (>=60) -> Pass
        processed, report = analytics.clean_and_process_data(self.valid_data)
        
        bob_status = processed[processed['Student ID'] == 'S002']['Status'].values[0]
        charlie_status = processed[processed['Student ID'] == 'S003']['Status'].values[0]
        
        self.assertEqual(bob_status, 'Fail')
        self.assertEqual(charlie_status, 'Pass')

    def test_missing_value_imputation(self):
        df_with_nan = self.valid_data.copy()
        df_with_nan.loc[0, 'Python'] = np.nan
        df_with_nan.loc[1, 'Attendance'] = np.nan
        
        processed, report = analytics.clean_and_process_data(df_with_nan)
        self.assertFalse(processed['Python'].isnull().any())
        self.assertFalse(processed['Attendance'].isnull().any())
        self.assertTrue(len(report['imputation_log']) > 0)

    def test_empty_dataset(self):
        empty_df = pd.DataFrame(columns=analytics.REQUIRED_COLUMNS)
        processed, report = analytics.clean_and_process_data(empty_df)
        self.assertEqual(len(processed), 0)
        kpis = analytics.get_summary_kpis(processed)
        self.assertEqual(kpis['total_students'], 0)
        self.assertEqual(kpis['class_average'], 0.0)

    def test_grade_boundaries(self):
        # Test grading logic directly via sample records
        test_df = pd.DataFrame({
            'Student ID': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
            'Name': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'],
            'Department': ['CSE']*6,
            'Python': [90, 80, 70, 60, 50, 40],
            'SQL': [90, 80, 70, 60, 50, 40],
            'C++': [90, 80, 70, 60, 50, 40],
            'OOP': [90, 80, 70, 60, 50, 40],
            'IOT': [90, 80, 70, 60, 50, 40],
            'Attendance': [90, 90, 90, 90, 90, 90]
        })
        processed, _ = analytics.clean_and_process_data(test_df)
        grades = processed['Grade'].tolist()
        self.assertEqual(grades, ['A+', 'A', 'B+', 'B', 'C', 'F'])

if __name__ == '__main__':
    unittest.main()
