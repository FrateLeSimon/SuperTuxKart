import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import time
import os
import keyboard
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from threading import Thread
import matplotlib.pyplot as plt  # Importer matplotlib

# Configuration globale
window_title = "SuperTuxKart"
capturing = False
start_time = None
tracked_keys = ["s", "d", "space", "shift", "q", "z", "c", "v"]

# Variables pour l'interface
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
            status_label.config(text="Enregistrement en cours", foreground="green")
            time_elapsed_label.config(text=f"Temps écoulé : {get_elapsed_time()}")
            start_button.config(state="disabled")
            stop_button.config(state="normal")
        else:
            status_label.config(text="En attente", foreground="red")
            time_elapsed_label.config(text="Temps écoulé : 0 secondes")
            start_button.config(state="normal")
            stop_button.config(state="disabled")
        
        keys_pressed_label.config(text=f"Touches pressées : {', '.join(pressed_keys) if pressed_keys else 'Aucune'}")
        root.update_idletasks()
        time.sleep(0.1)

# Fonction pour démarrer la capture
def start_capture_gui():
    global capturing, start_time
    if not capturing:
        capturing = True
        start_time = time.time()

# Fonction pour arrêter la capture
def stop_capture_gui():
    global capturing
    if capturing:
        capturing = False

# Listes pour stocker les timestamps
acceleration_data = []  # Pour la touche "Z"
braking_data = []       # Pour la touche "S"
drifting_data = []      # Pour la touche "Shift"

# Fonction principale de capture
def start_capture():
    global capturing, start_time, pressed_keys, acceleration_data, braking_data, drifting_data

    try:
        while True:
            if capturing:
                try:
                    # Activation de la fenêtre du jeu
                    game_window = next(w for w in gw.getWindowsWithTitle(window_title) if w.visible and w.title == window_title)
                    game_window.activate()
                    game_window.restore()
                    time.sleep(0.2)

                    # Positionnement de la fenêtre
                    fixed_left = 600
                    fixed_top = 0
                    game_window.moveTo(fixed_left, fixed_top)
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

                while capturing:
                    bbox = (game_window.left, game_window.top, game_window.width, game_window.height)
                    screenshot = pyautogui.screenshot(region=bbox)
                    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    img_name = f"frame_{int(time.time() - start_time)}.jpg"
                    img_path = os.path.join(images_dir, img_name)
                    cv2.imwrite(img_path, frame)

                    # Enregistrement des touches pressées
                    row = [img_name]
                    pressed_keys = [k for k in tracked_keys if keyboard.is_pressed(k)]
                    row += [str(int(k in pressed_keys)) for k in tracked_keys]

                    # Si la touche "Z" (accélération) est pressée, enregistrer le timestamp
                    if "z" in pressed_keys:
                        acceleration_data.append(time.time() - start_time)

                    # Si la touche "S" (freinage) est pressée, enregistrer le timestamp
                    if "s" in pressed_keys:
                        braking_data.append(time.time() - start_time)

                    # Si la touche "Shift" (dérapage) est pressée, enregistrer le timestamp
                    if "shift" in pressed_keys:
                        drifting_data.append(time.time() - start_time)

                    labels_file.write(",".join(row) + "\n")
                    labels_file.flush()

                    time.sleep(0.1)

                labels_file.close()

                # Appeler la fonction pour afficher et enregistrer le graphique
                show_acceleration_graph(dataset_dir)

    except KeyboardInterrupt:
        print("Interruption clavier détectée.")
    finally:
        if 'labels_file' in locals():
            labels_file.close()

# Fonction pour afficher le graphique
def show_acceleration_graph(session_dir):
    if not (acceleration_data or braking_data or drifting_data):
        print("Aucune donnée enregistrée.")
        return

    plt.figure(figsize=(10, 5))

    # Graphique pour l'accélération
    if acceleration_data:
        times_acceleration = [t for t in acceleration_data]
        values_acceleration = [1] * len(acceleration_data)
        plt.scatter(times_acceleration, values_acceleration, color="blue", label="Accélération (Z)")

    # Graphique pour le freinage
    if braking_data:
        times_braking = [t for t in braking_data]
        values_braking = [2] * len(braking_data)
        plt.scatter(times_braking, values_braking, color="red", label="Freinage (S)")

    # Graphique pour le dérapage
    if drifting_data:
        times_drifting = [t for t in drifting_data]
        values_drifting = [3] * len(drifting_data)
        plt.scatter(times_drifting, values_drifting, color="green", label="Dérapage (Shift)")

    # Configuration du graphique
    plt.xlabel("Temps écoulé (secondes)")
    plt.ylabel("Actions (1 = Accélération, 2 = Freinage, 3 = Dérapage)")
    plt.title("Graphique des actions (Accélération, Freinage, Dérapage)")
    plt.legend()
    plt.grid(True)

    # Enregistrer le graphique dans le dossier de la session
    graph_path = os.path.join(session_dir, "graph.png")
    plt.savefig(graph_path)
    print(f"Graphique enregistré : {graph_path}")

    # Afficher le graphique
    plt.show()

# Création de l'interface Tkinter
root = tk.Tk()
root.title("SuperTuxKart - Capture d'Écran")
root.geometry("600x600")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 12))

# Titre
title_label = tk.Label(root, text="SuperTuxKart - Capture", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
title_label.pack(pady=20)

# Statut
status_frame = tk.Frame(root, bg="#2c3e50")
status_frame.pack(pady=10)

status_label = tk.Label(status_frame, text="En attente", font=("Arial", 16), bg="#2c3e50", fg="red")
status_label.pack()

time_elapsed_label = tk.Label(status_frame, text="Temps écoulé : 0 secondes", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
time_elapsed_label.pack()

# Touches pressées
keys_pressed_label = tk.Label(root, text="Touches pressées : Aucune", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
keys_pressed_label.pack(pady=10)

# Boutons
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=20)

start_button = ttk.Button(button_frame, text="Démarrer", command=start_capture_gui)
start_button.grid(row=0, column=0, padx=10)

stop_button = ttk.Button(button_frame, text="Arrêter", command=stop_capture_gui, state="disabled")
stop_button.grid(row=0, column=1, padx=10)

# Bouton pour afficher le graphique
graph_button = ttk.Button(button_frame, text="Afficher le graphique", command=show_acceleration_graph)
graph_button.grid(row=0, column=2, padx=10)

# Instructions sur les touches avec tableau
instructions_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10)
instructions_frame.pack(pady=20, fill="both", expand=True)

instructions_title = tk.Label(instructions_frame, text="Touches disponibles :", font=("Arial", 14, "bold"), bg="#34495e", fg="#ecf0f1")
instructions_title.pack(anchor="w")

columns = ["Action", "Touche assignée"]
data = [
    ("Tourner à gauche", "Q"),
    ("Tourner à droite", "D"),
    ("Accélérer", "Z"),
    ("Frein / Reculer", "S"),
    ("Tirer", "C"),
    ("Nitro", "Espace"),
    ("Dérapage", "Shift gauche"),
    ("Regarder en arrière", "V"),
]

table = ttk.Treeview(instructions_frame, columns=columns, show="headings", height=10)
table.heading("Action", text="Action")
table.heading("Touche assignée", text="Touche assignée")

for action, key in data:
    table.insert("", "end", values=(action, key))

table.pack(fill="both", expand=True)

# Lancer la mise à jour de l'interface dans un thread séparé
Thread(target=update_gui, daemon=True).start()

# Lancer la capture dans un thread séparé
Thread(target=start_capture, daemon=True).start()

# Démarrer la boucle principale de l'interface
root.mainloop()