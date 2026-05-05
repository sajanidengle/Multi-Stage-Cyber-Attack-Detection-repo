import pandas as pd
import joblib

# Load model (if you saved it, else skip probability part)
# model = joblib.load("models/rf_model.pkl")

df = pd.read_csv("data/final_ckc_dataset.csv")

print("\n--- ADVANCED ALERT SYSTEM ---\n")

# Define severity levels
severity_map = {
    "Reconnaissance": "Low",
    "Exploitation": "High",
    "Installation": "High",
    "Command_and_Control": "Critical",
    "Actions_on_Objectives": "Critical"
}

for i, row in df.sample(20).iterrows():
    stage = row["CKC_Stage"]

    if stage != "Benign":
        severity = severity_map.get(stage, "Medium")

        print(f"""
🚨 ALERT TRIGGERED
------------------------
Flow ID   : {i}
Stage     : {stage}
Severity  : {severity}
------------------------
""")