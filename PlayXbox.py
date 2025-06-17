import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import pygame
import time
import os
from train_model import get_model
import vgamepad as vg
import pygetwindow as gw
import pyautogui

MODEL_PATH = 'model.pth'
IMG_SIZE = (224, 224)
WINDOW_TITLE = "SuperTuxKart"
CAPTURE_REGION = (600, 0, 800, 600)  # (left, top, width, height) à adapter si besoin

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

# Charger le modèle
checkpoint = torch.load(MODEL_PATH, map_location='cpu')
output_dim = checkpoint['model_state_dict']['fc.weight'].shape[0] if 'fc.weight' in checkpoint['model_state_dict'] else checkpoint['model_state_dict']['4.weight'].shape[0]
model = get_model(output_dim)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

gamepad = vg.VX360Gamepad()

def predict_action(image):
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        prediction = output[0].cpu().numpy()
    return prediction

def apply_action(prediction, num_axes=2, num_buttons=4):
    axes = prediction[:num_axes]
    buttons = prediction[num_axes:num_axes+num_buttons]
    lx = int(np.clip(axes[0], -1, 1) * 32767)
    ly = int(-np.clip(axes[1], -1, 1) * 32767)
    gamepad.left_joystick(x_value=lx, y_value=ly)
    if num_buttons > 0:
        if buttons[0] > 0.5:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    if num_buttons > 1:
        if buttons[1] > 0.5:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()

def main():
    print("Appuie sur la flèche HAUT (d-pad) de la manette pour démarrer l'IA, BAS pour arrêter.")
    running = False
    try:
        while True:
            pygame.event.pump()
            dpad_y = 0
            if joystick is not None and joystick.get_numhats() > 0:
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
                time.sleep(0.05)
            else:
                gamepad.left_joystick(x_value=0, y_value=0)
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.update()
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Arrêt manuel.")
        gamepad.left_joystick(x_value=0, y_value=0)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()

if __name__ == "__main__":
    main()
