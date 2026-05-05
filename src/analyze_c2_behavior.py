import pandas as pd
import numpy as np

# ===============================
# Load Dataset
# ===============================

file = "Friday-02-03-2018_TrafficForML_CICFlowMeter.csv"
df = pd.read_csv(f"data/raw/{file}", low_memory=False)

df.columns = df.columns.str.strip()
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

df.replace([np.inf, -np.inf], np.nan, inplace=True)

bot = df[df['Label'] == 'Bot']
benign = df[df['Label'] == 'Benign']

# ===============================
# Basic Behavioral Features
# ===============================

features_basic = [
    'Flow Duration',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts'
]

print("\n==============================")
print("=== BOT BASIC STATISTICS ===")
print("==============================\n")
print(bot[features_basic].describe())

print("\nBot Flow Duration Quantiles:")
print(bot['Flow Duration'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\nBot Flow Pkts/s Quantiles:")
print(bot['Flow Pkts/s'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\n==============================")
print("=== BENIGN BASIC STATISTICS ===")
print("==============================\n")
print(benign[features_basic].describe())

print("\nBenign Flow Duration Quantiles:")
print(benign['Flow Duration'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\nBenign Flow Pkts/s Quantiles:")
print(benign['Flow Pkts/s'].quantile([0.5, 0.75, 0.9, 0.95]))

# ===============================
# Temporal Behavior via IAT Features
# ===============================

features_temporal = [
    'Flow IAT Mean',
    'Flow IAT Std',
    'Active Mean',
    'Idle Mean'
]

print("\n==============================")
print("=== BOT TEMPORAL FEATURES ===")
print("==============================\n")
print(bot[features_temporal].describe())

print("\n==============================")
print("=== BENIGN TEMPORAL FEATURES ===")
print("==============================\n")
print(benign[features_temporal].describe())

# ===============================
# Candidate C2 Rule (Flow-Level)
# ===============================

candidate_c2 = df[
    (df['Flow Duration'] < 20000) &
    (df['Flow Pkts/s'] > 500) &
    (df['Tot Fwd Pkts'] <= 5)
]

print("\n==============================")
print("=== Candidate C2 Rule Distribution ===")
print("==============================\n")
print(candidate_c2['Label'].value_counts())

# Temporal-based C2 candidate
temporal_c2 = df[
    (df['Flow IAT Mean'] < 5000) &
    (df['Flow Duration'] < 20000)
]

print("\n==============================")
print("=== Temporal C2 Rule Distribution ===")
print("==============================\n")
print(temporal_c2['Label'].value_counts())