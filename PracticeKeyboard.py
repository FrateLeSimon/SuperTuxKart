import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import time
import os
import keyboard
from datetime import datetime
import tkinter as tk
from threading import Thread

window_title = "SuperTuxKart"
capturing = False
start_time = None
tracked_keys = ["w", "a", "s", "d", "space", "shift"]

# Variables pour l'interface
recording_status = "En attente"
pressed_keys = []

# Fonction pour calculer le temps écoulé
def get_elapsed_time():
    if capturing and start_time:
        elapsed = int(time.time() - start_time)
        return f"{elapsed} secondes"
    return "0 secondes"

# Fonction pour mettre à jour l'interface
def update_gui():
    while True:
        if capturing:
            status_label.config(text="Enregistrement en cours", fg="green")
            time_elapsed_label.config(text=f"Temps écoulé : {get_elapsed_time()}")
        else:
            status_label.config(text="En attente", fg="red")
            time_elapsed_label.config(text="Temps écoulé : 0 secondes")
        
        keys_pressed_label.config(text=f"Touches pressées : {', '.join(pressed_keys) if pressed_keys else 'Aucune'}")
        root.update_idletasks()
        time.sleep(0.1)

# Fonction principale de capture
def start_capture():
    global capturing, start_time, pressed_keys

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
                start_time = time.time()
                time.sleep(0.5)

            if capturing and keyboard.is_pressed("m"):
                print("Capture arrêtée !")
                capturing = False
                time.sleep(0.5)

            if capturing:
                bbox = (game_window.left, game_window.top, game_window.width, game_window.height)
                screenshot = pyautogui.screenshot(region=bbox)
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                img_name = f"frame_{int(time.time() - start_time)}.jpg"
                img_path = os.path.join(images_dir, img_name)
                cv2.imwrite(img_path, frame)

                row = [img_name]
                pressed_keys = [k for k in tracked_keys if keyboard.is_pressed(k)]
                row += [str(int(k in pressed_keys)) for k in tracked_keys]

                labels_file.write(",".join(row) + "\n")
                labels_file.flush()

                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interruption clavier détectée.")
    finally:
        if 'labels_file' in locals():
            labels_file.close()
        print(f"Données enregistrées dans {dataset_dir}")

# Création de l'interface Tkinter
root = tk.Tk()
root.title("SuperTuxKart - Capture d'Écran")
root.geometry("450x350")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Styles
title_label = tk.Label(root, text="SuperTuxKart - Capture", font=("Arial", 18, "bold"), fg="#333", bg="#f0f0f0")
title_label.pack(pady=10)

status_frame = tk.Frame(root, bg="#f0f0f0")
status_frame.pack(pady=10)

status_label = tk.Label(status_frame, text="En attente", font=("Arial", 14), fg="red", bg="#f0f0f0")
status_label.pack()

time_elapsed_label = tk.Label(status_frame, text="Temps écoulé : 0 secondes", font=("Arial", 12), bg="#f0f0f0")
time_elapsed_label.pack()

keys_pressed_label = tk.Label(root, text="Touches pressées : Aucune", font=("Arial", 12), bg="#f0f0f0")
keys_pressed_label.pack(pady=10)

instructions_label = tk.Label(root, text="Appuyez sur 'P' pour démarrer, 'M' pour arrêter", font=("Arial", 10), fg="#555", bg="#f0f0f0")
instructions_label.pack(side="bottom", pady=10)

# Lancer la mise à jour de l'interface dans un thread séparé
Thread(target=update_gui, daemon=True).start()

# Lancer la capture dans un thread séparé
Thread(target=start_capture, daemon=True).start()

# Démarrer la boucle principale de l'interface
root.mainloop()