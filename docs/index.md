# Adaptive Camera Smoothing for Virtual Production

## Documentation

- [Architecture](architecture.md)
- [Feature Engineering](feature_engineering.md)
- [Evaluation & Results](evaluation.md)
  

This page documents the design, implementation, and evaluation of a **real-time adaptive camera smoothing system** built for virtual production (VP).

The project explores how lightweight machine learning can be used **as a control signal**, rather than as a black-box decision maker, under strict real-time and latency constraints.

---

## 1. Context & Motivation

In virtual production, camera motion is not just a technical signal — it is part of the **cinematic language**.

When using VR tracking systems as camera trackers (without VR gameplay), motion exhibits two very different characteristics:

- **Intentional motion**  
  (pans, tilts, navigation, reframing)

- **Unintentional motion**  
  (hand jitter, micro vibration, sensor noise)

Traditional camera smoothing applies a *fixed* filter strength, which forces an undesirable trade-off:
- Increase smoothing → visible lag
- Decrease smoothing → visible jitter

This project aims to remove that trade-off.

---

## 2. Design Philosophy

Three principles guided the design:

### 2.1 Causality
The system must operate using **only past and present frames**.  
No lookahead, no buffering, no latency tricks.

### 2.2 Interpretability
Every part of the system should be explainable:
- Why did smoothing increase here?
- Why did it decrease there?

This ruled out opaque models and complex pipelines.

### 2.3 Real-Time Safety
The final system must be:
- deterministic
- stable
- cheap to compute
- suitable for Unreal Engine C++ integration

Machine learning is used **to estimate intent**, not to directly manipulate transforms.

---

## 3. High-Level Approach

Instead of smoothing the camera directly with ML, the system predicts a **smoothing factor (α)** that controls a conventional filter.

> ML answers *“how much smoothing is appropriate right now?”*  
> Traditional filtering answers *“how smoothing is applied.”*

This separation is critical for stability.

---

## 4. System Pipeline

The complete pipeline is shown below:

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


Each stage is deliberately simple and testable.

---

## 5. Data & Feature Engineering

Rather than feeding raw pose values into a model, the system computes **motion statistics** over a short sliding window.

These statistics encode:
- motion stability
- jitter
- acceleration bursts
- frame timing

Examples include:
- velocity variance
- acceleration standard deviation
- current speed
- mean delta time

This makes the model robust to absolute scale and sensitive to *behavior* instead of position.

A detailed breakdown is provided in the feature engineering section.

---

## 6. Machine Learning Model

### Model Choice
A **regularized linear regression (Ridge)** model was used.

Reasons:
- fast inference
- smooth outputs
- interpretable weights
- predictable behavior under extrapolation

The model outputs a single continuous value:

α ∈ ℝ


This value is later clamped to a safe operational range.

### Why Not Classification?
Camera motion does not switch cleanly between modes.  
Intent exists on a continuum.

Regression allows:
- smooth transitions
- no threshold artifacts
- no state machine

---

## 7. Evaluation Strategy

Because this is a **control system**, evaluation focused on:

- within-shot behavior
- smoothness over time
- response to motion changes
- absence of oscillation or lag

The model was evaluated **within each scenario**, rather than on unseen scenarios, to reflect real VP usage where shot types are known.

Visual inspection of α over time was treated as a first-class evaluation tool.

---

## 8. Output Conditioning

The raw ML output is not applied directly.

Instead:
1. α is clamped to a safe range
2. α controls a standard smoothing filter
3. No additional state or delay is introduced

This mirrors best practices in robotics and camera stabilization systems:
> *ML proposes — control logic disposes.*

---

## 9. Unreal Engine Integration

At runtime, Unreal Engine does **not** run ML libraries.

Instead:
- trained model parameters are exported as JSON
- normalization constants and weights are loaded once
- inference is a simple dot product + clamp

This ensures:
- deterministic behavior
- easy debugging
- production readiness

Both **position and rotation** are smoothed, with quaternion-based rotation handling to avoid artifacts.

---

## 10. Current Status

The system currently supports:
- real-time adaptive smoothing
- position and rotation channels
- shared sliding window
- Unreal Engine C++ implementation

The architecture is intentionally extensible to:
- per-axis models
- different window sizes
- different VP shot styles

---

## 11. What This Project Demonstrates

This project is not about “using ML”.

It demonstrates:
- how to apply ML **as part of a control system**
- how to respect real-time constraints
- how to integrate ML into a production engine responsibly
- how to design for interpretability and iteration

---

## 12. Next Sections

- Feature Engineering
- Model Design Details
- Evaluation & Visualizations
- Unreal Engine Implementation

Each section focuses on *why decisions were made*, not just *what was done*.

