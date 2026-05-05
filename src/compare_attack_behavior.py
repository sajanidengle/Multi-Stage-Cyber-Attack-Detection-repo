import pandas as pd

df = pd.read_csv("data/cleaned_02_14_2018.csv")

features = [
    'Flow Duration',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts'
]

print("Benign stats:\n")
print(df[df['Label'] == 'Benign'][features].describe())

print("\nSSH-Bruteforce stats:\n")
print(df[df['Label'] == 'SSH-Bruteforce'][features].describe())

print("\nFTP-Bruteforce stats:\n")
print(df[df['Label'] == 'FTP-BruteForce'][features].describe())