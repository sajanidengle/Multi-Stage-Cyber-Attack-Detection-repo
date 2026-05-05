import pandas as pd
import numpy as np
import os
import glob

raw_folder = "data/raw"
output_folder = "data/base_clean"

os.makedirs(output_folder, exist_ok=True)

files = glob.glob(os.path.join(raw_folder, "*.csv"))

for file in files:
    print(f"\nProcessing {file}...")

    df = pd.read_csv(file, low_memory=False)

    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        print("Label column missing — skipping.")
        continue

    # Clean Label formatting
    df["Label"] = df["Label"].astype(str).str.strip()

    # Remove duplicate header rows
    df = df[df["Label"] != "Label"]

    # Drop identifier columns
    drop_cols = ["Flow ID", "Src IP", "Dst IP", "Src Port", "Timestamp"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Convert all numeric columns safely
    for col in df.columns:
        if col != "Label":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace infinities using numpy (stable method)
    df = df.replace([np.inf, -np.inf], np.nan)

    # Drop rows with NaN
    df = df.dropna()

    filename = os.path.basename(file)
    output_path = os.path.join(output_folder, f"cleaned_{filename}")
    df.to_csv(output_path, index=False)

    print(f"Saved cleaned file: cleaned_{filename}")

print("\nAll files cleaned successfully.")