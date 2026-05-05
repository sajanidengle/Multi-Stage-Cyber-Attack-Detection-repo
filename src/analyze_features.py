import pandas as pd

df = pd.read_csv("data/cleaned_02_14_2018.csv")

# Select key behavioral features
features = [
    'Flow Duration',
    'Flow Byts/s',
    'Flow Pkts/s',
    'SYN Flag Cnt',
    'ACK Flag Cnt',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts'
]

print("Descriptive statistics:")
print(df[features].describe())