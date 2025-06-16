import pygame
import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import time
import os
from datetime import datetime

# Configuration
START_BUTTON_INDEX = 11  # PS4: bouton pour D-pad haut
STOP_BUTTON_INDEX = 12   # PS4: bouton pour D-pad bas
window_title = "SuperTuxKart"

# Initialisation de la manette
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

num_axes = joystick.get_numaxes()
num_buttons = joystick.get_numbuttons()
num_hats = joystick.get_numhats()

print(f"Manette détectée : {joystick.get_name()}")
print(f"Axes: {num_axes}, Boutons: {num_buttons}, Hats: {num_hats}")
print("Appuie sur BOUTON 11 (D-pad haut) pour démarrer, BOUTON 12 (D-pad bas) pour arrêter.")

capturing = False
frame_count = 0
labels_file = None
dataset_dir = None
images_dir = None
game_window = None

try:
    while True:
        pygame.event.pump()

        start_pressed = joystick.get_button(START_BUTTON_INDEX)
        stop_pressed = joystick.get_button(STOP_BUTTON_INDEX)

        if not capturing and start_pressed:
            try:
                game_window = next(w for w in gw.getWindowsWithTitle(window_title) if w.visible and w.title == window_title)
                print(f"Fenêtre trouvée : {game_window.title}")

                # Mettre la fenêtre au premier plan
                game_window.activate()
                game_window.restore()
                time.sleep(0.2)

                # Déplacement de la fenêtre à une position fixe
                fixed_left = 600
                fixed_top = 0
                game_window.moveTo(fixed_left, fixed_top)
                print(f"Fenêtre déplacée à ({fixed_left}, {fixed_top})")

            except StopIteration:
                raise RuntimeError(f"Aucune fenêtre visible avec le titre exact '{window_title}'.")

            # Création des dossiers
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dataset_dir = f"dataset/session_{timestamp}"
            images_dir = os.path.join(dataset_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            labels_path = os.path.join(dataset_dir, "labels.csv")
            labels_file = open(labels_path, "w")

            # Écriture en-tête CSV
            header = ["image"]
            header += [f"axis_{i}" for i in range(num_axes)]
            header += [f"button_{i}" for i in range(num_buttons)]
            header += [f"hat_{i}_x" for i in range(num_hats)]
            header += [f"hat_{i}_y" for i in range(num_hats)]
            labels_file.write(",".join(header) + "\n")

            print("Capture démarrée !")
            capturing = True
            frame_count = 0
            time.sleep(0.4)  # anti-rebond

        if capturing and stop_pressed:
            print("Capture arrêtée !")
            capturing = False
            time.sleep(0.4)

        if capturing:
            bbox = (game_window.left, game_window.top, game_window.width, game_window.height)
            screenshot = pyautogui.screenshot(region=bbox)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            img_name = f"frame_{frame_count}.jpg"
            img_path = os.path.join(images_dir, img_name)
            cv2.imwrite(img_path, frame)

            row = [img_name]
            row += [f"{joystick.get_axis(i):.3f}" for i in range(num_axes)]
            row += [str(joystick.get_button(i)) for i in range(num_buttons)]
            for i in range(num_hats):
                hat = joystick.get_hat(i)
                row.append(str(hat[0]))
                row.append(str(hat[1]))

            labels_file.write(",".join(row) + "\n")
            labels_file.flush()

            frame_count += 1
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Interruption clavier détectée.")
finally:
    if labels_file:
        labels_file.close()
    print(f"Données enregistrées dans {dataset_dir}" if dataset_dir else "Aucune donnée enregistrée.")
