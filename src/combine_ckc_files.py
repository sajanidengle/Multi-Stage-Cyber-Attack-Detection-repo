import pandas as pd
import glob
import os

input_folder = "data/ckc_mapped"
output_file = "data/final_ckc_dataset.csv"

files = glob.glob(os.path.join(input_folder, "*.csv"))

print(f"Found {len(files)} files.")

df_list = []

for file in files:
    print(f"Loading {file}...")
    df = pd.read_csv(file)
    df_list.append(df)

print("Concatenating files...")
final_df = pd.concat(df_list, ignore_index=True)

print("Saving final dataset...")
final_df.to_csv(output_file, index=False)

print("Final dataset saved as:", output_file)
print("Total rows:", len(final_df))
print("Total columns:", len(final_df.columns))