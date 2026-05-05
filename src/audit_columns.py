import pandas as pd
import glob

files = glob.glob("data/processed/*.csv")

column_sets = []

for file in files:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    column_sets.append(set(df.columns))

first = column_sets[0]

for i, cols in enumerate(column_sets):
    if cols != first:
        print(f"Column mismatch in file {i}")
        print(cols.symmetric_difference(first))

print("Column consistency check completed.")