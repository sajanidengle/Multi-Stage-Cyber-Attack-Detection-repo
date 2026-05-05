import pandas as pd

print("Loading RAW dataset...")

df_raw = pd.read_csv("data/02-14-2018.csv", low_memory=False)

print("\nRaw label distribution:")
print(df_raw['Label'].value_counts())