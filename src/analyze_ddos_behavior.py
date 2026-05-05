import pandas as pd

file = "Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv"

df = pd.read_csv(f"data/raw/{file}")

ddos = df[df['Label'] != 'Benign']
benign = df[df['Label'] == 'Benign']

features = [
    'Flow Duration',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts'
]

print("\n=== DDoS Statistics ===\n")
print(ddos[features].describe())

print("\nFlow Duration Quantiles (DDoS):")
print(ddos['Flow Duration'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\nFlow Pkts/s Quantiles (DDoS):")
print(ddos['Flow Pkts/s'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\n=== Benign Statistics ===\n")
print(benign[features].describe())

print("\nFlow Duration Quantiles (Benign):")
print(benign['Flow Duration'].quantile([0.5, 0.75, 0.9, 0.95]))

print("\nFlow Pkts/s Quantiles (Benign):")
print(benign['Flow Pkts/s'].quantile([0.5, 0.75, 0.9, 0.95]))

# Candidate slow-exhaustion rule test
candidate = df[
    (df['Flow Duration'] > 2738237) &
    (df['Flow Pkts/s'] < 100) &
    (df['Tot Fwd Pkts'] <= 10)
]

print("\nCandidate rule distribution:")
print(candidate['Label'].value_counts())

# Refined candidate rule test
refined_candidate = df[
    (df['Flow Duration'] > 5000000) &        # much longer than benign median
    (df['Flow Pkts/s'] < 10) &               # low packet rate
    (df['Flow Byts/s'] < 1000) &             # low byte throughput
    (df['Tot Fwd Pkts'] <= 5)                # minimal packets
]

print("\nRefined rule distribution:")
print(refined_candidate['Label'].value_counts())

df['Total_Pkts'] = df['Tot Fwd Pkts'] + df['Tot Bwd Pkts']

print("\nTotal Packets Quantiles (DDoS):")
print(ddos['Tot Fwd Pkts'].add(ddos['Tot Bwd Pkts']).quantile([0.5, 0.75, 0.9, 0.95]))

print("\nTotal Packets Quantiles (Benign):")
print(benign['Tot Fwd Pkts'].add(benign['Tot Bwd Pkts']).quantile([0.5, 0.75, 0.9, 0.95]))

# Precision slow-HTTP rule test
precision_candidate = df[
    (df['Flow Duration'] > 5000000) &
    (df['Total_Pkts'] <= 8) &
    (df['Flow Pkts/s'] < 10)
]

print("\nPrecision rule distribution:")
print(precision_candidate['Label'].value_counts())

# Multi-flow aggregation test
candidate_flows = df[
    (df['Flow Duration'] > 5000000) &
    (df['Flow Pkts/s'] < 10) &
    (df['Total_Pkts'] <= 8)
]

flow_counts = candidate_flows.groupby('Src IP')['Label'].count()

print("\nTop 10 sources by suspicious flow count:")
print(flow_counts.sort_values(ascending=False).head(10))

# Check benign suspicious flow counts
benign_candidate = candidate_flows[candidate_flows['Label'] == 'Benign']
benign_counts = benign_candidate.groupby('Src IP')['Label'].count()

print("\nTop 10 benign sources by suspicious flow count:")
print(benign_counts.sort_values(ascending=False).head(10))

# Variance test per source
import numpy as np

candidate_flows = df[
    (df['Flow Duration'] > 5000000) &
    (df['Flow Pkts/s'] < 10)
]

variance_per_source = candidate_flows.groupby('Src IP')['Total_Pkts'].var()

print("\nTop 10 lowest variance sources:")
print(variance_per_source.sort_values().head(10))

# Check label composition for zero-variance sources

zero_variance_sources = variance_per_source[variance_per_source == 0].index

print("\nZero variance sources label distribution:")

for src in list(zero_variance_sources)[:10]:
    print(f"\nSource: {src}")
    print(df[df['Src IP'] == src]['Label'].value_counts())