import os  # for working with file paths
import sqlite3  # for connecting to SQLite database
import pandas as pd  # for data handling and analysis
import streamlit as st  # for building the interactive dashboard
import plotly.express as px  # for simple interactive charts
import joblib  # to load the trained model

# Page Configuration (Streamlit)

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


DB_PATH = os.path.join("database", "hr.db")  # points to database/hr.db

#connect to DB

def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)  # allow reuse in Streamlit


#load data from SQLite

@st.cache_data  # cache the dataframe so the app feels faster
def load_employees() -> pd.DataFrame:
    """Load employees table from SQLite into a DataFrame."""
    conn = get_connection()  # open connection
    df = pd.read_sql_query("SELECT * FROM employees", conn)  # read all rows
    conn.close()  # close connection
    return df  # return dataframe


# run SQL safely

def execute_sql(query: str, params: tuple = ()) -> None:
    """Execute INSERT/UPDATE/DELETE queries."""
    conn = get_connection()  # open connection
    cur = conn.cursor()  # create cursor
    cur.execute(query, params)  # execute query with parameters
    conn.commit()  # save changes
    conn.close()  # close connection


# Title + Quick instructions

st.title("📊 Interactive HR Analytics Dashboard")  # main title

st.caption(
    "Data source: IBM HR Analytics dataset (employees table in SQLite). "
    "This dashboard supports basic analytics + adding/updating employees."
)

# Validate DB exists

if not os.path.exists(DB_PATH):  # check if database file exists
    st.error(
        "Database not found at 'database/hr.db'. "
        "Run your loader script first to create the database."
    )
    st.stop()  # stop the app here


# Load data

df = load_employees()  # load employees dataframe


# Basic validation: table not empty

if df.empty:  # if no rows exist
    st.warning("The employees table is empty. Please load data into SQLite first.")
    st.stop()  # stop the app here


# Tabs
tab_dashboard, tab_add, tab_update = st.tabs(
    ["Dashboard", "Add Employee", "Update Employee"]
)


# Dashboard Tab

with tab_dashboard:  # dashboard tab start

    # Sidebar filters 
    st.sidebar.header("Filters")  # sidebar title

    # Department filter options (handle missing column safely)
    if "Department" in df.columns:  # if Department exists
        dept_options = ["All"] + sorted(df["Department"].dropna().unique().tolist())  # build dropdown list
    else:
        dept_options = ["All"]  # fallback if missing

    selected_department = st.sidebar.selectbox(
        "Department",
        options=dept_options,
        index=0
    )

    # Apply filter to create "df_view"
    df_view = df.copy()  # make a copy for filtered view

    if selected_department != "All" and "Department" in df_view.columns:  # if user chose a department
        df_view = df_view[df_view["Department"] == selected_department]  # filter rows


    # KPI Section (Top)

    st.subheader("Key Metrics")  # section header

    # Create columns for KPI cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)  # 4 KPI cards in one row

    # Total employees in the filtered view
    total_employees = len(df_view)  # count rows

    # Average monthly income (if column exists)
    if "MonthlyIncome" in df_view.columns:  # check column
        avg_income = float(pd.to_numeric(df_view["MonthlyIncome"], errors="coerce").dropna().mean())  # compute mean safely
    else:
        avg_income = float("nan")  # fallback

    # Average performance rating (if column exists)
    if "PerformanceRating" in df_view.columns:  # check column
        avg_perf = float(pd.to_numeric(df_view["PerformanceRating"], errors="coerce").dropna().mean())  # compute mean safely
    else:
        avg_perf = float("nan")  # fallback

    # Attrition rate (if Attrition exists and uses Yes/No)
    if "Attrition" in df_view.columns:  # check column
        attrition_rate = (df_view["Attrition"].eq("Yes").mean()) * 100.0  # percent
    else:
        attrition_rate = float("nan")  # fallback

    # Display KPI metrics
    kpi1.metric("Total Employees", f"{total_employees}")  # KPI 1
    kpi2.metric("Avg Monthly Income", f"{avg_income:,.0f}" if pd.notna(avg_income) else "N/A")  # KPI 2
    kpi3.metric("Avg Performance", f"{avg_perf:.2f}" if pd.notna(avg_perf) else "N/A")  # KPI 3
    kpi4.metric("Attrition Rate", f"{attrition_rate:.2f}%" if pd.notna(attrition_rate) else "N/A")  # KPI 4


    # Visuals 
    st.subheader("Visual Analytics")  # section header

    col_left, col_right = st.columns(2)  # split area into two columns

    # ---- Chart 1: Employee count by Department (bar)
    with col_left:  # left column
        st.markdown("**1) Employee Count by Department**")  # chart title
        if "Department" in df.columns:  # use full df (not filtered) to see overall distribution
            dept_counts = df.groupby("Department").size().reset_index(name="count")  # group + count
            #fig1 = px.bar(dept_counts, x="Department", y="count")  # bar chart
            fig1 = px.bar(
            dept_counts,
            x="Department",
            y="count",
            color_discrete_sequence=["#C77DFF"]  # Purple
            )

            st.plotly_chart(fig1, use_container_width=True)  # display chart
        else:
            st.info("Column 'Department' not found in data.")  # fallback message

    # ---- Chart 2: Average Monthly Income by JobRole (bar)
    with col_right:  # right column
        st.markdown("**2) Avg Monthly Income by Job Role (Filtered)**")  # chart title
        if "JobRole" in df_view.columns and "MonthlyIncome" in df_view.columns:  # check columns
            temp = df_view.copy()  # copy
            temp["MonthlyIncome"] = pd.to_numeric(temp["MonthlyIncome"], errors="coerce")  # ensure numeric
            avg_by_role = temp.groupby("JobRole")["MonthlyIncome"].mean().reset_index()  # compute mean
            avg_by_role = avg_by_role.sort_values("MonthlyIncome", ascending=False)  # sort
            #fig2 = px.bar(avg_by_role, x="JobRole", y="MonthlyIncome")  # bar chart
            fig2 = px.bar(
            avg_by_role,
            x="JobRole",
            y="MonthlyIncome",
            color_discrete_sequence=["#C74968"]  # Pink
            )

            st.plotly_chart(fig2, use_container_width=True)  # display chart
        else:
            st.info("Columns 'JobRole' and/or 'MonthlyIncome' not found.")  # fallback message

    # Create another row for charts
    col3, col4 = st.columns(2)  # two columns again

    # ---- Chart 3: Attrition distribution (pie)
    with col3:  # left column
        st.markdown("**3) Attrition Distribution **")  # chart title
        if "Attrition" in df_view.columns:  # check column
            attr_counts = df_view["Attrition"].fillna("Unknown").value_counts().reset_index()  # counts
            attr_counts.columns = ["Attrition", "count"]  # rename columns
            #fig3 = px.pie(attr_counts, names="Attrition", values="count")  # pie chart
            fig3 = px.pie(
            attr_counts,
            names="Attrition",
            values="count",
            color_discrete_sequence=["#C77DFF", "#C74968"]
            )

            st.plotly_chart(fig3, use_container_width=True)  # display chart
        else:
            st.info("Column 'Attrition' not found.")  # fallback message

    # ---- Chart 4: Income distribution by Department (box)
    with col4:  # right column
        st.markdown("**4) Income Distribution by Department **")  # chart title
        if "Department" in df_view.columns and "MonthlyIncome" in df_view.columns:  # check columns
            temp2 = df_view.copy()  # copy
            temp2["MonthlyIncome"] = pd.to_numeric(temp2["MonthlyIncome"], errors="coerce")  # ensure numeric
            #fig4 = px.box(temp2.dropna(subset=["MonthlyIncome"]), x="Department", y="MonthlyIncome")  # box plot
            fig4 = px.box(
            temp2.dropna(subset=["MonthlyIncome"]),
            x="Department",
            y="MonthlyIncome",
            color_discrete_sequence=["#E0AAFF"]
            )

            st.plotly_chart(fig4, use_container_width=True)  # display chart
        else:
            st.info("Columns 'Department' and/or 'MonthlyIncome' not found.")  # fallback message


    # Data Table 

    st.subheader("Employee Table ")  # section header

    # Pick a small set of columns to display (simple + readable)
    preferred_cols = [
        "EmployeeNumber",
        "Department",
        "JobRole",
        "MonthlyIncome",
        "PerformanceRating",
        "Attrition",
        "Age",
        "Gender",
        "OverTime",
        "JobSatisfaction",
    ]

    # Keep only columns that actually exist in df_view
    display_cols = [c for c in preferred_cols if c in df_view.columns]  # filter columns

    # Show the dataframe table
    st.dataframe(df_view[display_cols] if display_cols else df_view, use_container_width=True)  # display


# Add Employee Tab

with tab_add:  # add employee tab start

    # CRUD Section: Add + Update
    st.subheader("Database Actions")  # section header

    center_col = st.columns([1, 2, 1])[1]  # center column

    # Action 1: Add new employee 
    with center_col:  # left action panel
        st.markdown("### ➕ Add New Employee")  # panel title

        st.caption(
            "This inserts a new row using a small subset of columns. "
            "Other columns will be NULL in SQLite (which is fine for this task)."
        )

        with st.form("add_employee_form", clear_on_submit=True):  # start a Streamlit form
            # Input fields (simple)
            new_emp_num = st.number_input("EmployeeNumber", min_value=1, step=1)  # numeric ID
            new_dept = st.text_input("Department", value="Sales")  # department text
            new_role = st.text_input("JobRole", value="Sales Executive")  # job role text
            new_income = st.number_input("MonthlyIncome", min_value=0, step=100)  # income numeric
            new_perf = st.number_input("PerformanceRating", min_value=1, max_value=5, step=1)  # rating
            new_attr = st.selectbox("Attrition", options=["No", "Yes"])  # yes/no
            new_age = st.number_input("Age", min_value=18, max_value=70, step=1, value=30)  # age
            new_gender = st.selectbox("Gender", options=["Male", "Female"])  # gender
            new_overtime = st.selectbox("OverTime", options=["No", "Yes"])  # overtime
            new_jobsat = st.number_input("JobSatisfaction", min_value=1, max_value=4, step=1, value=3)  # satisfaction

            submitted_add = st.form_submit_button("Add Employee")  # submit button

            if submitted_add:  # when user submits
                # Check if EmployeeNumber column exists (we use it as identifier)
                if "EmployeeNumber" not in df.columns:  # validate column exists in table
                    st.error("Cannot add: 'EmployeeNumber' column not found in employees table.")  # error
                else:
                    # Check for duplicates (simple validation)
                    existing = df[df["EmployeeNumber"] == int(new_emp_num)]  # filter existing
                    if len(existing) > 0:  # if duplicate found
                        st.error("EmployeeNumber already exists. Please choose a different number.")  # show error
                    else:
                        # Build an INSERT query using only a subset of columns (hard-coded)
                        insert_query = """
                        INSERT INTO employees
                        (EmployeeNumber, Department, JobRole, MonthlyIncome, PerformanceRating, Attrition, Age, Gender, OverTime, JobSatisfaction)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        """  # SQL insert statement

                        params = (
                            int(new_emp_num),  # EmployeeNumber
                            str(new_dept),  # Department
                            str(new_role),  # JobRole
                            int(new_income),  # MonthlyIncome
                            int(new_perf),  # PerformanceRating
                            str(new_attr),  # Attrition
                            int(new_age),  # Age
                            str(new_gender),  # Gender
                            str(new_overtime),  # OverTime
                            int(new_jobsat),  # JobSatisfaction
                        )  # query parameters

                        execute_sql(insert_query, params)  # insert row into DB

                        st.success(" Employee added successfully!")  # success message
                        st.cache_data.clear()  # clear cache so fresh data loads
                        st.rerun()  # rerun app to refresh


# Update Employee Tab

with tab_update:  # update employee tab start

    # CRUD Section: Add + Update
    st.subheader("Database Actions")  # section header

    center_col = st.columns([1, 2, 1])[1]  # center column

    # Action 2: Update an employee's income

    with center_col:  # right action panel
        st.markdown("### ✏️ Update Monthly Income")  # panel title

        st.caption("Select an existing EmployeeNumber and update MonthlyIncome in the database.")

        # Ensure EmployeeNumber exists
        if "EmployeeNumber" not in df.columns:  # validate column exists
            st.error("Cannot update: 'EmployeeNumber' column not found in employees table.")  # error
        else:
            # Create a dropdown of existing employee numbers (simple)
            emp_nums = sorted(pd.to_numeric(df["EmployeeNumber"], errors="coerce").dropna().astype(int).unique().tolist())  # list of IDs

            # Let user pick employee
            selected_emp = st.selectbox("Choose EmployeeNumber", options=emp_nums)  # dropdown

            # Let user type new income
            updated_income = st.number_input("New MonthlyIncome", min_value=0, step=100)  # input income

            # Update button
            if st.button("Update Income"):  # button click
                update_query = """
                UPDATE employees
                SET MonthlyIncome = ?
                WHERE EmployeeNumber = ?;
                """  # SQL update statement

                execute_sql(update_query, (int(updated_income), int(selected_emp)))  # run update

                st.success(" MonthlyIncome updated successfully!")  # success message
                st.cache_data.clear()  # clear cache so refreshed data loads
                st.rerun()  # rerun app
