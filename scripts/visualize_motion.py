import pandas as pd
import matplotlib.pyplot as plt


# Configuration
INPUT_FILE = "data/tracking_logs_with_velocity.csv"
SCENARIO = "controlled_handheld_pan"
TAKE = 1
AXIS = "X_pose"   # try X_pose, Y_pose, or Z_pose

# Load data
df = pd.read_csv(INPUT_FILE)

# Filter scenario + take
df = df[(df["scenario"] == SCENARIO) & (df["take"] == TAKE)]

# Extract signals
time = df["time"]
pos = df[AXIS]
vel = df[f"vel_{AXIS}"]

# Acceleration (second derivative)
acc = vel.diff() / df["dt"]


# Plot
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time, pos)
plt.title(f"{SCENARIO} take {TAKE} — Position ({AXIS})")
plt.ylabel("Position")

plt.subplot(3, 1, 2)
plt.plot(time, vel)
plt.title("Velocity")
plt.ylabel("Units / s")

plt.subplot(3, 1, 3)
plt.plot(time, acc)
plt.title("Acceleration")
plt.ylabel("Units / s²")
plt.xlabel("Time (s)")

plt.tight_layout()
plt.show()