import pandas as pd
import os

# CONFIGURATION
INPUT_FILE = "data/features_all_axes.csv"
OUTPUT_ROOT = "data/edge_impulse"

# Load features
df = pd.read_csv(INPUT_FILE)

# Create root output folder
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# Split by axis, scenario, take
for axis, axis_df in df.groupby("axis"):
    axis_dir = os.path.join(OUTPUT_ROOT, axis)
    os.makedirs(axis_dir, exist_ok=True)

    for (scenario, take), g in axis_df.groupby(["scenario", "take"]):
        filename = f"{scenario}_take_{take}.csv"
        filepath = os.path.join(axis_dir, filename)

        # Drop metadata columns not needed by Edge Impulse
        ei_df = g.drop(columns=["scenario", "take", "axis"])

        ei_df.to_csv(filepath, index=False)

print("Edge Impulse CSV splitting complete")
print(f"Output written to: {OUTPUT_ROOT}")