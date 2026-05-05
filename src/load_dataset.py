import pandas as pd
import numpy as np

print("Loading full dataset...")

df = pd.read_csv("data/02-14-2018.csv", low_memory=False)

print("Initial shape:", df.shape)

# Clean column spacing
df.columns = df.columns.str.strip()

# Replace infinity values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop missing values
# Only drop rows if critical behavioral columns are missing
critical_cols = ['Flow Duration', 'Flow Byts/s', 'Flow Pkts/s']
df.dropna(subset=critical_cols, inplace=True)

# Drop duplicates
df.drop_duplicates(inplace=True)

# Remove negative flow durations (physically impossible)
df = df[df['Flow Duration'] >= 0]

print("Shape after cleaning:", df.shape)

# Convert Timestamp
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df.dropna(subset=['Timestamp'], inplace=True)

# Sort by time
df.sort_values(by='Timestamp', inplace=True)

print("Final shape after timestamp cleaning:", df.shape)

# Save cleaned version
df.to_csv("data/cleaned_02_14_2018.csv", index=False)

print("Cleaning complete and saved.")