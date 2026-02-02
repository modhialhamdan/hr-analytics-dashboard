import pandas as pd
import joblib

# Paths
MODEL_PATH = "models/attrition_model.joblib"
DATA_PATH = "data/HR-Employee-Attrition.csv"

# Load trained model package
package = joblib.load(MODEL_PATH)

model = package["model"]              # trained pipeline
feature_cols = package["feature_cols"]  # columns used in training

print("Model loaded successfully.")

# Load dataset
df = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully.")


# Select features
X = df[feature_cols]

# Run predictions
pred = model.predict(X)
proba = model.predict_proba(X)[:, 1]


# Combine results
results = df.copy()
results["Attrition_Prediction"] = pred
results["Attrition_Probability"] = proba

# Show sample output
print("\nSample Predictions:\n")
print(
    results[
        [
            "Age",
            "Department",
            "JobRole",
            "MonthlyIncome",
            "Attrition_Prediction",
            "Attrition_Probability",
        ]
    ].head(10)
)


# Save results
#OUTPUT_PATH = "data/attrition_predictions.csv"
#results.to_csv(OUTPUT_PATH, index=False)

#print(f"\nPredictions saved to: {OUTPUT_PATH}")
