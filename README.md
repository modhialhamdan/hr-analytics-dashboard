# HR Analytics Dashboard

This project is an HR analytics dashboard  built using Python, SQLite, and Streamlit.

The idea is simple:
- Takهing an HR dataset (IBM HR Analytics)
- Storing it in a SQLite database
- Analyzing it using Python and SQL
- Visualizing the results in an interactive dashboard

Focuses on understanding employee data and answering practical HR questions related to performance, income, and attrition.


## What does this project do?
- Loads employee data from a CSV file into a SQLite database
- Performs exploratory data analysis (EDA)
- Answers HR-related questions using:
  - Pandas
  - SQL (SQLite)
- Provides an interactive Streamlit dashboard where you can:
  - View key HR KPIs
  - Filter data by department
  - Add a new employee
  - Update an employee’s monthly income


## Tools & Technologies
- Python 3.11
- Pandas
- SQLite
- Streamlit
- Plotly


## Project Structure

hr-analytics-dashboard/

│

├── app.py

│ # Streamlit dashboard

│

├── src/

│ ├── 01_load_to_sqlite.py

│ ├── 02_sql_queries.py

│ └── 03_eda_sql_answers.py

│

├── data/

│ └── HR-Employee-Attrition.csv

│

├── database/

│ └── hr.db

│

└── README.md


Dashboard Features
- Key HR metrics (KPIs)
- Department-based filtering
- Employee distribution and income analysis
- Attrition insights

SQL-based data updates:
- Add new employee
- Update monthly income
- Key Insights

Some examples of insights extracted from the analysis:
- Employees who work overtime tend to have higher attrition rates
- Lower job satisfaction is associated with higher attrition
- High performance does not always mean higher income
- Certain departments may require focused retention strategies

Notes
- SQLite is used as a lightweight database to enable SQL-based analysis without requiring a database server
- EDA and SQL answers were implemented as a Python script instead of a notebook to avoid kernel issues and keep execution simple and reproducible

- The same database is used by both the analysis scripts and the Streamlit dashboard



