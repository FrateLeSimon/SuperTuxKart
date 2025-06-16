import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import time
import os
import keyboard
from datetime import datetime

window_title = "SuperTuxKart"
capturing = False
frame_count = 0

# Liste des touches à suivre (ajuste selon ton jeu)
tracked_keys = ["w", "a", "s", "d", "space", "shift"]

print("Appuie sur P pour démarrer la capture.")
print("Appuie sur M pour arrêter la capture.")

try:
    while True:
        if not capturing and keyboard.is_pressed("p"):
            try:
                game_window = next(w for w in gw.getWindowsWithTitle(window_title) if w.visible and w.title == window_title)
                print(f"Fenêtre trouvée : {game_window.title}")

                game_window.activate()
                game_window.restore()
                time.sleep(0.2)

                fixed_left = 600
                fixed_top = 0
                game_window.moveTo(fixed_left, fixed_top)
                print(f"Fenêtre déplacée à ({fixed_left},{fixed_top})")
            except StopIteration:
                raise RuntimeError(f"Aucune fenêtre visible avec le titre exact '{window_title}'.")

            # Préparation du dossier de session
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dataset_dir = f"dataset/keyboard_session_{timestamp}"
            images_dir = os.path.join(dataset_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            labels_path = os.path.join(dataset_dir, "labels.csv")
            labels_file = open(labels_path, "w")

            # En-tête CSV
            header = ["image"] + tracked_keys
            labels_file.write(",".join(header) + "\n")

            print("Capture démarrée !")
            capturing = True
            frame_count = 0
            time.sleep(0.5)

        if capturing and keyboard.is_pressed("m"):
            print("Capture arrêtée !")
            capturing = False
            time.sleep(0.5)

        if capturing:
            bbox = (game_window.left, game_window.top, game_window.width, game_window.height)
            screenshot = pyautogui.screenshot(region=bbox)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            img_name = f"frame_{frame_count}.jpg"
            img_path = os.path.join(images_dir, img_name)
            cv2.imwrite(img_path, frame)

            row = [img_name]
            row += [str(int(keyboard.is_pressed(k))) for k in tracked_keys]

            labels_file.write(",".join(row) + "\n")
            labels_file.flush()

            frame_count += 1
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Interruption clavier détectée.")
finally:
    if 'labels_file' in locals():
        labels_file.close()
    print(f"Données enregistrées dans {dataset_dir}")