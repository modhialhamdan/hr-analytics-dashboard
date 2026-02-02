
import os
import sqlite3
import pandas as pd

#  Configuration

DB_PATH = os.path.join("database", "hr.db")

def run_sql(query: str) -> pd.DataFrame:
    """Execute a SQL SELECT query and return results as a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df_out = pd.read_sql_query(query, conn)
    conn.close()
    return df_out


# Load data from SQLite
print("Loading data from SQLite ")

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(
        "Database not found. Please run:\n"
        "python src/01_load_to_sqlite.py"
    )

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM employees", conn)
conn.close()

print("Data loaded successfully ✅")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# Basic EDA

print("\nBasic EDA ")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values (top 10):")
missing = df.isna().mean().sort_values(ascending=False) * 100
print(missing.head(10))

print("\nDuplicate rows:", df.duplicated().sum())

#Questions – Pandas

print("\nQuestions (Pandas) ")

# Total number of employees
print("\nTotal number of employees")
total_employees = len(df)
print("Answer:", total_employees)

#Employee count per department
print("\nEmployee count per department")
dept_counts = df["Department"].value_counts()
print(dept_counts)

# Average monthly income by job role
print("\nAverage monthly income by job role")
df["MonthlyIncome"] = pd.to_numeric(df["MonthlyIncome"], errors="coerce")
avg_income_role = (
    df.groupby("JobRole")["MonthlyIncome"]
    .mean()
    .sort_values(ascending=False)
)
print(avg_income_role)

# Top 5 employees by performance rating
print("\nTop 5 employees by performance rating")
df["PerformanceRating"] = pd.to_numeric(df["PerformanceRating"], errors="coerce")
top5_perf = (
    df.sort_values(
        ["PerformanceRating", "MonthlyIncome"],
        ascending=[False, False]
    )
    .head(5)[
        ["EmployeeNumber", "Department", "JobRole",
         "PerformanceRating", "MonthlyIncome"]
    ]
)
print(top5_perf)

# Department with highest average performance rating
print("\nDepartment with highest average performance rating")
avg_perf_dept = (
    df.groupby("Department")["PerformanceRating"]
    .mean()
    .sort_values(ascending=False)
)
print(avg_perf_dept)

#  Questions – SQL
print("\nQuestions (SQL)")

#Total employees (SQL)
print("\n(SQL): Total employees")
print(run_sql("""
SELECT COUNT(*) AS total_employees
FROM employees;
"""))

# Employees per department (SQL)
print("\n(SQL): Employees per department")
print(run_sql("""
SELECT Department, COUNT(*) AS employee_count
FROM employees
GROUP BY Department
ORDER BY employee_count DESC;
"""))

# Average monthly income per job role (SQL)
print("\n(SQL): Average monthly income per job role")
print(run_sql("""
SELECT JobRole,
       ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income
FROM employees
GROUP BY JobRole
ORDER BY avg_monthly_income DESC;
"""))

# Top 5 employees by performance rating (SQL)
print("\n(SQL): Top 5 employees by performance rating")
print(run_sql("""
SELECT EmployeeNumber, Department, JobRole,
       PerformanceRating, MonthlyIncome
FROM employees
ORDER BY PerformanceRating DESC, MonthlyIncome DESC
LIMIT 5;
"""))

# Department with highest avg performance (SQL)
print("\n(SQL): Best performing department")
print(run_sql("""
SELECT Department,
       ROUND(AVG(PerformanceRating), 3) AS avg_perf
FROM employees
GROUP BY Department
ORDER BY avg_perf DESC
LIMIT 1;
"""))

#  Business Questions

print("\nBusiness-HR Info ")

# Attrition rate by department
print("\nAttrition rate by department")
print(run_sql("""
SELECT Department,
       ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2)
           AS attrition_rate_pct,
       COUNT(*) AS n_employees
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;
"""))

# Overtime vs attrition
print("\nAttrition rate by overtime")
print(run_sql("""
SELECT OverTime,
       ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2)
           AS attrition_rate_pct,
       COUNT(*) AS n_employees
FROM employees
GROUP BY OverTime
ORDER BY attrition_rate_pct DESC;
"""))

# Job satisfaction vs attrition
print("\nAttrition rate by job satisfaction")
print(run_sql("""
SELECT JobSatisfaction,
       ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2)
           AS attrition_rate_pct,
       COUNT(*) AS n_employees
FROM employees
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction ASC;
"""))

# Final Insights

print("\nInsights")

print("""
1. Employees who work overtime show a noticeably higher attrition rate.
2. Lower job satisfaction levels are strongly associated with higher attrition.
3. High performance does not always correspond to the highest income.
4. Some departments combine high headcount with higher attrition risk,
   indicating a need for targeted retention strategies.
5. SQLite proved effective as a lightweight backend for analytics and data management.
""")

