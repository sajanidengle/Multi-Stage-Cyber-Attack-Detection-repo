import pandas as pd

df = pd.read_csv("data/cleaned_02_14_2018.csv")

print("Dataset shape:", df.shape)

print("\nLabel distribution:")
print(df['Label'].value_counts())

print("\nPercentage distribution:")
print(df['Label'].value_counts(normalize=True) * 100)