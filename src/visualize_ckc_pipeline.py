import pandas as pd
import matplotlib.pyplot as plt

print("Loading dataset...")

file_path = "data/final_ckc_dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded.")

# Count CKC stage distribution
stage_counts = df["CKC_Stage"].value_counts()

print("\nCKC Stage Distribution:\n")
print(stage_counts)

# Plot
plt.figure(figsize=(10,6))

stage_counts.plot(
    kind="bar",
    color=[
        "#4CAF50",   # Benign
        "#F32121",   # Reconaissance    
        "#FF9800",   # Actions
        "#F44336",   # Exploitation
        "#9C27B0",   # C2
        "#212CF3"    # Installation
    ]
)

plt.title("Cyber Kill Chain Stage Distribution")
plt.xlabel("CKC Stage")
plt.ylabel("Number of Network Flows")

plt.xticks(rotation=30)

plt.tight_layout()

output_file = "data/ckc_stage_distribution.png"

plt.savefig(output_file)

print("\nChart saved to:", output_file)

plt.show()