## Imitation Learning for Autonomous Agents in SuperTuxKart Ice Hockey

### Introduction

This work explores the application of imitation learning (IL) and Dataset Aggregation (DAgger) to train autonomous agents in the competitive ice hockey mode of the open-source video game SuperTuxKart. Unlike traditional approaches relying on human demonstrations, this study leverages a built-in AI agent as an expert, aiming to replicate its behavior through supervised learning. The investigation evaluates whether purely observational learning is sufficient to generate competent in-game policies and identifies the limits of these techniques in multi-agent video game settings.

---

### Expert Selection and Data Generation

To establish a reliable expert policy, five built-in AI agents (referred to as TA agents) were evaluated through a round-robin tournament. The agent with the highest average goals and win rate, “jurgen,” was selected as the expert.

Demonstration data were collected by observing jurgen playing multiple matches against other agents. Each game state was encoded as an 11-dimensional feature vector capturing the relative positions, velocities, and angular relationships between the agent, its teammate, the puck, and opponents. The corresponding expert actions—acceleration, steering, and braking—were recorded. Only games where the expert successfully scored were retained for training, yielding a dataset of 20 successful matches.

---

### Supervised Imitation Learning

A fully connected neural network was trained on the collected dataset using supervised learning. The architecture consisted of two hidden layers with ReLU activations and dropout, taking the 11-dimensional feature input and outputting three continuous action values. The model was trained with the Adam optimizer and mean squared error loss over 75 epochs. Validation loss stabilized around 0.14–0.15, indicating reasonable generalization despite the modest dataset size.

---

### Dataset Aggregation (DAgger)

To address the covariate shift issue inherent in supervised IL, DAgger was employed. After training the initial imitation agent, a secondary dataset was constructed by allowing the agent to act autonomously, while querying the expert at each timestep to collect corrective actions. This aggregated dataset was then used to train a new agent with the same architecture. Training was stopped after 50 epochs due to convergence.

---

### Evaluation Protocol

Five policy configurations were tested, including:
- Two identical imitation-learned agents,
- Two independently trained imitation agents,
- Two identical DAgger-trained agents,
- A hybrid configuration (one imitation, one DAgger),
- Two independently trained DAgger agents.

Each policy configuration was evaluated across 32 games against a set of standard TA opponents. Metrics included goal-scoring performance and qualitative behavior analysis.

---

### Results

The best performance was achieved by two independently trained imitation agents, scoring 18 goals in 32 games—still far below the expert agent’s average of over 2.0 goals per game. Surprisingly, DAgger-trained policies performed significantly worse, often failing to score. The results suggest that, in this setup, pure imitation learning was more effective than DAgger, contradicting common expectations from the literature.

The observed failure of DAgger may stem from insufficient coverage of diverse states in the aggregated dataset, poor generalization of expert corrections, or lack of exploration during data collection.

---

### Discussion and Future Work

The study highlights the effectiveness of basic imitation learning when applied to a controlled, low-dimensional feature space extracted from game states. However, it also underscores the difficulty of leveraging DAgger without careful design, particularly in dynamic, multi-agent environments.

Several directions are proposed to enhance performance:
- Using recurrent neural networks (RNNs) to exploit temporal dependencies,
- Training a centralized multi-agent controller to encourage collaboration,
- Pretraining with imitation learning followed by DAgger fine-tuning,
- Augmenting data collection with noise or synthetic state generation.

---

### Conclusion

This work demonstrates the feasibility of training autonomous video game agents via imitation learning using AI experts instead of humans. While performance remained below that of the expert agent, the approach achieved non-trivial results. The study further reveals that DAgger may not always outperform supervised IL in practice, particularly when data coverage and correction strategies are limited. These insights are valuable for future work in agent training in complex interactive game environments.
