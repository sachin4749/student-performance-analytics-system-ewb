# Performance Analytics System

A professional, browser-accessible BTech Student Performance Analytics web application built with Python, Streamlit, Pandas, NumPy, and Plotly.

## Features
- **Overview Dashboard:** Class KPIs, grade distribution, pass/fail proportions, and department averages.
- **Subject-Wise Analytics:** Average, highest, lowest marks, and comparative subject distributions.
- **Department Analytics:** Department-wise student counts, average scores, and pass rates.
- **Top 5 Performers:** Ranked student leaderboard with tie-breaking rules.
- **Student Search:** Case-insensitive partial name and ID search.
- **Records Explorer & Export:** Interactive filtering by department, grade, and status with CSV report downloads.
- **Data Quality & Imputation:** Automatic handling of missing values, median imputation for marks, mean imputation for attendance, and out-of-range validation.

---

## Project Structure
```text
performance-analytics-system/
├── app.py
├── analytics.py
├── tests.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample_data/
    └── students.csv
```

---

## Local Installation & Running

1. **Clone or download the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run tests:**
   ```bash
   python tests.py
   ```
4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

---

## Deployment on Streamlit Community Cloud

1. Push your repository to **GitHub**.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your GitHub repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy**!
