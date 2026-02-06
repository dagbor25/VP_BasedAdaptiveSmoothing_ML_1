import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Configuration
DATA_FILE = Path("data/training_X_axis.csv")

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

TEST_SPLIT_RATIO = 0.2
RIDGE_ALPHA = 1.0   # regularization strength

# Load data
df = pd.read_csv(DATA_FILE)

# Sanity checks
assert "alpha" in df.columns, "Missing target column: alpha"
for col in FEATURE_COLUMNS:
    assert col in df.columns, f"Missing feature column: {col}"

print(f"Loaded dataset with {len(df)} samples")

# Train / test split (NO SHUFFLING)
train_parts = []
test_parts = []

for scenario, group in df.groupby("scenario"):
    split_idx = int((1.0 - TEST_SPLIT_RATIO) * len(group))
    train_parts.append(group.iloc[:split_idx])
    test_parts.append(group.iloc[split_idx:])

train_df = pd.concat(train_parts)
test_df  = pd.concat(test_parts)

X_train = train_df[FEATURE_COLUMNS].values
y_train = train_df["alpha"].values

X_test  = test_df[FEATURE_COLUMNS].values
y_test  = test_df["alpha"].values

print("\nScenario-aware split:")
print("Train samples:", len(train_df))
print("Test samples: ", len(test_df))

X_train = train_df[FEATURE_COLUMNS].values
y_train = train_df["alpha"].values

X_test  = test_df[FEATURE_COLUMNS].values
y_test  = test_df["alpha"].values

print(f"Train samples: {len(train_df)}")
print(f"Test samples:  {len(test_df)}")

# Feature normalization (fit on TRAIN ONLY)
scaler = StandardScaler()
X_train_norm = scaler.fit_transform(X_train)
X_test_norm  = scaler.transform(X_test)

print("\nNormalization statistics (TRAIN set only):")
for name, mean, std in zip(FEATURE_COLUMNS, scaler.mean_, scaler.scale_):
    print(f"{name:15s} mean={mean:10.4f} std={std:10.4f}")

# Sanity check
print("\nSanity check (normalized TRAIN data):")
print("Mean ≈ 0 :", np.mean(X_train_norm, axis=0))
print("Std  ≈ 1 :", np.std(X_train_norm, axis=0))

# Train Ridge Regression model
model = Ridge(alpha=RIDGE_ALPHA)
model.fit(X_train_norm, y_train)


# Evaluation
y_train_pred = model.predict(X_train_norm)
y_test_pred  = model.predict(X_test_norm)

train_mse = mean_squared_error(y_train, y_train_pred)
test_mse  = mean_squared_error(y_test, y_test_pred)

print("\nModel performance:")
print(f"Train MSE: {train_mse:.6f}")
print(f"Test  MSE: {test_mse:.6f}")

# Inspect learned weights (IMPORTANT)
print("\nLearned feature weights (sorted by importance):")
for name, w in sorted(
    zip(FEATURE_COLUMNS, model.coef_),
    key=lambda x: abs(x[1]),
    reverse=True
):
    print(f"{name:15s} {w:+.6f}")

print("\nIntercept:")
print(f"{model.intercept_:+.6f}")


print("\nTraining complete.")