# Summary of the Study: *Observation of the Evolution of Hide and Seek AI*

## Introduction

This study analyzes the emergence of complex behaviors in artificial intelligence agents within a competitive hide-and-seek environment. The work is inspired by OpenAI's research on multi-agent dynamics where strategies emerge without direct supervision, solely through reinforcement learning.

## Objective

The goal is to observe whether sophisticated strategies can naturally emerge in agents within a simple environment, using only basic reward signals. The hide-and-seek game serves as the framework for studying this dynamic.

## Methodology

- **Environment**: 3D simulation with agents, walls, blocks, and ramps.
- **Agents**:
  - *Hiders*: must hide from seekers.
  - *Seekers*: must find the hiders.
- **Learning**: each group of agents is trained using the PPO algorithm (Proximal Policy Optimization), without access to the opposing group’s strategies.
- **Rewards**:
  - Hiders gain points if they are not seen.
  - Seekers gain points if they spot a hider.
- **Autocurriculum**: the advancement of one group forces the other to adapt, creating a dynamic learning loop.

## Observed Results

Emergent behaviors unfold in several progressive stages:

1. **Random exploration**: agents move around without any clear strategy.
2. **Object manipulation**: hiders learn to use blocks to build shelters.
3. **Ramp usage**: seekers learn to place ramps to reach hiders' hiding spots.
4. **Counter-strategies**: hiders block ramps or trap them to prevent their use.

These behaviors are not manually programmed. They emerge solely through adaptation to victory conditions. Each innovation by one group triggers a countermeasure from the opposing group.

## Analysis

- **Hiders**:
  - Learn to cooperate.
  - Use the environment strategically.
  - Anticipate enemy movements.

- **Seekers**:
  - Learn to place ramps to overcome obstacles.
  - Identify risky or likely hiding areas.
  - Coordinate their exploration attempts (to a certain degree).

The study shows that competitive learning can generate behaviors similar to those observed in humans, including tool use, without explicitly programming these behaviors.

## Limitations

- Seekers' performance plateaus around 30%.
- Strategies are highly dependent on the simulated environment.
- Some behaviors are fragile: changes in scenario or object layout can break the learned strategies.

## Conclusion

The experiment demonstrates that in a competitive environment with simple rules, agents can autonomously develop complex behaviors. These results confirm the value of multi-agent environments and autocurriculum approaches for fostering the emergence of collective artificial intelligence, without human supervision.

## References

- Baker, B. et al. (2020). *Emergent Tool Use From Multi-Agent Autocurricula*. arXiv:1909.07528.
- Observation and reproduction carried out as part of a student project.
