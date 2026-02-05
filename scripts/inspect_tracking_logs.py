import pandas as pd

# --------------------------------------------------
# Path to the raw tracking logs
# --------------------------------------------------
INPUT_FILE = "data/tracking_logs.xlsx"

# --------------------------------------------------
# Load the Excel file
# --------------------------------------------------
df = pd.read_excel(INPUT_FILE)

# --------------------------------------------------
# Basic inspection
# --------------------------------------------------
print("✅ File loaded successfully")
print("Number of rows:", len(df))
print("Column names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())