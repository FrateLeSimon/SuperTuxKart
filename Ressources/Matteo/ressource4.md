# Creating Multi-level AI Racing Agents Using a Combination of Imitation and Reinforcement Learning

## Introduction

This study explores the development of AI opponents for racing games using a combination of **Imitation Learning (IL)** and **Reinforcement Learning (RL)** within Unreal Engine 5. The primary objective is to design AI agents that behave like human players, offering varying levels of challenge.

Unlike prior work that often focused solely on either IL or RL, this paper combines both to improve realism and adaptability. The AI agents learn from real human racing data (via IL), and then refine their behaviors using RL through rewards and penalties.

## Objectives

- Mimic human driving behavior using imitation learning.
- Improve AI adaptability and performance via reinforcement learning.
- Use **cross-correlation** to match AI behavior to different player archetypes.
- Enable dynamic difficulty adjustment by creating AI agents of varying skill levels.

## Related Works

Three main areas of past work are reviewed:

1. **Fuzzy-Rule-Based Driving Architecture**: Modular and rule-based, but lacks adaptability.
2. **Cross-Correlation Analysis**: Used to measure behavioral similarity between NPCs and players.
3. **Deep Learning DDA**: Highly accurate but resource-intensive.

This research builds upon these foundations but emphasizes simplicity, interpretability, and resource-efficiency.

## Preliminaries

- **Unreal Engine 5**: Used to design and train AI agents through visual blueprints and prebuilt vehicle systems.
- **Cross-Correlation**: Employed to compare behavioral patterns between AI and human drivers (e.g., speed, deviation).
- **Rule-Based System**: Acts as a baseline method using conditional logic for driving behavior.

## Proposed Method

A hybrid architecture is proposed:

1. **Imitation Learning (IL)**: 
   - Collect player driving data (e.g., acceleration, braking, steering).
   - Train AI to mimic behavior using supervised learning.
   - Classify players into five skill levels (from novice to expert).

2. **Reinforcement Learning (RL)**:
   - AI receives rewards for staying on track and penalties for deviation.
   - RL fine-tunes behavior after IL training.
   - AI optimizes acceleration, braking, and steering via feedback loops.

3. **Cross-Correlation**:
   - Used post-training to evaluate similarity between AI and different player classes.

## Neural Network Details

- **Input**: Position, speed, direction, deviation.
- **Hidden Layer**: 1 layer with 8 neurons.
- **Output**: Acceleration, braking, and steering.
- **Activation Functions**:
  - Sigmoid for acceleration and braking.
  - Tanh for steering.
- **Optimizer**: Adam, using adaptive learning rates.

## Implementation

- **Rule-Based System**: Implemented using UE5 blueprints. Adjusts speed/steering based on track position and collisions.
- **Imitation Learning**: Uses collected human driving data to train AI agents by skill tier.
- **Reinforcement Learning**: Trained further using reward functions focused on track adherence.
- **Blueprint Tools**: Functions to record speed, deviation, and steering during races.

## Data Collection

- 10 players were recorded.
- Divided into training (Group 1) and testing (Group 2).
- Players classified by lap time into skill tiers.
- Data collected: acceleration, steering, and deviation from track.

## Results

- Cross-correlation graphs and heatmaps showed strong alignment between AI behavior and player archetypes.
- AI agents closely matched the styles of their respective training groups.
- An anomaly was found where "Above Average" AIs were less similar to "Expert" players than "Average" AIs. This was attributed to differing emphasis on deviation vs. speed.

## Analysis

- The hybrid model (IL + RL) produced AI agents that were more adaptable and realistic than rule-based or IL-only agents.
- Reinforcement learning refined the AI’s decision-making under dynamic race conditions.
- Cross-correlation confirmed the similarity between human and AI behaviors.

## Future Work

- Expand difficulty levels and player archetypes.
- Include more complex environments (e.g., weather, terrain).
- Integrate multi-objective RL (e.g., balancing speed and safety).
- Enhance reward structures (e.g., for overtaking).
- Explore multiplayer AI-human interactions.

## Conclusion

The combined IL + RL approach successfully created multi-tier AI racing agents that behave like human players. The model is resource-efficient, works well with UE5's blueprint tools, and is suitable for small development teams. The use of cross-correlation for validation is novel and effective. This method has strong potential for scalable and immersive AI design in racing games.

## References

This summary is based on the full paper available at:
[IEEE Xplore - DOI: 10.1109/COMPAS60761.2024.10796663](https://www.researchgate.net/publication/387238166)

Authors:
- Nafiz-Al-Rashid Sun
- Surovi Adlin Palma
- Fernaz Narin Nur
- Humayara Binte Rashid
- A. H. M. Saiful Islam
