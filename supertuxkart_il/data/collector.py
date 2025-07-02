import os
import torch
import numpy as np
from supertuxkart_il.environments.pytux_simple import SimplePyTux
from supertuxkart_il.baseline.simple_controller import SimpleExpertController

def collect_trajectories(save_dir, n_episodes=10, max_steps=1000, noise_std=0.05, track='lighthouse'):
    os.makedirs(save_dir, exist_ok=True)
    env = SimplePyTux(track=track, max_length=max_steps)
    expert = SimpleExpertController()
    for ep in range(n_episodes):
        state = env.reset()
        episode_dir = os.path.join(save_dir, f'ep_{ep:03d}')
        os.makedirs(episode_dir, exist_ok=True)
        for t in range(max_steps):
            action = expert.act(state, noise=noise_std)
            next_state, reward, done, _ = env.step(action)
            # Sauvegarde du couple (état, action)
            data = {
                'state': {
                    'image': state['image'],
                    'velocity': state['velocity'],
                    'rotation': state['rotation']
                },
                'action': action
            }
            torch.save(data, os.path.join(episode_dir, f'{t:04d}.pt'))
            state = next_state
            if done:
                break
    env.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='data/trajectories')
    parser.add_argument('--episodes', type=int, default=10)
    parser.add_argument('--max_steps', type=int, default=1000)
    parser.add_argument('--noise_std', type=float, default=0.05)
    parser.add_argument('--track', type=str, default='lighthouse')
    args = parser.parse_args()
    collect_trajectories(args.save_dir, args.episodes, args.max_steps, args.noise_std, args.track) 