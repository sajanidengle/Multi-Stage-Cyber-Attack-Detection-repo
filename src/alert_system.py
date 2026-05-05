import pandas as pd

df = pd.read_csv("data/final_ckc_dataset.csv")

print("\n--- ALERT SYSTEM OUTPUT ---\n")

for i, row in df.sample(20).iterrows():
    stage = row["CKC_Stage"]

    if stage != "Benign":
        print(f"🚨 ALERT: {stage} activity detected at flow {i}")