import os
import torch
import numpy as np
from supertuxkart_il.environments.pytux_simple import SimplePyTux
from pynput import keyboard

# Mapping clavier -> action SuperTuxKart [steer, acc, brake, drift]
KEYS = {
    'left': 0,   # steer -1
    'right': 1,  # steer +1
    'up': 2,     # acc
    'down': 3,   # brake
    'shift': 4   # drift
}

def get_action_from_keys(keys_pressed):
    # Action : [steer, acc, brake, drift]
    steer = 0.0
    acc = 0.0
    brake = 0.0
    drift = 0.0
    if 'left' in keys_pressed:
        steer -= 1.0
    if 'right' in keys_pressed:
        steer += 1.0
    if 'up' in keys_pressed:
        acc = 1.0
    if 'down' in keys_pressed:
        brake = 1.0
    if 'shift' in keys_pressed:
        drift = 1.0
    return np.array([steer, acc, brake, drift], dtype=np.float32)


def collect_human_trajectories(save_dir, n_episodes=1, max_steps=1000, track='lighthouse'):
    os.makedirs(save_dir, exist_ok=True)
    env = SimplePyTux(track=track, max_length=max_steps)
    keys_pressed = set()
    
    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                c = key.char.lower()
                if c == 'q':
                    keys_pressed.add('left')
                elif c == 'd':
                    keys_pressed.add('right')
                elif c == 'z':
                    keys_pressed.add('up')
                elif c == 's':
                    keys_pressed.add('down')
            elif key == keyboard.Key.space:
                keys_pressed.add('shift')
        except Exception:
            pass
    def on_release(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                c = key.char.lower()
                if c == 'q':
                    keys_pressed.discard('left')
                elif c == 'd':
                    keys_pressed.discard('right')
                elif c == 'z':
                    keys_pressed.discard('up')
                elif c == 's':
                    keys_pressed.discard('down')
            elif key == keyboard.Key.space:
                keys_pressed.discard('shift')
        except Exception:
            pass
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    print("Contrôle : ZQSD (direction/accélération/frein), espace (drift). Ferme la fenêtre ou attends la fin pour terminer l'épisode.")
    for ep in range(n_episodes):
        state = env.reset()
        episode_dir = os.path.join(save_dir, f'ep_{ep:03d}')
        os.makedirs(episode_dir, exist_ok=True)
        for t in range(max_steps):
            action = get_action_from_keys(keys_pressed)
            next_state, reward, done, _ = env.step(action)
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
                print(f"Épisode {ep+1} terminé après {t+1} étapes.")
                break
    env.close()
    listener.stop()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='data/human_trajectories')
    parser.add_argument('--episodes', type=int, default=1)
    parser.add_argument('--max_steps', type=int, default=1000)
    parser.add_argument('--track', type=str, default='lighthouse')
    args = parser.parse_args()
    collect_human_trajectories(args.save_dir, args.episodes, args.max_steps, args.track) 