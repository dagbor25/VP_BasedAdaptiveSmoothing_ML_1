
# Adaptive Camera Smoothing for Virtual Production

A real-time, machine-learning–driven adaptive camera smoothing system for **virtual production**, designed to stabilize micro jitter while preserving intentional camera motion — with **near-zero perceptual lag**.

This project uses VR headset pose data **purely as a tracking device** (no VR gameplay) to drive a `CineCameraActor` in Unreal Engine, applying adaptive smoothing based on learned motion intent.

---



##  Problem Statement

In virtual production (VP), camera motion must feel **natural, responsive, and stable**.

Traditional camera smoothing approaches rely on **all-axis tracking parameters**, which leads to:

-  **Lag/responsiveness** issue during filming operations
-  **Insufficient or over stabilization** during micro jitter
-  Manual calibration for different shot types
-  Poor balance between responsiveness and stability

This problem is amplified when using VR tracking systems as camera trackers, where IMU noise is inherent, and motion characteristics vary continuously.

---

## Core Idea

Instead of applying a fixed smoothing strength, this system **predicts a per-axis adaptive smoothing factor (α) in real time**, based on recent motion statistics. The smoothing factor is mapped inversely against velocity and acceleration.

> Fast, intentional motion → **low smoothing**  
> Slow, jitter-dominated motion → **high smoothing**

The result is an **intent-aware camera smoother** that adapts continuously in real-time.

---

##  Solution Overview

1. **Capture pose data** (position & rotation) in Unreal Engine
2. **Compute motion features** over a short,  sliding window
3. **Predict a smoothing factor (α)** using a lightweight regression model
4. **Clamp α to safe bounds**
5. **Apply adaptive smoothing** to camera position and rotation

Key properties:
- Fully causal (no future frames)
- Interpretable model
- Deterministic runtime behavior
- Unreal Engine–native C++ integration
- No ML frameworks required at runtime

---

## System Architecture

VR Tracking Pose
→
Sliding Window (frames)
→
Motion Feature Extraction
→
ML Regression Model
→
Clamp α
→
Adaptive Camera Smoothing
→
CineCameraActor
→
Validation


---

##  Feature Set (per window)

The model operates on **engineered motion statistics**, not raw pose values:

| Feature | Description |
|------|------------|
| `v_mean` | Mean velocity magnitude |
| `v_std` | Velocity fluctuation (jitter indicator) |
| `a_mean` | Mean acceleration magnitude |
| `a_std` | Acceleration variability |
| `pos_var` | Position variance |
| `vel_var` | Velocity variance |
| `abs_v_current` | Current speed |
| `dt_mean` | Mean frame delta time |

These features capture **motion intent vs instability**, which is critical for VP.

---

##  Machine Learning Approach

- **Model**: Ridge Regression (linear model)
- **Output**: Continuous smoothing factor α
- **Why regression?**
  - No hard thresholds
  - Smooth transitions
  - Interpretable behavior
  - Stable and fast inference

> ML predicts *intententional camera operation* — control logic enforces *physical limits*.

α is clamped to a safe range before being applied.

---

##  Unreal Engine Integration

- Model parameters exported as JSON
- Loaded once at runtime
- Prediction = simple dot product + clamp
- Implemented entirely in **C++**
- Applied to both **position and rotation**
- Quaternion-based rotation smoothing (no gimbal lock)

The system runs comfortably in real time and is suitable for live VP workflows.

---

##  Tech Stack

- **Python**: data processing, feature extraction, model training
- **scikit-learn**: regression model
- **Unreal Engine 5 (C++)**: real-time integration
- **GitHub Pages**: documentation & visualizations

---

##  Results

- Adaptive smoothing responds correctly to motion intent
- No perceptible lag during fast camera movement
- Effective stabilization during micro jitter
- Stable, bounded control signal
- Fully interpretable behavior

(See full plots and analysis in the documentation.)

---

##  Documentation

Full project walkthrough, visualizations, and design decisions:  
**GitHub Pages:**  https://<your-username>.github.io/VP_BasedAdaptiveSmoothing_ML/


---

##  Next Steps

- Independent models per axis (Y/Z)
- Further tuning for different VP shot styles
- Implement non-linear ML models to estimate alpha
- Simulate raw tracking and adaptive smoothing behaviour in real time


---

## License

MIT License
