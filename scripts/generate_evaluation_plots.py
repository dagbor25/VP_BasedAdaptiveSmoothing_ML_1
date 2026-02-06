import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

# Configuration
DATA_FILE = Path("data/training_X_axis.csv")
OUTPUT_DIR = Path("docs/visuals")

SCENARIO_NAME = "still_on_tripod"

FEATURE_COLUMNS = [
    "v_mean",
    "v_std",
    "a_mean",
    "a_std",
    "pos_var",
    "vel_var",
    "abs_v_current",
    "dt_mean",
]

RIDGE_ALPHA = 1.0
ALPHA_MIN = 0.05
ALPHA_MAX = 0.85

# Prepare output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE)
scenario_df = df[df["scenario"] == SCENARIO_NAME].copy()

assert len(scenario_df) > 0, "Scenario not found"

# Train model (same as training script)
X = df[FEATURE_COLUMNS].values
y = df["alpha"].values

scaler = StandardScaler()
X_norm = scaler.fit_transform(X)

model = Ridge(alpha=RIDGE_ALPHA)
model.fit(X_norm, y)

# Predict alpha for selected scenario
X_scenario = scenario_df[FEATURE_COLUMNS].values
X_scenario_norm = scaler.transform(X_scenario)

alpha_raw = model.predict(X_scenario_norm)
alpha = np.clip(alpha_raw, ALPHA_MIN, ALPHA_MAX)

time = np.arange(len(alpha))

# Plot 1: Alpha vs Time
plt.figure(figsize=(10, 4))
plt.plot(time, alpha, linewidth=1.5)
plt.xlabel("Window index (time)")
plt.ylabel("Alpha (smoothing factor)")
plt.title(f"Adaptive Smoothing (α) Over Time\nScenario: {SCENARIO_NAME}")
plt.ylim(ALPHA_MIN, ALPHA_MAX)
plt.grid(True)

alpha_time_path = OUTPUT_DIR / f"alpha_vs_time_{SCENARIO_NAME}.png"
plt.tight_layout()
plt.savefig(alpha_time_path, dpi=150)
plt.close()

# Plot 2: Motion vs Alpha (dual axis)
fig, ax1 = plt.subplots(figsize=(10, 4))

ax1.plot(
    time,
    scenario_df["v_std"].values,
    color="tab:blue",
    label="Velocity fluctuation (v_std)"
)
ax1.set_xlabel("Window index (time)")
ax1.set_ylabel("v_std", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(
    time,
    alpha,
    color="tab:orange",
    label="Alpha (smoothing factor)"
)
ax2.set_ylabel("Alpha", color="tab:orange")
ax2.set_ylim(ALPHA_MIN, ALPHA_MAX)
ax2.tick_params(axis="y", labelcolor="tab:orange")

plt.title(f"Motion vs Adaptive Smoothing\nScenario: {SCENARIO_NAME}")
fig.tight_layout()

motion_alpha_path = OUTPUT_DIR / f"motion_vs_alpha_{SCENARIO_NAME}.png"
plt.savefig(motion_alpha_path, dpi=150)
plt.close()

# Done
print("Plots saved:")
print(alpha_time_path)
print(motion_alpha_path)
