import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from supertuxkart_il.agents.imitation_agent import ImitationAgent
from supertuxkart_il.environments.pytux_simple import SimplePyTux
from supertuxkart_il.utils.dataset import TrajectoryDataset
import numpy as np

def train(
    data_dir='data/trajectories',
    epochs=10,
    batch_size=32,
    lr=1e-3,
    val_split=0.1,
    device='cuda' if torch.cuda.is_available() else 'cpu',
):
    dataset = TrajectoryDataset(data_dir)
    n_val = int(len(dataset) * val_split)
    n_train = len(dataset) - n_val
    train_set, val_set = random_split(dataset, [n_train, n_val])
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size)
    model = ImitationAgent().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for img, vel, rot, act in train_loader:
            img = img.permute(0,3,1,2).float().to(device) / 255.0  # (B, C, H, W)
            vel = torch.tensor(vel, dtype=torch.float32).to(device)
            rot = torch.tensor(rot, dtype=torch.float32).to(device)
            act = torch.tensor(act, dtype=torch.float32).to(device)
            pred = model(img, vel, rot)
            loss = criterion(pred, act)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * img.size(0)
        train_loss /= len(train_loader.dataset)
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for img, vel, rot, act in val_loader:
                img = img.permute(0,3,1,2).float().to(device) / 255.0
                vel = torch.tensor(vel, dtype=torch.float32).to(device)
                rot = torch.tensor(rot, dtype=torch.float32).to(device)
                act = torch.tensor(act, dtype=torch.float32).to(device)
                pred = model(img, vel, rot)
                loss = criterion(pred, act)
                val_loss += loss.item() * img.size(0)
        if len(val_loader.dataset) > 0:
            val_loss /= len(val_loader.dataset)
        else:
            print("Aucune donnée de validation disponible, val_loss non calculé.")
        print(f"Epoch {epoch+1}/{epochs} | Train loss: {train_loss:.4f} | Val loss: {val_loss:.4f}")
    torch.save(model.state_dict(), 'imitation_agent.pth')
    print("Modèle sauvegardé sous imitation_agent.pth")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/trajectories')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    args = parser.parse_args()
    train(args.data_dir, args.epochs, args.batch_size, args.lr) 