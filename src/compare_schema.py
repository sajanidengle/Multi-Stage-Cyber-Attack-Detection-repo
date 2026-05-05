import pandas as pd

file1 = "data/raw/Friday-02-03-2018_TrafficForML_CICFlowMeter.csv"
file2 = "data/raw/Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv"

df1 = pd.read_csv(file1, nrows=5)
df2 = pd.read_csv(file2, nrows=5)

df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

cols1 = set(df1.columns)
cols2 = set(df2.columns)

print("Columns only in Friday file:")
print(cols1 - cols2)

print("\nColumns only in Tuesday file:")
print(cols2 - cols1)