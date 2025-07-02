import os
import torch
import numpy as np
from torch.utils.data import Dataset
import pickle

class TrajectoryDataset(Dataset):
    """
    Dataset pour charger les trajectoires (état, action) collectées par le contrôleur expert.
    Format attendu :
        - Un dossier par épisode
        - Dans chaque dossier, des fichiers .pt ou .pkl contenant :
            {
                'state': {
                    'image': np.array (H, W, C),
                    'velocity': np.array (3,),
                    'rotation': np.array (4,)
                },
                'action': np.array (4,)
            }
    """
    def __init__(self, data_dir, transform=None):
        self.samples = []
        self.transform = transform
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.pt') or file.endswith('.pkl'):
                    self.samples.append(os.path.join(root, file))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path = self.samples[idx]
        if path.endswith('.pt'):
            data = torch.load(path, weights_only=False)
        else:
            with open(path, 'rb') as f:
                data = pickle.load(f)
        state = data['state']
        action = data['action']
        image = state['image']
        if self.transform:
            image = self.transform(image)
        velocity = np.array(state['velocity'], dtype=np.float32)
        rotation = np.array(state['rotation'], dtype=np.float32)
        action = np.array(action, dtype=np.float32)
        return image, velocity, rotation, action 