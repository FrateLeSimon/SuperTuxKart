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

# Dataset personnalisé
class ImageCSVRegressionDataset(Dataset):
    def __init__(self, csv_file, images_dir, img_size=(224, 224), label_scaler=None):
        self.data = pd.read_csv(csv_file)
        self.images_dir = images_dir
        self.img_size = img_size
        self.transform = transforms.Compose([
            transforms.Resize(self.img_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self.image_names = self.data.iloc[:, 0].values
        self.labels = self.data.iloc[:, 1:].values.astype(np.float32)
        if label_scaler is None:
            self.label_scaler = MinMaxScaler()
            self.labels = self.label_scaler.fit_transform(self.labels)
        else:
            self.label_scaler = label_scaler
            self.labels = self.label_scaler.transform(self.labels)

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        img_path = os.path.join(self.images_dir, self.image_names[idx])
        image = Image.open(img_path).convert('RGB')
        image = self.transform(image)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return image, label

# Modèle CNN simple (ResNet18 modifié si dispo)
def get_model(output_dim):
    try:
        import torchvision.models as models
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, output_dim)
        return model
    except ImportError:
        # Fallback simple CNN
        return nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(32, output_dim)
        )

def main():
    parser = argparse.ArgumentParser(description='Train PyTorch model on image dataset with CSV labels')
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file')
    parser.add_argument('--images', type=str, required=True, help='Path to images directory')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--img_size', type=int, nargs=2, default=[224, 224])
    parser.add_argument('--save', type=str, default='model.pth', help='Path to save model')
    args = parser.parse_args()

    # Dataset et DataLoader
    dataset = ImageCSVRegressionDataset(args.csv, args.images, tuple(args.img_size))
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = get_model(dataset.labels.shape[1]).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(args.epochs):
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

    # Sauvegarde du modèle
    torch.save(model.state_dict(), args.save)
    print(f"Modèle sauvegardé sous {args.save}")

if __name__ == '__main__':
    main()
