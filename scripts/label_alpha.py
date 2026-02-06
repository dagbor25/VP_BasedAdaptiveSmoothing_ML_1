import pandas as pd
from pathlib import Path

# CONFIGURATION
INPUT_DIR = Path("data/features/X_axis")
OUTPUT_DIR = Path("data/labeled/X_axis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALPHA_MAP = {
    # A. Micro / Steady
    "still_on_tripod": 0.9,
    "handheld_still": 0.85,

    # B. Controlled Motion
    "controlled_handheld_pan": 0.45,
    "controlled_handheld_tilt": 0.45,
    "controlled_on_tripod_pan": 0.35,
    "controlled_on_tripod_tilt": 0.3,
    "slide_handheld": 0.4,
    "travel_handheld": 0.35,

    # C. Aggressive / Intentional
    "fast_pan_tripod": 0.1,
    "fast_tilt_tripod": 0.1,
    "handheld_full_nav": 0.2,
}

def infer_alpha(filename: str) -> float:
    for key, alpha in ALPHA_MAP.items():
        if key in filename:
            return alpha
    raise ValueError(f"No alpha rule for file: {filename}")

# Label files
for csv_file in INPUT_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)
    alpha = infer_alpha(csv_file.name)
    df["alpha"] = alpha

    out_file = OUTPUT_DIR / csv_file.name
    df.to_csv(out_file, index=False)

    print(f"Labeled {csv_file.name} → alpha = {alpha}")
