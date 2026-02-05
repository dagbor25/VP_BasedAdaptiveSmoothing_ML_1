import pandas as pd
import numpy as np

INPUT_FILE = "data/tracking_logs.xlsx"
OUTPUT_FILE = "data/tracking_logs_with_velocity.csv"

# Load data
df = pd.read_excel(INPUT_FILE)

# Sort by scenario, take, and time
# (important for correct differencing)
df = df.sort_values(by=["scenario", "take", "time"]).reset_index(drop=True)

# Compute dt (time difference per scenario/take)
df["dt"] = df.groupby(["scenario", "take"])["time"].diff()

# Compute linear velocity (position derivatives)
for axis in ["X_pose", "Y_pose", "Z_pose"]:
    df[f"vel_{axis}"] = (
        df.groupby(["scenario", "take"])[axis].diff() / df["dt"]
    )

# Compute angular velocity (Euler angle derivatives)
for axis in ["X_rot", "Y_rot", "Z_rot"]:
    df[f"ang_vel_{axis}"] = (
        df.groupby(["scenario", "take"])[axis].diff() / df["dt"]
    )

# Save processed data
df.to_csv(OUTPUT_FILE, index=False)

print("Velocity computation complete")
print(f" Output written to: {OUTPUT_FILE}")
