import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import pygame
import time
import os
from train_model import get_model
import pygetwindow as gw
import pyautogui

from pyvigem.common import DS4_BUTTONS
from pyvigem.client import VigemClient
from pyvigem.target import DS4Controller

MODEL_PATH = 'model.pth'
IMG_SIZE = (224, 224)
CAPTURE_REGION = (600, 0, 800, 600)  # à adapter selon ton écran

# Initialisation de la manette physique (PS4 en entrée)
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Chargement du modèle
checkpoint = torch.load(MODEL_PATH, map_location='cpu')
output_dim = checkpoint['model_state_dict']['fc.weight'].shape[0] if 'fc.weight' in checkpoint['model_state_dict'] else checkpoint['model_state_dict']['4.weight'].shape[0]
model = get_model(output_dim)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Transformation image
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# Initialisation de la manette virtuelle DS4
client = VigemClient()
client.connect()

ds4 = DS4Controller(client)
ds4.connect()

def predict_action(image):
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        return output[0].cpu().numpy()

def apply_action(prediction, num_axes=2, num_buttons=4):
    axes = prediction[:num_axes]
    buttons = prediction[num_axes:num_axes+num_buttons]

    # Joystick gauche
    lx = int(np.clip((axes[0] + 1) / 2 * 255, 0, 255))  # de -1/1 vers 0/255
    ly = int(np.clip((1 - axes[1]) / 2 * 255, 0, 255))  # inversé pour Y

    ds4.left_joystick(x=lx, y=ly)

    # Bouton croix (X sur PS4)
    if buttons[0] > 0.5:
        ds4.press_button(DS4_BUTTONS.CROSS)
    else:
        ds4.release_button(DS4_BUTTONS.CROSS)

    # Bouton carré (Carré sur PS4)
    if buttons[1] > 0.5:
        ds4.press_button(DS4_BUTTONS.SQUARE)
    else:
        ds4.release_button(DS4_BUTTONS.SQUARE)

    ds4.update()

def main():
    print("Appuie sur le d-pad haut pour démarrer l'IA, bas pour arrêter.")
    running = False
    try:
        while True:
            pygame.event.pump()
            _, dpad_y = joystick.get_hat(0)

            if not running and dpad_y == 1:
                running = True
                print("IA démarrée !")
                time.sleep(0.3)
            elif running and dpad_y == -1:
                running = False
                print("IA arrêtée !")
                time.sleep(0.3)

            if running:
                screenshot = pyautogui.screenshot(region=CAPTURE_REGION)
                image = Image.fromarray(np.array(screenshot))
                prediction = predict_action(image)
                apply_action(prediction)
                time.sleep(0.05)pip
                ds4.left_joystick(x=128, y=128)  # position neutre
                ds4.release_button(DS4_BUTTONS.CROSS)
                ds4.release_button(DS4_BUTTONS.SQUARE)
                ds4.update()
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Arrêt manuel.")
    finally:
        ds4.disconnect()
        client.disconnect()

if __name__ == "__main__":
    main()
