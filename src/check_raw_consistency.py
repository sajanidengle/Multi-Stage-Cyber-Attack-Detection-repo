import glob
import pandas as pd

files = glob.glob("data/raw/*.csv")

schemas = {}

for file in files:
    df = pd.read_csv(file, nrows=5)
    df.columns = df.columns.str.strip()
    schema = tuple(sorted(df.columns))
    
    if schema not in schemas:
        schemas[schema] = []
        
    schemas[schema].append(file)

print("\nNumber of unique schemas:", len(schemas))

for i, (schema, file_list) in enumerate(schemas.items(), 1):
    print(f"\nSchema {i} appears in:")
    for f in file_list:
        print("   ", f)