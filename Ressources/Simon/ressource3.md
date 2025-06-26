# Hierarchical Imitation Learning of Team Behavior from Heterogeneous Demonstrations

This work introduces DTIL (Deep Team Imitation Learner), a hierarchical multi-agent imitation learning framework designed to learn team behavior from heterogeneous and partially observable demonstrations. Unlike existing multi-agent imitation learning (MAIL) methods, which typically assume homogeneous behavior across agents and demonstrations, DTIL explicitly models the diversity and suboptimality of real-world team behaviors.

DTIL leverages a hierarchical structure for each agent, consisting of a high-level policy that selects discrete subtasks and a low-level policy that executes actions within those subtasks. The learning process follows an expectation-maximization (EM) procedure: in the E-step, latent subtask labels are inferred from demonstrations; in the M-step, both policy levels are updated using a distribution-matching approach, namely IQLearn, which avoids adversarial training and ensures scalability.

The method is grounded in a formal extension of the occupancy measure matching framework to multi-agent and partially observable settings. Theoretical results guarantee convergence and one-to-one correspondence between occupancy distributions and hierarchical policies, ensuring consistency even under partial supervision.

DTIL is evaluated in a variety of cooperative domains—such as Multi-Jobs, Movers and Flood, and SMACv2 (StarCraft II micromanagement scenarios)—and demonstrates clear advantages over existing baselines including behavior cloning, MA-GAIL, and MA-OptionGAIL. The approach proves particularly effective in capturing multimodal strategies and generalizing from imperfect, unlabeled demonstrations. Notably, DTIL is capable of learning meaningful team coordination even with only 20% of subtask labels provided during training.

In summary, DTIL offers a robust and interpretable framework for learning complex, multimodal team behaviors in realistic, partially observable environments. It addresses critical limitations of prior MAIL approaches and sets a foundation for future research in team modeling, imitation-based coaching, and real-world multi-agent systems.

