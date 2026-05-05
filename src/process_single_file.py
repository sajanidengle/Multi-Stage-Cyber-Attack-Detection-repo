import pandas as pd
import numpy as np
import gc

def map_ckc(row):
    if row['Flow Duration'] < 20 and row['Tot Fwd Pkts'] == 1 and row['Tot Bwd Pkts'] == 1:
        return 1
    elif row['Tot Fwd Pkts'] >= 20 and row['Tot Bwd Pkts'] >= 20 and row['Flow Duration'] > 300000:
        return 2
    else:
        return 0

filename = "Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv"

raw_path = f"data/raw/{filename}"
processed_path = f"data/processed/ckc_labeled_{filename}"

print(f"\nProcessing {filename}...")

df = pd.read_csv(raw_path, low_memory=False)

df.columns = df.columns.str.strip()
df.replace([np.inf, -np.inf], np.nan, inplace=True)

critical_cols = ['Flow Duration', 'Flow Byts/s', 'Flow Pkts/s']
df.dropna(subset=critical_cols, inplace=True)

df.drop_duplicates(inplace=True)
df = df[df['Flow Duration'] >= 0]

df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df.dropna(subset=['Timestamp'], inplace=True)
df.sort_values(by='Timestamp', inplace=True)

df['CKC_Stage'] = df.apply(map_ckc, axis=1)

stage_names = {
    0: "Baseline/Non-Stage-Mapped",
    1: "Exploitation-Burst",
    2: "Exploitation-Sustained"
}

df['CKC_Stage_Name'] = df['CKC_Stage'].map(stage_names)

df.to_csv(processed_path, index=False)

print("File processed and saved.")

del df
gc.collect()