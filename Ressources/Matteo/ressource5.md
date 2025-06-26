# An AI Approach for Analyzing Driving Behaviour in Simulated Racing Using Telemetry Data

## 📘 Introduction

This study addresses the growing demand for advanced analytics in **sim racing esports**. By applying **Artificial Intelligence (AI)** and **Machine Learning (ML)**, the authors analyze drivers' behavior using telemetry data gathered from a racing simulator. The aim is to identify performance patterns and driving styles, which can then support driver training and simulation software development.

## 🎯 Objectives

- Use telemetry data to objectively characterize sim racers' behavior.
- Apply machine learning to cluster racers into performance groups.
- Identify key metrics differentiating elite drivers from lower-skilled ones.
- Provide data-driven insight to improve racing performance.

## 🛠️ Apparatus

- **Simulator Setup**: ACC racing game + Logitech Pro racing hardware (wheel, gearbox, pedals).
- **Telemetry Tool**: MoTec i2 Pro software captures 84 data channels (e.g., speed, throttle, steering angle, etc.).
- **Participants**: 93 drivers; most held a driving license and had significant sim racing experience.

## 📊 Data Collection & Preprocessing

- **Sampling Rate**: 50Hz
- **Collected Files**:
  - Lap time summary
  - Channel statistics
  - Time-series telemetry data
- **Cleaning**:
  - Removed invalid laps and outliers.
  - Standardized lap data using custom normalization.
- **Final Dataset**: 557 laps after preprocessing.

## 🧪 Feature Engineering

Key telemetry-based features extracted per lap:
- **Control Metrics**: speed, throttle, brake, steering angle.
- **Behavioral Metrics**:
  - *Lane Deviation*: distance from centerline.
  - *Oversteer / Understeer*: inferred from wheel input and motion.
  - *Steering Reversal Rate*: number of direction changes.
  - *Trail Braking / Throttle Release*: timing and magnitude of input transitions.

## 📈 Results

### 1. Performance Level Analysis

- Used **K-means clustering** (k=2) to divide laps into FAST (elite) and SLOW (low skill) groups.
- **Accuracy**: 81.4%
- **Lap Time Stats**:
  - FAST: avg 89.9s (std 2.65)
  - SLOW: avg 102.9s (std 5.09)

### 2. Driving Pattern Analysis

- **Throttle/Brake**:
  - FAST drivers apply sharper throttle, release brakes later, and trail brake effectively.
- **Steering**:
  - FAST drivers show tighter lines and smoother wheel control.
- **Acceleration**:
  - Higher longitudinal and lateral acceleration in elite laps.
- **Over/Understeer**:
  - Understeer is more frequent in fast laps (managed deliberately).
  - Oversteer is minimized in elite performances.

### 3. Track Sector Observations

- Notable differences in corner handling (especially early corners).
- FAST drivers brake earlier, trail brake into corners, and apply throttle earlier.
- Less variance in the final track sector — most drivers behave similarly.

## ✅ Conclusion

- **AI and telemetry data** effectively model driver behavior in sim racing.
- Elite drivers distinguish themselves through:
  - Higher average speed
  - More aggressive but controlled input timing
  - Efficient use of throttle and brakes
- Findings can:
  - Improve driver training programs.
  - Optimize car setups.
  - Inform design of adaptive AI opponents.
  - Guide development of self-driving AI in simulations.

## 🔮 Future Work

- Analyze more varied tracks.
- Extend to **time-series prediction** (e.g., lap time forecasting).
- Apply insights to **autonomous vehicle training**.
