import os  # for file paths
import sqlite3  # for SQLite operations
import pandas as pd  # for query results as DataFrames

DB_PATH = os.path.join("database", "hr.db")  # database path


def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """Run a SELECT query and return results as a DataFrame."""
    conn = sqlite3.connect(DB_PATH)  # connect to DB
    df = pd.read_sql_query(query, conn, params=params)  # execute query
    conn.close()  # close connection
    return df  # return results


# 1) Total employees
print(run_query("SELECT COUNT(*) AS total_employees FROM employees;"))

# 2) Employees per department
print(
    run_query(
        """
        SELECT Department, COUNT(*) AS employee_count
        FROM employees
        GROUP BY Department
        ORDER BY employee_count DESC;
        """
    )
)

# 3) Average monthly income per job role
print(
    run_query(
        """
        SELECT JobRole, ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income
        FROM employees
        GROUP BY JobRole
        ORDER BY avg_monthly_income DESC;
        """
    )
)

# 4) Top 5 employees by performance (and income as tie-break)
print(
    run_query(
        """
        SELECT EmployeeNumber, Department, JobRole, PerformanceRating, MonthlyIncome
        FROM employees
        ORDER BY PerformanceRating DESC, MonthlyIncome DESC
        LIMIT 5;
        """
    )
)

# 5) Department with the best average performance
print(
    run_query(
        """
        SELECT Department, ROUND(AVG(PerformanceRating), 3) AS avg_perf
        FROM employees
        GROUP BY Department
        ORDER BY avg_perf DESC
        LIMIT 1;
        """
    )
)

# 6) (Business) Attrition rate by OverTime
print(
    run_query(
        """
        SELECT OverTime,
               ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
               COUNT(*) AS n_employees
        FROM employees
        GROUP BY OverTime
        ORDER BY attrition_rate_pct DESC;
        """
    )
)

# 7) (Business) Attrition rate by JobSatisfaction
print(
    run_query(
        """
        SELECT JobSatisfaction,
               ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS attrition_rate_pct,
               COUNT(*) AS n_employees
        FROM employees
        GROUP BY JobSatisfaction
        ORDER BY JobSatisfaction ASC;
        """
    )
)
