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
from threading import Thread, Lock
import matplotlib.pyplot as plt
from collections import deque
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration globale
WINDOW_TITLE = "SuperTuxKart"
CAPTURE_INTERVAL = 0.1  # secondes
GUI_UPDATE_INTERVAL = 0.1  # secondes

# Configuration de position de la fenêtre de jeu
WINDOW_FIXED_LEFT = 675     # Position X (600 pixels du bord gauche)
WINDOW_FIXED_TOP = 0        # Position Y (0 pixels du bord haut)
WINDOW_WIDTH = 1254         # Largeur souhaitée (optionnel)
WINDOW_HEIGHT = 1029         # Hauteur souhaitée (optionnel)

# Configuration pour le positionnement automatique
AUTO_POSITION_ON_STARTUP = True    # Active le repositionnement automatique au démarrage
STARTUP_DELAY = 1.0                # Délai en secondes avant le repositionnement

# Configuration de l'interface utilisateur
GUI_WIDTH = 650
GUI_HEIGHT = 960
GUI_POSITION_X = 10         # Position X de l'interface
GUI_POSITION_Y = 10         # Position Y de l'interface

# Variables d'état avec thread safety
capturing = False
start_time = None
tracked_keys = ["s", "d", "space", "shift", "q", "z", "c", "v"]
pressed_keys = []
data_lock = Lock()

# Utilisation de deque pour de meilleures performances
acceleration_data = deque()
braking_data = deque()
drifting_data = deque()

# Fonction pour calculer le temps écoulé
def get_elapsed_time():
    """Calcule le temps écoulé depuis le début de la capture."""
    if capturing and start_time:
        elapsed = int(time.time() - start_time)
        return f"{elapsed} secondes"
    return "0 secondes"

class GameWindowManager:
    """Gestionnaire pour la fenêtre de jeu avec contrôle avancé."""
    
    @staticmethod
    def find_and_activate_window():
        """Trouve et active la fenêtre du jeu avec positionnement et dimensionnement."""
        try:
            game_window = next(
                w for w in gw.getWindowsWithTitle(WINDOW_TITLE) 
                if w.visible and w.title == WINDOW_TITLE
            )
            
            # Activer et restaurer la fenêtre
            game_window.activate()
            game_window.restore()
            time.sleep(0.2)
            
            # Positionner la fenêtre
            game_window.moveTo(WINDOW_FIXED_LEFT, WINDOW_FIXED_TOP)
            
            # Redimensionner si nécessaire (optionnel)
            try:
                game_window.resizeTo(WINDOW_WIDTH, WINDOW_HEIGHT)
                logger.info(f"Fenêtre redimensionnée à {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            except Exception as e:
                logger.warning(f"Impossible de redimensionner la fenêtre : {e}")
            
            logger.info(f"Fenêtre positionnée à ({WINDOW_FIXED_LEFT}, {WINDOW_FIXED_TOP})")
            return game_window
            
        except StopIteration:
            raise RuntimeError(f"Aucune fenêtre visible avec le titre exact '{WINDOW_TITLE}'.")
    
    @staticmethod
    def auto_position_at_startup():
        """Positionne automatiquement la fenêtre du jeu au démarrage de l'application."""
        try:
            game_window = next(
                w for w in gw.getWindowsWithTitle(WINDOW_TITLE) 
                if w.visible and w.title == WINDOW_TITLE
            )
            
            # Restaurer la fenêtre si elle est minimisée
            if game_window.isMinimized:
                game_window.restore()
                time.sleep(0.3)
            
            # Positionner la fenêtre
            game_window.moveTo(WINDOW_FIXED_LEFT, WINDOW_FIXED_TOP)
            
            # Redimensionner si nécessaire
            try:
                game_window.resizeTo(WINDOW_WIDTH, WINDOW_HEIGHT)
                logger.info(f"✅ Fenêtre SuperTuxKart positionnée automatiquement : {WINDOW_WIDTH}x{WINDOW_HEIGHT} à ({WINDOW_FIXED_LEFT}, {WINDOW_FIXED_TOP})")
            except Exception as e:
                logger.warning(f"⚠️ Impossible de redimensionner automatiquement : {e}")
            
            return True
            
        except StopIteration:
            logger.warning(f"⚠️ Fenêtre SuperTuxKart non trouvée au démarrage. Lancez le jeu d'abord.")
            return False
    
    @staticmethod
    def get_window_info():
        """Retourne les informations sur la fenêtre de jeu."""
        try:
            game_window = next(
                w for w in gw.getWindowsWithTitle(WINDOW_TITLE) 
                if w.visible and w.title == WINDOW_TITLE
            )
            return {
                "title": game_window.title,
                "left": game_window.left,
                "top": game_window.top,
                "width": game_window.width,
                "height": game_window.height,
                "visible": game_window.visible,
                "minimized": game_window.isMinimized,
                "maximized": game_window.isMaximized,
                "active": game_window.isActive
            }
        except StopIteration:
            return None

class DataCollector:
    """Collecteur de données pour les actions du joueur."""
    
    def __init__(self):
        self.session_dir = None
        self.labels_file = None
        self.frame_count = 0
    
    def setup_session(self):
        """Configure le répertoire de session et les fichiers."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = f"dataset/keyboard_session_{timestamp}"
        images_dir = os.path.join(self.session_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        labels_path = os.path.join(self.session_dir, "labels.csv")
        self.labels_file = open(labels_path, "w")
        
        header = ["image"] + tracked_keys
        self.labels_file.write(",".join(header) + "\n")
        
        logger.info(f"Session créée : {self.session_dir}")
        return images_dir
    
    def capture_frame_and_input(self, game_window, images_dir):
        """Capture une frame et enregistre les inputs."""
        bbox = (game_window.left, game_window.top, game_window.width, game_window.height)
        screenshot = pyautogui.screenshot(region=bbox)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        img_name = f"frame_{self.frame_count:06d}.jpg"
        img_path = os.path.join(images_dir, img_name)
        cv2.imwrite(img_path, frame)
        
        # Thread-safe access to pressed_keys
        with data_lock:
            current_pressed = [k for k in tracked_keys if keyboard.is_pressed(k)]
            pressed_keys[:] = current_pressed  # Update global list
            
            # Enregistrement des timestamps
            current_time = time.time() - start_time
            if "z" in current_pressed:
                acceleration_data.append(current_time)
            if "s" in current_pressed:
                braking_data.append(current_time)
            if "shift" in current_pressed:
                drifting_data.append(current_time)
        
        # Écriture CSV
        row = [img_name] + [str(int(k in current_pressed)) for k in tracked_keys]
        self.labels_file.write(",".join(row) + "\n")
        self.labels_file.flush()
        
        self.frame_count += 1
    
    def cleanup(self):
        """Nettoie les ressources."""
        if self.labels_file:
            self.labels_file.close()
        return self.session_dir

# Fonction pour mettre à jour l'interface
def update_gui():
    """Met à jour l'interface utilisateur de manière optimisée."""
    while True:
        try:
            with data_lock:
                current_pressed = pressed_keys.copy()
            
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
            
            keys_text = ', '.join(current_pressed) if current_pressed else 'Aucune'
            keys_pressed_label.config(text=f"Touches pressées : {keys_text}")
            
            root.update_idletasks()
            time.sleep(GUI_UPDATE_INTERVAL)
        except Exception as e:
            logger.error(f"Erreur dans update_gui: {e}")
            time.sleep(1)

# Fonction pour démarrer la capture
def start_capture_gui():
    """Démarre la capture depuis l'interface."""
    global capturing, start_time
    if not capturing:
        with data_lock:
            capturing = True
            start_time = time.time()
            # Réinitialiser les données
            acceleration_data.clear()
            braking_data.clear()
            drifting_data.clear()
        logger.info("Capture démarrée")

# Fonction pour arrêter la capture
def stop_capture_gui():
    """Arrête la capture depuis l'interface."""
    global capturing
    if capturing:
        with data_lock:
            capturing = False
        logger.info("Capture arrêtée")

# Fonction principale de capture optimisée
def start_capture():
    """Fonction principale de capture optimisée."""
    global capturing
    collector = DataCollector()
    
    try:
        while True:
            if capturing:
                try:
                    # Utiliser le gestionnaire de fenêtre optimisé
                    game_window = GameWindowManager.find_and_activate_window()
                    
                    # Configuration de session
                    images_dir = collector.setup_session()
                    
                    # Boucle de capture principale
                    while capturing:
                        collector.capture_frame_and_input(game_window, images_dir)
                        time.sleep(CAPTURE_INTERVAL)
                    
                    # Générer le graphique à la fin de la session
                    session_dir = collector.cleanup()
                    if session_dir:
                        show_acceleration_graph(session_dir)
                
                except Exception as e:
                    logger.error(f"Erreur pendant la capture: {e}")
                    with data_lock:
                        capturing = False
            
            time.sleep(0.5)  # Éviter la surcharge CPU
    
    except KeyboardInterrupt:
        logger.info("Interruption clavier détectée.")
    finally:
        collector.cleanup()

# Fonction pour afficher le graphique optimisée
def show_acceleration_graph(session_dir=None):
    """Affiche et sauvegarde le graphique des actions avec de meilleures performances."""
    with data_lock:
        accel_data = list(acceleration_data)
        brake_data = list(braking_data)
        drift_data = list(drifting_data)
    
    if not (accel_data or brake_data or drift_data):
        logger.info("Aucune donnée enregistrée pour le graphique.")
        return

    plt.figure(figsize=(12, 6))
    
    # Configuration optimisée du graphique
    if accel_data:
        plt.scatter(accel_data, [1] * len(accel_data), 
                   color="blue", label="Accélération (Z)", alpha=0.7, s=30)
    
    if brake_data:
        plt.scatter(brake_data, [2] * len(brake_data), 
                   color="red", label="Freinage (S)", alpha=0.7, s=30)
    
    if drift_data:
        plt.scatter(drift_data, [3] * len(drift_data), 
                   color="green", label="Dérapage (Shift)", alpha=0.7, s=30)

    # Configuration du graphique
    plt.xlabel("Temps écoulé (secondes)", fontsize=12)
    plt.ylabel("Actions", fontsize=12)
    plt.title("Graphique des actions du joueur", fontsize=14, fontweight='bold')
    plt.yticks([1, 2, 3], ['Accélération', 'Freinage', 'Dérapage'])
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Sauvegarder le graphique si un répertoire de session est fourni
    if session_dir:
        try:
            graph_path = os.path.join(session_dir, "actions_graph.png")
            plt.savefig(graph_path, dpi=150, bbox_inches='tight')
            logger.info(f"Graphique sauvegardé : {graph_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du graphique : {e}")

    # Afficher le graphique
    try:
        plt.show()
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage du graphique : {e}")

# Fonction pour créer l'interface utilisateur
def create_gui():
    """Crée l'interface utilisateur avec un design amélioré et positionnement personnalisé."""
    global root, status_label, time_elapsed_label, keys_pressed_label
    global start_button, stop_button
    
    root = tk.Tk()
    root.title("SuperTuxKart - Capture d'Écran et Analyse")
    
    # Configuration de la taille et position
    root.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}+{GUI_POSITION_X}+{GUI_POSITION_Y}")
    root.resizable(False, False)
    root.configure(bg="#2c3e50")
    
    # Centrer la fenêtre si les positions ne sont pas spécifiées
    if GUI_POSITION_X == 0 and GUI_POSITION_Y == 0:
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - GUI_WIDTH) // 2
        y = (screen_height - GUI_HEIGHT) // 2
        root.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}+{x}+{y}")
    
    # Garder la fenêtre au-dessus des autres (optionnel)
    # root.attributes('-topmost', True)
    
    logger.info(f"Interface créée : {GUI_WIDTH}x{GUI_HEIGHT} à la position ({GUI_POSITION_X}, {GUI_POSITION_Y})")

    # Styles améliorés
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 12))

    # Titre avec style amélioré
    title_label = tk.Label(
        root, 
        text="SuperTuxKart - Capture & Analyse", 
        font=("Arial", 22, "bold"), 
        bg="#2c3e50", 
        fg="#ecf0f1"
    )
    title_label.pack(pady=20)

    # Frame de statut avec bordure
    status_frame = tk.Frame(root, bg="#34495e", relief="ridge", bd=2)
    status_frame.pack(pady=15, padx=20, fill="x")

    status_label = tk.Label(
        status_frame, 
        text="En attente", 
        font=("Arial", 16, "bold"), 
        bg="#34495e", 
        fg="red"
    )
    status_label.pack(pady=10)

    time_elapsed_label = tk.Label(
        status_frame, 
        text="Temps écoulé : 0 secondes", 
        font=("Arial", 14), 
        bg="#34495e", 
        fg="#ecf0f1"
    )
    time_elapsed_label.pack(pady=5)

    # Touches pressées avec style amélioré
    keys_pressed_label = tk.Label(
        root, 
        text="Touches pressées : Aucune", 
        font=("Arial", 14), 
        bg="#2c3e50", 
        fg="#f39c12",
        wraplength=600
    )
    keys_pressed_label.pack(pady=15)

    # Boutons avec disposition améliorée
    button_frame = tk.Frame(root, bg="#2c3e50")
    button_frame.pack(pady=20)

    start_button = ttk.Button(
        button_frame, 
        text="🔴 Démarrer la capture", 
        command=start_capture_gui,
        width=20
    )
    start_button.grid(row=0, column=0, padx=10, pady=5)

    stop_button = ttk.Button(
        button_frame, 
        text="⏹️ Arrêter la capture", 
        command=stop_capture_gui, 
        state="disabled",
        width=20
    )
    stop_button.grid(row=0, column=1, padx=10, pady=5)

    graph_button = ttk.Button(
        button_frame, 
        text="📊 Afficher le graphique", 
        command=lambda: show_acceleration_graph(),
        width=20
    )
    graph_button.grid(row=1, column=0, padx=10, pady=10)

    # Nouveau bouton pour afficher les informations de la fenêtre
    window_info_button = ttk.Button(
        button_frame, 
        text="🖥️ Info fenêtre jeu", 
        command=show_window_info,
        width=20
    )
    window_info_button.grid(row=1, column=1, padx=10, pady=10)

    # Bouton pour repositionner manuellement la fenêtre
    reposition_button = ttk.Button(
        button_frame, 
        text="🎮 Repositionner jeu", 
        command=reposition_game_window,
        width=20
    )
    reposition_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    return root

def reposition_game_window():
    """Repositionne manuellement la fenêtre du jeu."""
    success = GameWindowManager.auto_position_at_startup()
    
    # Créer une popup de confirmation
    popup = tk.Toplevel(root)
    popup.title("Repositionnement")
    popup.geometry("350x150")
    popup.resizable(False, False)
    
    # Centrer la popup
    popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (350 // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (150 // 2)
    popup.geometry(f"350x150+{x}+{y}")
    
    if success:
        popup.configure(bg="#27ae60")
        message = "✅ Fenêtre repositionnée avec succès !\n\nPosition : ({}, {})\nTaille : {}x{}".format(
            WINDOW_FIXED_LEFT, WINDOW_FIXED_TOP, WINDOW_WIDTH, WINDOW_HEIGHT
        )
        color = "#27ae60"
    else:
        popup.configure(bg="#e74c3c")
        message = "❌ Impossible de repositionner !\n\nVeuillez lancer SuperTuxKart d'abord."
        color = "#e74c3c"
    
    message_label = tk.Label(
        popup, 
        text=message, 
        font=("Arial", 11, "bold"), 
        bg=color, 
        fg="white",
        justify="center"
    )
    message_label.pack(expand=True, padx=20, pady=20)
    
    close_button = ttk.Button(
        popup, 
        text="Fermer", 
        command=popup.destroy
    )
    close_button.pack(pady=10)
    
    # Fermer automatiquement après 3 secondes
    popup.after(3000, popup.destroy)

def show_window_info():
    """Affiche les informations sur la fenêtre de jeu dans une popup."""
    window_info = GameWindowManager.get_window_info()
    
    if window_info:
        info_text = f"""
Informations de la fenêtre SuperTuxKart :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Position : ({window_info['left']}, {window_info['top']})
📏 Taille : {window_info['width']} x {window_info['height']} pixels
👁️ Visible : {'Oui' if window_info['visible'] else 'Non'}
🔽 Minimisée : {'Oui' if window_info['minimized'] else 'Non'}
🔼 Maximisée : {'Oui' if window_info['maximized'] else 'Non'}
🎯 Active : {'Oui' if window_info['active'] else 'Non'}

Configuration actuelle :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 Position cible : ({WINDOW_FIXED_LEFT}, {WINDOW_FIXED_TOP})
📐 Taille cible : {WINDOW_WIDTH} x {WINDOW_HEIGHT} pixels
        """
        
        # Créer une fenêtre popup
        popup = tk.Toplevel(root)
        popup.title("Informations de la fenêtre")
        popup.geometry("400x350")
        popup.configure(bg="#2c3e50")
        popup.resizable(False, False)
        
        # Centrer la popup
        popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (400 // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (350 // 2)
        popup.geometry(f"400x350+{x}+{y}")
        
        # Texte d'information
        info_label = tk.Label(
            popup, 
            text=info_text, 
            font=("Consolas", 10), 
            bg="#2c3e50", 
            fg="#ecf0f1",
            justify="left",
            anchor="nw"
        )
        info_label.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Bouton pour fermer
        close_button = ttk.Button(
            popup, 
            text="Fermer", 
            command=popup.destroy
        )
        close_button.pack(pady=10)
        
    else:
        # Message d'erreur si la fenêtre n'est pas trouvée
        error_popup = tk.Toplevel(root)
        error_popup.title("Erreur")
        error_popup.geometry("300x150")
        error_popup.configure(bg="#e74c3c")
        error_popup.resizable(False, False)
        
        # Centrer la popup d'erreur
        error_popup.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (300 // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (150 // 2)
        error_popup.geometry(f"300x150+{x}+{y}")
        
        error_label = tk.Label(
            error_popup, 
            text="❌ Fenêtre SuperTuxKart\nnon trouvée !\n\nVeuillez lancer le jeu d'abord.", 
            font=("Arial", 12, "bold"), 
            bg="#e74c3c", 
            fg="white",
            justify="center"
        )
        error_label.pack(expand=True)
        
        close_button = ttk.Button(
            error_popup, 
            text="Fermer", 
            command=error_popup.destroy
        )
        close_button.pack(pady=10)

# Fonction pour créer le tableau des instructions
def create_instructions_table(parent):
    """Crée le tableau des instructions avec un design amélioré."""
    instructions_frame = tk.Frame(parent, bg="#34495e", relief="ridge", bd=2)
    instructions_frame.pack(pady=20, padx=20, fill="both", expand=True)

    instructions_title = tk.Label(
        instructions_frame, 
        text="🎮 Touches disponibles :", 
        font=("Arial", 16, "bold"), 
        bg="#34495e", 
        fg="#ecf0f1"
    )
    instructions_title.pack(anchor="w", padx=10, pady=10)

    # Tableau avec scroll si nécessaire
    table_frame = tk.Frame(instructions_frame, bg="#34495e")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Action", "Touche assignée")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
    
    # Configuration des colonnes
    table.heading("Action", text="Action")
    table.heading("Touche assignée", text="Touche assignée")
    table.column("Action", width=300, anchor="w")
    table.column("Touche assignée", width=150, anchor="center")

    # Données du tableau
    actions_data = [
        ("🔄 Tourner à gauche", "Q"),
        ("🔄 Tourner à droite", "D"),
        ("⚡ Accélérer", "Z"),
        ("🛑 Frein / Reculer", "S"),
        ("🎯 Tirer", "C"),
        ("💨 Nitro", "Espace"),
        ("🏎️ Dérapage", "Shift gauche"),
        ("👁️ Regarder en arrière", "V"),
    ]

    for action, key in actions_data:
        table.insert("", "end", values=(action, key))

    # Scrollbar pour le tableau
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def main():
    """Fonction principale optimisée avec positionnement automatique au démarrage."""
    try:
        logger.info("🚀 Démarrage de l'application SuperTuxKart Capture...")
        
        # Tentative de positionnement automatique de la fenêtre du jeu au démarrage
        if AUTO_POSITION_ON_STARTUP:
            logger.info("🎮 Recherche de la fenêtre SuperTuxKart...")
            time.sleep(STARTUP_DELAY)  # Petit délai pour s'assurer que tout est chargé
            GameWindowManager.auto_position_at_startup()
        
        # Créer l'interface utilisateur
        root = create_gui()
        
        # Créer le tableau des instructions
        create_instructions_table(root)
        
        # Démarrer les threads
        gui_thread = Thread(target=update_gui, daemon=True)
        capture_thread = Thread(target=start_capture, daemon=True)
        
        gui_thread.start()
        capture_thread.start()
        
        logger.info("✅ Application démarrée avec succès")
        
        # Démarrer la boucle principale
        root.mainloop()
        
    except Exception as e:
        logger.error(f"❌ Erreur dans la fonction principale : {e}")
    finally:
        logger.info("👋 Application fermée")

if __name__ == "__main__":
    main()