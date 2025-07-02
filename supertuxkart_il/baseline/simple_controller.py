import numpy as np

class SimpleExpertController:
    """
    Contrôleur expert heuristique basé sur l'aim point.
    Utilise un modèle CNN pour prédire un point d'attaque (optionnel, ici on peut mettre une heuristique simple ou un stub).
    """
    def __init__(self, disable_drift=False):
        self.disable_drift = disable_drift

    def act(self, state, noise=None):
        # Ici, on suppose que state est un dict avec 'image', 'velocity', 'rotation'
        # Pour simplifier, on utilise une heuristique basique sur la vélocité et la rotation
        velocity = np.linalg.norm(state['velocity'])
        # Heuristique : si la rotation yaw est grande, on tourne plus
        steer = float(state['rotation'][1])  # Yaw simplifié
        acc = 1.0 if velocity < 30 else 0.5
        brake = 1.0 if velocity > 35 else 0.0
        drift = 1.0 if abs(steer) > 0.2 and not self.disable_drift else 0.0
        # Ajout de bruit optionnel
        if noise is not None:
            steer += np.random.randn() * noise
        return np.array([steer, acc, brake, drift], dtype=np.float32) 