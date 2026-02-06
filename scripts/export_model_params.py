import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

# Config
DATA_FILE = Path("data/training_X_axis.csv")
OUT_FILE  = Path("data/model_X_axis.json")

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

# Train
df = pd.read_csv(DATA_FILE)

X = df[FEATURE_COLUMNS].values
y = df["alpha"].values

scaler = StandardScaler()
X_norm = scaler.fit_transform(X)

model = Ridge(alpha=RIDGE_ALPHA)
model.fit(X_norm, y)

# Export
export = {
    "feature_order": FEATURE_COLUMNS,
    "means": scaler.mean_.tolist(),
    "stds": scaler.scale_.tolist(),
    "weights": model.coef_.tolist(),
    "bias": float(model.intercept_),
    "alpha_min": ALPHA_MIN,
    "alpha_max": ALPHA_MAX,
}

OUT_FILE.parent.mkdir(exist_ok=True, parents=True)

with open(OUT_FILE, "w") as f:
    json.dump(export, f, indent=2)

print(f"Model exported to {OUT_FILE}")