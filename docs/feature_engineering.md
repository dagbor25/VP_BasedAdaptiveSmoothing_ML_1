# Feature Engineering
## Navigation

- [Home](index.md)
- [Architecture](Architecture)
- [Evaluation & Results](evaluation.md)

This page explains **why and how motion features were designed** for the adaptive camera smoothing system, and why these features are suitable for real-time virtual production workflows.

The goal of feature engineering in this project is not to maximize model complexity, but to **encode camera intent and instability in a compact, interpretable form**.

---

## 1. Design Goals

Feature design was guided by four constraints:

1. **Real-time feasibility**  
   Features must be computable every frame or short window with negligible cost.

2. **Causality**  
   Only past and present data may be used. No lookahead.

3. **Interpretability**  
   Each feature should have a clear physical or perceptual meaning.

4. **Intent sensitivity**  
   Features must distinguish between:
   - intentional camera motion
   - unintentional jitter or noise

---

## 2. Why Not Raw Pose Data?

Raw position and rotation values are **poor predictors of intent**:

- Absolute position does not encode motion quality
- Sudden changes matter more than absolute values
- Noise is scale-dependent
- Frame rate variations distort raw derivatives

Instead, this system uses **statistical motion descriptors** computed over a short sliding window.

---

## 3. Sliding Window Approach

All features are computed over a **fixed-size, causal sliding window** (e.g. 10 frames).

This window:
- captures short-term motion behavior
- smooths per-frame noise
- avoids perceptible latency
- adapts naturally to different frame rates

Each window produces **one feature vector**, used to predict a smoothing factor (α).

---

## 4. Feature Overview

The final feature set contains **8 features**, chosen to balance expressiveness and simplicity:

| Feature | Category | Encodes |
|------|--------|--------|
| `v_mean` | Velocity | Overall motion intensity |
| `v_std` | Velocity | Motion instability / jitter |
| `a_mean` | Acceleration | Sustained directional change |
| `a_std` | Acceleration | Acceleration noise |
| `pos_var` | Position | Spatial instability |
| `vel_var` | Velocity | Jitter magnitude |
| `abs_v_current` | Velocity | Instantaneous intent |
| `dt_mean` | Timing | Frame rate awareness |

Each feature is explained below.

---

## 5. Velocity-Based Features

### 5.1 `v_mean` — Mean Velocity Magnitude

**What it measures:**  
Average speed over the window.

**Why it matters:**  
- High values indicate deliberate camera movement
- Low values indicate static or near-static shots

**Interpretation:**  
High `v_mean` often implies intentional motion and therefore **less smoothing**.

---

### 5.2 `v_std` — Velocity Standard Deviation

**What it measures:**  
How much velocity fluctuates over time.

**Why it matters:**  
- High fluctuation often indicates jitter
- Stable velocity indicates controlled motion

**Interpretation:**  
High `v_std` → motion instability → **more smoothing**

This is one of the most influential features in the model.

---

### 5.3 `vel_var` — Velocity Variance

**What it measures:**  
Magnitude of velocity instability (variance instead of standard deviation).

**Why both variance and std?**  
- Variance preserves scale
- Standard deviation preserves intuition

Together, they allow the model to respond differently to:
- small frequent jitter
- large but smooth motion

---

### 5.4 `abs_v_current` — Current Velocity Magnitude

**What it measures:**  
Instantaneous speed at the most recent frame.

**Why it matters:**  
- Captures sudden intentional motion
- Helps reduce smoothing during rapid transitions

**Important note:**  
On its own, this feature is not sufficient.  
It is only meaningful **in context** with variance-based features.

---

## 6. Acceleration-Based Features

### 6.1 `a_mean` — Mean Acceleration Magnitude

**What it measures:**  
Sustained change in velocity.

**Why it matters:**  
- Captures intentional starts, stops, and transitions
- Helps distinguish purposeful movement from noise

**Interpretation:**  
High `a_mean` often correlates with deliberate camera action → **less smoothing**.

---

### 6.2 `a_std` — Acceleration Standard Deviation

**What it measures:**  
Variability in acceleration.

**Why it matters:**  
- High values indicate erratic motion
- Low values indicate smooth transitions

This feature helps suppress micro jitter without penalizing smooth movement.

---

## 7. Position-Based Feature

### 7.1 `pos_var` — Position Variance

**What it measures:**  
Spatial instability within the window.

**Why it matters:**  
- Captures subtle vibration even when velocity is low
- Useful for detecting handheld “buzz” in static shots

This feature is especially important for:
- locked-off shots
- still handheld shots

---

## 8. Timing Feature

### 8.1 `dt_mean` — Mean Delta Time

**What it measures:**  
Average frame time over the window.

**Why it matters:**  
- Makes the model frame-rate aware
- Prevents sensitivity to FPS changes
- Improves robustness across 25 / 30 / 60 fps

This allows the same model to work across different VP setups.

---

## 9. Feature Normalization

All features are **standardized (Z-score)** using statistics computed from training data:


x_norm = (x - mean) / std


Why this matters:
- prevents dominance by large-magnitude features
- improves numerical stability
- allows consistent behavior in Unreal Engine

The same normalization constants are reused at runtime.

---

## 10. Why This Feature Set Works

This feature set succeeds because it:

- encodes **behavior**, not raw state
- distinguishes **intent vs instability**
- is robust to scale and frame rate
- remains interpretable
- is cheap to compute

Importantly, no single feature decides the outcome.  
The model learns a **weighted combination**, resulting in smooth, continuous behavior.

---

## 11. Limitations & Extensions

Current limitations:
- Translation and rotation features are trained separately
- Sliding window size is fixed
- Feature set is handcrafted

Possible extensions:
- per-axis feature weighting
- adaptive window sizing
- frequency-domain features (if latency allows)

These were intentionally deferred to keep the v1 system stable and understandable.

---

## 12. Summary

Feature engineering is the foundation of this system.

By designing features that reflect **how camera motion is perceived**, rather than how it is measured, the system can adapt smoothing intelligently without sacrificing responsiveness.

This balance is essential for virtual production workflows.
