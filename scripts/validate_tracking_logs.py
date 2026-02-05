import pandas as pd

INPUT_FILE = "data/tracking_logs.xlsx"

df = pd.read_excel(INPUT_FILE)

print("=== BASIC DATASET INFO ===")
print(df.info())

print("\n=== MISSING VALUES PER COLUMN ===")
print(df.isnull().sum())

print("\n=== FIRST TIME VALUES ===")
print(df["time"].head(10))

print("\n=== LAST TIME VALUES ===")
print(df["time"].tail(10))