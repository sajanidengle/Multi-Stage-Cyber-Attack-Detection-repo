import pandas as pd

print("Loading dataset...")

file_path = "data/final_ckc_dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded.")
print("Total rows:", len(df))

# Columns we want to show in the example
important_columns = [
    "Dst Port",
    "Flow Duration",
    "Flow Pkts/s",
    "Flow IAT Mean",
    "Tot Fwd Pkts",
    "Tot Bwd Pkts",
    "Label",
    "CKC_Stage"
]

print("\nExtracting example flow for each CKC stage...\n")

examples = []

# Get unique CKC stages
stages = df["CKC_Stage"].unique()

for stage in stages:

    stage_df = df[df["CKC_Stage"] == stage]

    sample = stage_df.sample(1, random_state=42)

    sample = sample[important_columns]

    examples.append(sample)

# Combine all examples
examples_df = pd.concat(examples)

print("Example flows:\n")

print(examples_df)

# Save to CSV for presentation
output_file = "data/ckc_stage_examples.csv"

examples_df.to_csv(output_file, index=False)

print("\nExamples saved to:", output_file)