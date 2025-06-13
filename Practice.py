import pygame
import pyautogui
import cv2
import numpy as np
import time
import os
from datetime import datetime

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

num_axes = joystick.get_numaxes()
num_buttons = joystick.get_numbuttons()
num_hats = joystick.get_numhats()

print(f"Axes: {num_axes}, Boutons: {num_buttons}, Hats: {num_hats}")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
dataset_dir = f"dataset/session_{timestamp}"
images_dir = os.path.join(dataset_dir, "images")
os.makedirs(images_dir, exist_ok=True)
labels_path = os.path.join(dataset_dir, "labels.csv")
labels_file = open(labels_path, "w")

header = ["image"]
header += [f"axis_{i}" for i in range(num_axes)]
header += [f"button_{i}" for i in range(num_buttons)]
header += [f"hat_{i}_x" for i in range(num_hats)]
header += [f"hat_{i}_y" for i in range(num_hats)]
labels_file.write(",".join(header) + "\n")

print("Appuie sur la flèche HAUT (d-pad up) pour démarrer la capture.")
print("Appuie sur la flèche BAS (d-pad down) pour arrêter la capture.")

capturing = False
frame_count = 0

try:
    while True:
        pygame.event.pump()

        # Lecture des hats (d-pad)
        dpad_x, dpad_y = joystick.get_hat(0) if num_hats > 0 else (0,0)

        if not capturing and dpad_y == 1:  # flèche haut pressée
            print("Capture démarrée !")
            capturing = True
            frame_count = 0
            time.sleep(0.5)  # anti-rebond

        if capturing and dpad_y == -1:  # flèche bas pressée
            print("Capture arrêtée !")
            capturing = False
            time.sleep(0.5)  # anti-rebond

        if capturing:
            screenshot = pyautogui.screenshot(region=(0, 40, 800, 600))
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
    labels_file.close()
    print(f"Données enregistrées dans {dataset_dir}")
