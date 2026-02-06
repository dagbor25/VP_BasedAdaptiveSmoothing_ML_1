import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

# Configuration
DATA_FILE = Path("data/training_X_axis.csv")
SCENARIO_NAME = "handheld_full_nav"

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

# Load dataset
df = pd.read_csv(DATA_FILE)

scenario_df = df[df["scenario"] == SCENARIO_NAME].copy()

assert len(scenario_df) > 0, "Scenario not found!"

print(f"Loaded {len(scenario_df)} samples for scenario: {SCENARIO_NAME}")

# Train model again (same as train_regressor.py)
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
alpha_clamped = np.clip(alpha_raw, ALPHA_MIN, ALPHA_MAX)

# Plot
time = np.arange(len(alpha_clamped))

plt.figure()
plt.plot(time, alpha_clamped, label="Clamped α")
plt.xlabel("Window index (time)")
plt.ylabel("Alpha (smoothing factor)")
plt.title(f"Predicted α over time — {SCENARIO_NAME}")
plt.legend()
plt.show()

# Secondary plot: motion vs alpha
plt.figure()
plt.plot(time, scenario_df["v_std"].values, label="v_std (velocity fluctuation)")
plt.plot(time, alpha_clamped, label="Clamped α")
plt.xlabel("Window index (time)")
plt.title("Motion vs Adaptive Smoothing")
plt.legend()
plt.show()

# Tertiary Plot
fig, ax1 = plt.subplots()

ax1.plot(time, scenario_df["v_std"].values, color="tab:blue", label="v_std")
ax1.set_xlabel("Window index (time)")
ax1.set_ylabel("v_std (velocity fluctuation)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(time, alpha_clamped, color="tab:orange", label="Clamped α")
ax2.set_ylabel("Alpha (smoothing factor)", color="tab:orange")
ax2.set_ylim(ALPHA_MIN, ALPHA_MAX)
ax2.tick_params(axis="y", labelcolor="tab:orange")

plt.title("Motion vs Adaptive Smoothing — handheld_full_nav")
fig.tight_layout()
plt.show()
