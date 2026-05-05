import pandas as pd
import os

processed_folder = "data/processed"

for filename in os.listdir(processed_folder):
    if filename.startswith("ckc_labeled") and filename.endswith(".csv"):
        print(f"\n=== {filename} ===")
        
        df = pd.read_csv(os.path.join(processed_folder, filename))
        
        print(df['CKC_Stage'].value_counts())