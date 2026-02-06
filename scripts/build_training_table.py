from pathlib import Path
import pandas as pd

INPUT_DIR = Path("data/labeled/X_axis")
OUTPUT_FILE = Path("data/training_X_axis.csv")

def infer_scenario_from_filename(filename: str) -> str:
    # Example: controlled_handheld_pan_take_1.csv
    return filename.split("_take_")[0]

def build_training_table():
    all_rows = []

    for csv_file in INPUT_DIR.glob("*.csv"):
        df = pd.read_csv(csv_file)

        if "alpha" not in df.columns:
            raise ValueError(f"Missing alpha in {csv_file.name}")

        scenario = infer_scenario_from_filename(csv_file.name)
        df["scenario"] = scenario

        all_rows.append(df)

    if not all_rows:
        raise RuntimeError("No labeled CSV files found.")

    full_df = pd.concat(all_rows, ignore_index=True)
    full_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Training table written to {OUTPUT_FILE}")
    print("Scenarios found:", full_df["scenario"].unique())

if __name__ == "__main__":
    build_training_table()