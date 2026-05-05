import pandas as pd

df = pd.read_csv("data/final_ckc_dataset.csv")

print("\nCKC Stage Distribution:\n")
print(df["CKC_Stage"].value_counts())