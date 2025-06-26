# From Voxels to Victory: Enhancing Racing AI with Fuzzy DQN and Imitation Learning

## Introduction

This study investigates how to improve racing game AI using a hybrid approach that combines:

- Voxel-based feature extraction for better spatial understanding
- Fuzzy logic integrated into Deep Q-Learning (Fuzzy DQN)
- Imitation learning to accelerate early training

Racing games are increasingly used in AI research due to their real-time complexity, demand for optimal decision-making, and relevance to autonomous driving. Traditional AI methods often fail to balance exploration, performance, and adaptability.

---

## Methodology

### 1. Voxelized Track Feature Extraction

Rather than relying on handcrafted reward shaping, the authors introduce **automatic voxelization** of the track using an **octree structure**:

- The environment is divided into small 3D cubes (voxels)
- An optimal path is generated using the A* algorithm
- Rewards are assigned when the agent passes voxels in order

This creates a **dense and meaningful reward signal** that guides the agent through the track.

**Total reward formula:**

```
R_total = R_speed + R_toward + R_time + R_penalty + R_voxel
```

Where:
- `R_speed`: encourages high speed
- `R_toward`: rewards moving toward the goal
- `R_time`: penalizes long durations
- `R_penalty`: punishes going off-track
- `R_voxel`: rewards passing the correct voxels

---

### 2. Imitation Learning

Imitation learning is used to initialize the agent with expert-like behavior.

#### 2.1 Data Collection

An expert plays the game while data is logged:

```
τ = {(s₁, a₁), (s₂, a₂), ..., (s_T, a_T)}
```

Each pair consists of an observed state and the expert’s action.

#### 2.2 Behavioral Cloning

The AI learns to mimic the expert through supervised learning. The objective is to minimize the difference between its predicted action and the expert’s action:

```
J(θ) = Σ ||π_θ(s_t) - a_t||²
```

This allows faster convergence and gives the agent a strong initial policy before switching to reinforcement learning.

---

### 3. Fuzzy Deep Q-Network (Fuzzy DQN)

Fuzzy DQN introduces **fuzzy logic** into standard Deep Q-Networks to better handle uncertainty and non-linearity in decision-making.

#### 3.1 Fuzzy Noise Layer

- Introduces fuzziness in the action space during exploration
- Based on **Gaussian membership functions** to simulate varying degrees of truth

**Gaussian Membership Example:**

```
μ(x) = exp(- (x - c)² / (2σ²) )
```

#### 3.2 Fuzzy Rules and Inference

Actions are selected using a **weighted Q-value sum** across fuzzy sets:

```
Q_f(s, a) = Σ [ ω_i * Q_i(s, a) ]
```

This improves stability and avoids erratic behavior, especially during early training.

**Example fuzzy rules (speed strategy):**

| Fuzzy Set   | Speed Range     |
|-------------|------------------|
| Low         | 0–50 km/h        |
| Medium      | 50–100 km/h      |
| High        | 100–150 km/h     |
| Very High   | >150 km/h        |

---

## Experimental Results

### Reward Comparison (Custom vs. Baselines)

| Algorithm   | Performance Summary |
|-------------|---------------------|
| **Custom**  | Highest final reward (~400), fast convergence |
| **Q-Learning** | Steady improvement, slower than custom |
| **DQN**     | Less stable, lower peak reward |
| **SARSA**   | Weakest performance, unstable |

The proposed method outperforms all baselines in terms of reward, convergence speed, and training stability.

### Loss Curves

- Early phase: High and volatile loss
- After 10,000 steps: Loss stabilizes and gradually approaches zero
- Final phase: Low and stable loss values, showing successful learning

---

## Conclusion

The study presents a **robust hybrid method** that improves racing AI through:

- **Voxelized rewards**: Easy to generalize and compute, removes manual reward engineering
- **Imitation learning**: Speeds up training and gives stable early behavior
- **Fuzzy DQN**: Enhances decision-making under uncertainty, improves learning efficiency

This approach has strong potential not only in gaming but also in **real-world autonomous navigation** tasks.

---

## References

1. Fang Z.Y. (2023). *Active Tracking Based on Deep Reinforcement Learning*.
2. Duan et al. (2023). *Multi-agent Pathfinding Based on Deep Reinforcement Learning*.
3. Zang R. (2022). *Research on Multi-Agent Deep Reinforcement Learning*.
4. Zhang Y.T. (2021). *Obstacle Avoidance Based on Deep Reinforcement Learning*.
5. Gao Q. (2022). *Research on Deep Reinforcement Learning Algorithms*.
6. Wang et al. (2021). *Application of Fuzzy Neural Network in Autonomous Driving*.
