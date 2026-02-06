# System Architecture

This page describes the architecture of the adaptive camera smoothing system, from VR tracking input to the final CineCameraActor output.

---

## High-Level Concept

The system treats machine learning as a **decision aid**, not as a controller.

Instead of directly modifying the camera transform, the ML model predicts a **smoothing strength (α)**, which controls a traditional smoothing filter.

This separation ensures stability, interpretability, and real-time safety.

---

## Conceptual Flow

VR Headset Tracking
-->
Unreal Engine Pose Stream
-->
Motion Analysis (short history)
-->
Intent Estimation (ML)
-->
Smoothing Strength (α)
-->
Camera Filtering
-->
CineCameraActo

At no point does ML directly move the camera.

## Runtime Pipeline (Technical)

The runtime system operates fully in real time and is entirely causal.

[Pose @ Frame N]
-->
[Compute Velocity & Acceleration]
-->
[Sliding Window Buffer (N-k … N)]
-->
[Feature Extraction]
-->
[Normalize Features]
-->
[Linear Regression Model]
-->
[Clamp α]
-->
[Adaptive Smoothing]
-->
[CineCameraActor Transform]

Key properties:
- No lookahead
- Fixed computational cost
- Deterministic behavior

## Training vs Runtime Separation

### Training (Offline – Python)

Unreal Logs
-->
Data Cleaning
-->
Feature Extraction
-->
Alpha Labeling
-->
Regression Training
-->
Model Parameters (JSON)

### Runtime (Online – Unreal Engine C++)
Model Parameters (JSON)
-->
Feature Normalization
-->
Dot Product + Bias
-->
Clamp α
-->
Camera Smoothing


##  ML Model → Gain Scheduler
Smoothing Filter → Low-Pass Filter

The ML model schedules the filter gain (α) based on motion intent, while the filter itself remains simple and stable.

This architecture mirrors best practices in:
- robotics
- camera stabilization
- flight control systems

It avoids instability while allowing adaptive behavior.

## Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    A[VR Headset Tracking] --> B[Unreal Pose Stream]
    B --> C[Velocity & Acceleration]
    C --> D[Sliding Window Buffer]
    D --> E[Feature Extraction]
    E --> F[Normalize Features]
    F --> G[Regression Model]
    G --> H[Clamp α]
    H --> I[Adaptive Smoothing]
    I --> J[CineCameraActor]
