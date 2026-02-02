# HR Analytics Dashboard

This project is an HR analytics interactive dashboard  built using Python, SQLite, and Streamlit.

The idea is simple:
- Taking an HR dataset (IBM HR Analytics)
- Storing it in a SQLite database
- Analyzing it using Python and SQL
- Visualizing the results in an interactive dashboard
- Predicting attrition of employees using Machine Learning

Focuses on understanding employee data and answering practical HR questions related to performance, income, and attrition.



## Tools 
- Python 3.11
- Pandas
- SQLite
- Streamlit
- Plotly
- scikit-learn
- joblib

## Project Structure

```
hr-analytics-dashboard/
│
├── app.py                      # Main Streamlit application
│
├── src/
│   ├── load_to_sqlite.py       # Loads CSV data into SQLite
│   ├── sql_queries.py          # SQL exploration / analysis queries
│   ├── train_attrition_model.py# Trains attrition prediction model (offline)
│   ├── predict_attrition.py    # Runs predictions using saved model (CLI)
│   └── utils.py                # Helper / utility functions (if used)
│
├── database/
│   └── hr.db                   # SQLite database (employees table)
│
├── data/
│   └── HR-Employee-Attrition.csv
│
├── models/
│   └── attrition_model.joblib  # Saved ML model (optional)
│
├── screenshots/
│   ├── dashboard_main.png
│   ├── dashboard_charts.png
│   ├── add_employee.png
│   └── update_employee.png
│
└── README.md
```


## Environment Setup

### 1. Create and activate Conda environment
```bash
conda create -n hr_dashboard python=3.11
conda activate hr_dashboard
```

### 2. Install required libraries
```bash
pip install pandas streamlit plotly joblib
```

## Running the project Step by Step

Follow the steps below **in order**. Each script has a clear responsibility.

---

### Load the CSV data into SQLite

This step:
- Reads the IBM HR CSV file
- Creates the SQLite database
- Inserts all employee records into the `employees` table

```bash
python src/load_to_sqlite.py
```

Output:
- A database file will be created at:
  ```
  database/hr.db
  ```

! Run this step **once** (or again only if you want to reset the database).

---

### Run SQL analysis queries 

This step:
- Runs exploratory SQL queries
- Helps answer business questions (attrition, income, departments, etc.)
- Prints results to the terminal

```bash
python src/sql_queries.py
```

This step is optional and used mainly for **analysis / reporting**.

---

### Train the Attrition Prediction Model (offline)

This step:
- Loads data from SQLite
- Trains a machine learning model to predict employee attrition
- Saves the trained model to disk

```bash
python src/train_attrition_model.py
```

Output:
- A trained model saved at:
  ```
  models/attrition_model.joblib
  ```

This script is **not connected to Streamlit** and is run offline.

---

### Run predictions using the trained model

This step:
- Loads the saved model
- Runs predictions on sample or existing employee data
- Prints prediction results in the terminal

```bash
python src/predict_attrition.py
```

This step is optional and for **model validation only**.

---

### Launch the Streamlit Dashboard

This step:
- Starts the interactive HR Analytics dashboard
- Allows filtering, visualization, and database CRUD actions

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at:
```
http://localhost:8501
```

---

### Recommended Execution Order - Summary

```
1. load_to_sqlite.py
2. sql_queries.py        
3. train_attrition_model.py
4. predict_attrition.py 
5. app.py
```

## Dashboard Overview
### Tab 1: Dashboard
<img width="2152" height="1212" alt="image" src="https://github.com/user-attachments/assets/0eb10170-7993-4d04-bea5-2af2130f5696" />
<img width="2069" height="1084" alt="image" src="https://github.com/user-attachments/assets/c4a5c92d-d87e-4e4e-b7b2-695b5591ce92" />
<img width="2051" height="786" alt="image" src="https://github.com/user-attachments/assets/0ef2bad2-950e-455c-b44e-6ab1c94b7120" />
<img width="2018" height="819" alt="image" src="https://github.com/user-attachments/assets/c79d41b0-5c8b-424d-b4c9-5b0d4d298fd1" />
### Tab 2: 
<img width="2139" height="1210" alt="image" src="https://github.com/user-attachments/assets/391cf9dc-0c80-41a0-8a27-df4518bff5e4" />

### Tab 3:
<img width="2126" height="1217" alt="image" src="https://github.com/user-attachments/assets/d6035850-cfed-413a-a328-d1ff759ab1ca" />


## Dashboard Features

### Dashboard Tab
- Key HR metrics (headcount, income, performance, attrition rate)
- Interactive visualizations:
  - Employee count by department
  - Average income by job role
  - Attrition distribution
  - Income distribution by department
- Filter by department
- Interactive employee table

### Add Employee Tab
- Insert a new employee into the SQLite database
- Uses a controlled subset of fields
- Automatically refreshes the dashboard after insertion

### Update Employee Tab
- Update an employee’s MonthlyIncome
- Uses `EmployeeNumber` as the unique identifier
- Changes are saved directly to SQLite



## Some examples of insights extracted from the analysis:
- Employees who work overtime tend to have higher attrition rates
- Lower job satisfaction is associated with higher attrition
- High performance does not always mean higher income
- Certain departments may require focused retention strategies
- Attrition prediction can help identify at-risk employees early and support proactive HR decision-making

## Notes
- SQLite is used as a lightweight database to enable SQL-based analysis without requiring a database server
- EDA and SQL answers were implemented as a Python script instead of a notebook to avoid kernel issues and keep execution simple and reproducible
- A machine learning model was trained offline to predict employee attrition and saved for reuse
- The same database is used by both the analysis scripts and the Streamlit dashboard
  
## Author
- Modhi Alhamdan - AI Trainee









