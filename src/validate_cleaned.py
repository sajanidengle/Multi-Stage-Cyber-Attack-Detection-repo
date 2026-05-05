import glob
import pandas as pd

files = glob.glob("data/base_clean/cleaned_*.csv")

column_sets = []

for file in files:
    df = pd.read_csv(file, nrows=5)
    df.columns = df.columns.str.strip()
    column_sets.append(tuple(sorted(df.columns)))

print("Number of cleaned files:", len(files))
print("Unique column structures:", len(set(column_sets)))

# Show column count
df_sample = pd.read_csv(files[0], nrows=5)
print("Number of columns:", len(df_sample.columns))

print("\nColumns:")
print(df_sample.columns.tolist())