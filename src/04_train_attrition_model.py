import os  # for file paths
import sqlite3  # to connect to SQLite
import pandas as pd  # data handling
from sklearn.impute import SimpleImputer  # to handle missing values safely
from sklearn.model_selection import train_test_split  # split train/test
from sklearn.compose import ColumnTransformer  # preprocess different column types
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # encoding + scaling
from sklearn.pipeline import Pipeline  # combine preprocessing + model
from sklearn.linear_model import LogisticRegression  # simple baseline classifier
from sklearn.metrics import classification_report, roc_auc_score  # evaluation metrics
import joblib  # to save/load model


# Paths
DB_PATH = os.path.join("database", "hr.db")  # SQLite database file
MODEL_DIR = "models"  # folder to store trained model
MODEL_PATH = os.path.join(MODEL_DIR, "attrition_model.joblib")  # model output path

# Safety checks
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(
        "Database not found at database/hr.db. "
        "Run: python src/01_load_to_sqlite.py first."
    )

# Create models folder if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

# Load data from SQLite
conn = sqlite3.connect(DB_PATH)  # open database connection
df = pd.read_sql_query("SELECT * FROM employees", conn)  # load table into DataFrame
conn.close()  # close connection (good practice)

# Target definition (Attrition)
# Convert target to binary: Yes -> 1, No -> 0
df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})

# Drop rows with missing target (just in case)
df = df.dropna(subset=["Attrition"])


# Choose features, simpler
# These are common columns in the IBM HR dataset and useful for attrition prediction.
feature_cols = [
    "Age",
    "BusinessTravel",
    "Department",
    "DistanceFromHome",
    "Education",
    "EducationField",
    "EnvironmentSatisfaction",
    "Gender",
    "JobInvolvement",
    "JobLevel",
    "JobRole",
    "JobSatisfaction",
    "MaritalStatus",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "OverTime",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

# Keep only columns that actually exist, safe in case of changes
feature_cols = [c for c in feature_cols if c in df.columns]

# Build X and y
X = df[feature_cols].copy()  # features
y = df["Attrition"].astype(int)  # target

# Split data (train/test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identify numeric vs categorical columns
numeric_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
categorical_cols = [c for c in X.columns if c not in numeric_cols]

# Preprocessing
# Numeric: fill missing with median + scale
# Categorical: fill missing + one-hot encode
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),  # fill missing numeric values
    ("scale", StandardScaler())  # scale numeric features
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),  # fill missing categorical values
    ("onehot", OneHotEncoder(handle_unknown="ignore"))  # one-hot encode categories safely
])


preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ]
)

# Model

# Logistic Regression is simple and good baseline for attrition classification.
model = LogisticRegression(
    max_iter=2000,  # increase iterations so it converges
    class_weight="balanced"  # handle class imbalance (attrition is usually minority)
)

# Full pipeline (preprocess + model)

clf = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", model)
])

# Train

clf.fit(X_train, y_train)

# Evaluate

y_pred = clf.predict(X_test)  # predicted labels (0/1)
y_proba = clf.predict_proba(X_test)[:, 1]  # probability of Attrition=1

print("\n=== Model Evaluation (Test Set) ===")
print(classification_report(y_test, y_pred))

try:
    auc = roc_auc_score(y_test, y_proba)
    print("ROC-AUC:", round(auc, 4))
except Exception:
    print("ROC-AUC could not be computed (check class distribution).")


# Save model + feature list

# Save as a dictionary so we keep feature_cols with the model
artifact = {
    "model": clf,
    "feature_cols": feature_cols
}

joblib.dump(artifact, MODEL_PATH)
print(f" Model saved to: {MODEL_PATH}")
