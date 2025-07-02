import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNNEncoder(nn.Module):
    def __init__(self, in_channels=3, feature_dim=128):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, 16, 5, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(16, 32, 5, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, 5, stride=2, padding=2),
            nn.ReLU(),
            nn.Flatten(),
        )
        self.fc = nn.Linear(64 * 16 * 12, feature_dim)  # pour image 128x96
    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class ImitationAgent(nn.Module):
    def __init__(self, feature_dim=128, action_dim=4):
        super().__init__()
        self.encoder = SimpleCNNEncoder()
        self.mlp = nn.Sequential(
            nn.Linear(feature_dim + 3 + 4, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )
    def forward(self, image, velocity, rotation):
        # image: (B, 3, 96, 128), velocity: (B,3), rotation: (B,4)
        x = self.encoder(image)
        x = torch.cat([x, velocity, rotation], dim=1)
        return self.mlp(x) 