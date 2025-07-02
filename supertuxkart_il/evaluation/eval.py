import torch
import numpy as np
from supertuxkart_il.agents.imitation_agent import ImitationAgent
from supertuxkart_il.environments.pytux_simple import SimplePyTux

def evaluate(model_path='imitation_agent.pth', n_episodes=5, max_steps=1000, track='lighthouse', device='cuda' if torch.cuda.is_available() else 'cpu'):
    env = SimplePyTux(track=track, max_length=max_steps)
    model = ImitationAgent().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    rewards = []
    steps = []
    for ep in range(n_episodes):
        state = env.reset()
        total_reward = 0
        for t in range(max_steps):
            img = torch.tensor(state['image']).permute(2,0,1).unsqueeze(0).float().to(device) / 255.0
            vel = torch.tensor(state['velocity']).unsqueeze(0).float().to(device)
            rot = torch.tensor(state['rotation']).unsqueeze(0).float().to(device)
            with torch.no_grad():
                action = model(img, vel, rot).cpu().numpy()[0]
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            state = next_state
            if done:
                break
        rewards.append(total_reward)
        steps.append(t+1)
        print(f"Episode {ep+1}: Reward={total_reward:.1f}, Steps={t+1}")
    print(f"Moyenne Reward: {np.mean(rewards):.1f} | Moyenne Steps: {np.mean(steps):.1f}")
    env.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default='imitation_agent.pth')
    parser.add_argument('--episodes', type=int, default=5)
    parser.add_argument('--max_steps', type=int, default=1000)
    parser.add_argument('--track', type=str, default='lighthouse')
    args = parser.parse_args()
    evaluate(args.model_path, args.episodes, args.max_steps, args.track) 