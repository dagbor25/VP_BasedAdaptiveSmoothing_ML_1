import pandas as pd

# CONFIGURATION
INPUT_FILE = "data/tracking_logs_with_velocity.csv"
OUTPUT_FILE = "data/features_all_axes.csv"

WINDOW_MS = 300      # <<< configurable (e.g. 200–500)
AXES = ["X_pose", "Y_pose", "Z_pose"]

# Load data
df = pd.read_csv(INPUT_FILE)

# Ensure correct ordering
df = df.sort_values(by=["scenario", "take", "time"]).reset_index(drop=True)

feature_rows = []

# Feature extraction
for (scenario, take), g in df.groupby(["scenario", "take"]):

    g = g.reset_index(drop=True)

    for i in range(len(g)):
        t_now = g.loc[i, "time"]

        # Time-based window (past only)
        window = g[(t_now - g["time"]) <= (WINDOW_MS / 1000)] \
                   .iloc[:i+1]

        if len(window) < 3:
            continue  # not enough data

        for axis in AXES:
            v = window[f"vel_{axis}"]
            a = v.diff() / window["dt"]
            p = window[axis]

            feature_rows.append({
                "scenario": scenario,
                "take": take,
                "axis": axis,

                "v_mean": v.mean(),
                "v_std": v.std(),
                "a_mean": a.mean(),
                "a_std": a.std(),
                "pos_var": p.var(),
                "vel_var": v.var(),
                "abs_v_current": abs(v.iloc[-1]),
                "dt_mean": window["dt"].mean()
            })

# Save features
features_df = pd.DataFrame(feature_rows)
features_df.to_csv(OUTPUT_FILE, index=False)

print(" Feature extraction complete")
print(f" Output written to: {OUTPUT_FILE}")
