# Summary of the Study: *Les recherches de VICO*

## Introduction

This master's thesis explores the application of artificial intelligence (AI), specifically *narrow AI*, in video game development. The focus is on the **Drivatar** system used in *Forza Motorsport*, a racing game series developed by Turn10 Studios in partnership with Microsoft. The Drivatar simulates human driving behavior using machine learning, creating an illusion of human presence during gameplay.

## Objective

The goal is to analyze how narrow AI systems can generate realistic emotional responses and powerful affective illusions in players—particularly during individual competition against the machine.

## Methodology

The work is structured around three core chapters:

- **Foundational Concepts**:
  - Defines key terms: video games, artificial intelligence, computing systems, and machine learning.
  - Sets the general technological context.

- **Evolution of Video Game Development**:
  - Reviews the history of video games from analog beginnings to the modern digital era.
  - Highlights technological and conceptual innovations, including NPCs and virtual bots.

- **Narrow AI and Strong Emotions**:
  - Focuses on multiple specialized narrow AI systems interacting to simulate realistic human behavior.
  - Drivatar is the centerpiece: it faithfully reproduces and predicts human driving behavior, fostering social and emotional engagement.

## Case Study: *Forza Motorsport*'s Drivatar

The Drivatar leverages large-scale data collection and complex algorithms to:

- Learn individual player styles.
- Predict future behavior.
- Create compelling and emotionally resonant gameplay.

Players feel as if they're racing against real humans, not just scripted AI.

## Additional Summaries

### Racing Game AI – Artificial Intelligence for Games

This part outlines five key AI aspects in racing games:

1. **Track Representation**:
   - Node-based vs. geometrically sector-based designs for flexible and realistic paths.

2. **Racing Lines**:
   - Use of expert-recorded or dynamically generated optimal paths based on game conditions.

3. **Vehicle Driving Models**:
   - Neural networks and systems like Drivatar replicate human-like control and driving behavior.

4. **AI Vehicle Tuning**:
   - Genetic algorithms or expert systems optimize car settings depending on track and weather.

5. **Spectator and Pedestrian Simulation**:
   - Finite state machines, flocking behavior, and scripted animations create lively and responsive game environments.

### Machine Learning and Games

This section explores the synergy between games and machine learning, showing how games are both platforms for AI research and beneficiaries of it:

- **Learning in Games**: e.g., TD-Gammon.
- **Player Modeling**: predicting and adapting to human behavior.
- **Behavior Capture**: intelligent avatars that imitate players (like Drivatar).
- **Model Robustness**: interpretable and stable predictive systems.
- **Dynamic Difficulty Adjustment**: adapting gameplay to user skill levels.
- **Explainability**: allowing AI to justify its decisions to players.
- **Resource Management**: efficient real-time AI computation.

Examples include *Neverwinter Nights*, *Omaha Poker*, *Bridge*, and *Chess*.

### Data Quality in Imitation Learning

Focuses on the importance of high-quality training data in **imitation learning (IL)**, particularly for robotics:

- **Problem**: Distributional shift between training and test phases due to compounded prediction errors.

- **Two Key Properties**:
  - **Action Divergence**: difference between expert and learned policy.
  - **Transition Diversity**: variety in system states for a given action (too much noise harms learning).

- **Recommendations**:
  - Ensure action consistency to minimize divergence.
  - Introduce moderate noise to promote useful diversity without information loss.

This provides a formal and practical framework for improving IL data quality.

## Conclusion

Across multiple chapters and case studies, the document reveals how **narrow AI systems**, like Drivatar, successfully simulate emotionally impactful and realistic behaviors in video games. Through smart data use and algorithmic complexity, these systems create immersive and socially resonant gaming experiences that blur the line between virtual and real.
