import argparse
import os
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import glob
import json

# Dataset multi-session
class ImageCSVRegressionDataset(Dataset):
    def __init__(self, dataset_root="dataset", img_size=(224, 224), label_scaler=None, used_sessions=None):
        self.img_size = img_size
        self.transform = transforms.Compose([
            transforms.Resize(self.img_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self.image_paths = []
        all_labels = []
        self.sessions_used = []
        for session_dir in glob.glob(os.path.join(dataset_root, "*")):
            session_name = os.path.basename(session_dir)
            if used_sessions and session_name in used_sessions:
                continue
            csv_path = os.path.join(session_dir, "labels.csv")
            images_dir = os.path.join(session_dir, "images")
            if os.path.isfile(csv_path) and os.path.isdir(images_dir):
                df = pd.read_csv(csv_path)
                for _, row in df.iterrows():
                    img_file = os.path.join(images_dir, row.iloc[0])
                    if os.path.isfile(img_file):
                        self.image_paths.append(img_file)
                        all_labels.append(row.iloc[1:].values.astype(np.float32))
                self.sessions_used.append(session_name)
        self.labels = np.array(all_labels, dtype=np.float32)
        if label_scaler is None:
            self.label_scaler = MinMaxScaler()
            self.labels = self.label_scaler.fit_transform(self.labels)
        else:
            self.label_scaler = label_scaler
            self.labels = self.label_scaler.transform(self.labels)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        image = self.transform(image)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return image, label

# Modèle CNN (avec fallback si torchvision n'est pas dispo)
def get_model(output_dim):
    try:
        import torchvision.models as models
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, output_dim)
        return model
    except ImportError:
        return nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(32, output_dim)
        )

def main():
    parser = argparse.ArgumentParser(description='Train PyTorch model on image dataset with CSV labels')
    parser.add_argument('--dataset', type=str, default='dataset')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--img_size', type=int, nargs=2, default=[224, 224])
    parser.add_argument('--save', type=str, default='model.pth')
    args = parser.parse_args()

    log_file = os.path.join(args.dataset, "used_sessions.json")
    if os.path.isfile(log_file):
        with open(log_file, "r") as f:
            used_sessions = set(json.load(f))
    else:
        used_sessions = set()

    dataset = ImageCSVRegressionDataset(args.dataset, tuple(args.img_size), used_sessions=used_sessions)
    if len(dataset) == 0:
        print("Aucune nouvelle donnée à entraîner. Arrêt.")
        return
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Modèle
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = get_model(dataset.labels.shape[1]).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.MSELoss()

    start_epoch = 0
    if os.path.isfile(args.save):
        print(f"🔁 Reprise depuis {args.save}")
        checkpoint = torch.load(args.save, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint.get('epoch', 0)
    else:
        print("🆕 Nouveau modèle initialisé")

    for epoch in range(start_epoch, args.epochs):
        model.train()
        running_loss = 0.0
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch+1}/{args.epochs} - Loss: {epoch_loss:.6f}")

        # Sauvegarde après chaque epoch
        torch.save({
            'epoch': epoch + 1,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, args.save)

    print(f"✅ Modèle final sauvegardé dans {args.save}")

    # Après entraînement, on met à jour le log
    if dataset.sessions_used:
        used_sessions.update(dataset.sessions_used)
        with open(log_file, "w") as f:
            json.dump(sorted(list(used_sessions)), f)

if __name__ == '__main__':
    main()
