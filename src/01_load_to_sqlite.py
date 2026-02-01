# src/01_load_to_sqlite.py

import os  # for file paths and folder creation
import sqlite3  # for SQLite database operations
import pandas as pd  # for reading and processing CSV data

# Hard-coded paths (simple)

CSV_PATH = os.path.join("data", "HR-Employee-Attrition.csv")  # path to the dataset CSV
DB_PATH = os.path.join("database", "hr.db")  # path to the SQLite database file

# Ensure the database folder exists

os.makedirs("database", exist_ok=True)  # create database/ folder if it does not exist

# Basic sanity checks

if not os.path.exists(CSV_PATH):  # check if the CSV exists
    raise FileNotFoundError(f"CSV not found at: {CSV_PATH}")  # stop with a clear error


# Load CSV into a DataFrame

df = pd.read_csv(CSV_PATH)  # read the CSV file


# Minimal cleaning 
# Drop columns that are usually constant in this dataset (optional but tidy)
columns_to_drop = []  # list of columns to drop if present
if "Over18" in df.columns:  # check column existence
    columns_to_drop.append("Over18")  # mark for drop
if "StandardHours" in df.columns:  # check column existence
    columns_to_drop.append("StandardHours")  # mark for drop

df = df.drop(columns=columns_to_drop, errors="ignore")  # drop safely without crashing
df = df.drop_duplicates()  # remove duplicates if any


# Write DataFrame to SQLite

conn = sqlite3.connect(DB_PATH)  # connect (creates db if missing)

# Replace the table each run (simple and safe for development)
df.to_sql("employees", conn, if_exists="replace", index=False)  # write to employees table


# Adding a few indexes 
with conn:  # auto-commit block
    if "Department" in df.columns:  # if column exists
        conn.execute("CREATE INDEX IF NOT EXISTS idx_department ON employees(Department);")  # speed up dept queries
    if "JobRole" in df.columns:  # if column exists
        conn.execute("CREATE INDEX IF NOT EXISTS idx_jobrole ON employees(JobRole);")  # speed up role queries
    if "EmployeeNumber" in df.columns:  # if column exists
        conn.execute("CREATE INDEX IF NOT EXISTS idx_empnum ON employees(EmployeeNumber);")  # speed up lookups

conn.close()  # close database connection


# Success message

print(f"✅ Loaded {len(df)} rows into SQLite at: {DB_PATH}")  # confirm success
