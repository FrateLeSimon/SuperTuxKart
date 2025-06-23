## MEGA-DAgger: Imitation Learning with Multiple Imperfect Experts

MEGA-DAgger is an imitation learning framework designed to leverage multiple imperfect experts in high-risk environments, such as autonomous driving. The method addresses key limitations of traditional approaches like DAgger and HG-DAgger, which assume access to a single, reliable expert. In practice, expert demonstrations are often noisy, inconsistent, or suboptimal.

The goal of MEGA-DAgger is to learn a policy that can match—or outperform—the best available experts, while minimizing risky behavior. To achieve this, the method introduces three core mechanisms: safety-based data filtering, expert action conflict resolution, and dynamic expert selection.

The **first mechanism**, filtering, relies on Control Barrier Functions (CBFs) to evaluate the safety of demonstrations. If an expert performs an unsafe maneuver (e.g., too close to an obstacle, excessive speed), the demonstration is truncated and excluded from the training dataset. This prevents unsafe transitions from contaminating the learning process.

The **second mechanism** resolves action conflicts between experts. At a given time step, multiple experts may propose different actions. MEGA-DAgger compares the current observation (e.g., LiDAR scan) to past states using cosine similarity. It then selects the most appropriate action using a composite score that balances safety (CBF-based) and efficiency (progress toward the goal).

The **third mechanism** is a dynamic expert selection strategy. At each iteration, MEGA-DAgger identifies which expert performs best under current environmental conditions. The choice may vary depending on track layout, traffic density, or noise. This adaptive strategy makes it possible to extract complementary strengths from different experts rather than averaging their behaviors.

The authors evaluate MEGA-DAgger in a realistic racing simulator (f1tenth-gym), using neural-network-based agents trained on raw LiDAR data. Experimental results show that MEGA-DAgger significantly outperforms baseline methods such as HG-DAgger across several metrics: collision rate, successful lap completions, average speed, and robustness. In some cases, the learned policy even exceeds the performance of individual experts, demonstrating intelligent behavior aggregation.

The method is also validated on a real F1TENTH physical robot, confirming its applicability beyond simulation. The paper concludes by suggesting future extensions, such as learning expert trust scores automatically or integrating human experts in the loop.

In summary, MEGA-DAgger is a robust and scalable solution for imitation learning in uncertain environments. By intelligently aggregating demonstrations from diverse and imperfect sources, it enables high-performing, safe, and generalizable autonomous agents—without requiring explicit reward engineering.
