import pandas as pd
import os

data_folder = "data/ckc_mapped"

for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        print("\n==============================")
        print(f"File: {filename}")
        print("==============================")

        file_path = os.path.join(data_folder, filename)

        df = pd.read_csv(file_path, usecols=["CKC_Stage"])

        print(df["CKC_Stage"].value_counts())