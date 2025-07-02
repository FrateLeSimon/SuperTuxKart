"""
Script d'installation universel pour SuperTuxKart IL.
- Crée un venv Python 3.11
- Installe les dépendances (hors pystk)
- Installe pystk automatiquement sous Windows 3.11
- Crée les dossiers nécessaires
- Guide l'utilisateur étape par étape
"""
import os
import sys
import subprocess
import urllib.request
import json

VENV_DIR = "venv"
PYTHON_REQUIRED = (3, 11)
PYTHON_MAX = (3, 12)  # exclu 3.12+

def is_venv():
    """Retourne True si le script est exécuté dans un venv."""
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def check_python_version():
    """Vérifie que la version de Python est 3.11."""
    v = sys.version_info
    if not (v.major, v.minor) == PYTHON_REQUIRED:
        print(f"Ce projet nécessite Python 3.11 (trouvé: {v.major}.{v.minor})")
        print("Télécharge Python 3.11 ici : https://www.python.org/downloads/release/python-3110/")
        sys.exit(1)

def create_venv():
    """Crée un environnement virtuel s'il n'existe pas déjà."""
    if not os.path.exists(VENV_DIR):
        print("Création de l'environnement virtuel (venv)...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("venv créé.")
    else:
        print("venv déjà présent.")

def pip_path():
    """Retourne le chemin vers l'exécutable pip du venv."""
    return os.path.join(VENV_DIR, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "pip")

def install_requirements():
    """Installe les dépendances du projet (hors pystk) dans le venv."""
    pip = pip_path()
    print("Installation des dépendances dans le venv (sauf pystk)...")
    # On retire pystk du requirements.txt si présent
    with open("requirements.txt", "r") as f:
        lines = [l for l in f if "pystk" not in l]
    with open("requirements_tmp.txt", "w") as f:
        f.writelines(lines)
    subprocess.check_call([pip, "install", "-r", "requirements_tmp.txt"])
    os.remove("requirements_tmp.txt")
    print("Dépendances installées (hors pystk).")

def get_latest_pystk_wheel_url():
    """Tente de récupérer l'URL de la wheel pystk pour Python 3.9 Windows via l'API GitHub."""
    api_url = "https://api.github.com/repos/philkr/pystk/releases/latest"
    try:
        with urllib.request.urlopen(api_url) as resp:
            data = json.load(resp)
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith("cp39-cp39-win_amd64.whl"):
                return asset.get("browser_download_url")
    except Exception as e:
        print(f"[DEBUG] Erreur lors de l'accès à l'API GitHub : {e}")
    return None

def install_pystk():
    """Installe pystk automatiquement sous Windows 3.11, sinon affiche la marche à suivre."""
    pip = pip_path()
    try:
        import pystk
        print("pystk déjà installé.")
        return
    except ImportError:
        pass

    print("Installation de pystk...")

    # Cas Windows + Python 3.11
    if os.name == "nt" and sys.version_info.major == 3 and sys.version_info.minor == 11:
        wheel_file = "PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl"
        wheel_path = os.path.join(os.path.dirname(__file__), wheel_file)
        if os.path.exists(wheel_path):
            try:
                print(f"Installation de la wheel dans le venv : {wheel_file}")
                subprocess.check_call([pip, "install", wheel_file])
                print("PySuperTuxKart installé dans le venv.")
                return
            except Exception as e:
                print(f"Échec de l'installation dans le venv : {e}")
                print("Tentative d'installation globale avec py -3.11 -m pip ...")
                try:
                    subprocess.check_call(["py", "-3.11", "-m", "pip", "install", wheel_file])
                    print("PySuperTuxKart installé globalement.")
                    return
                except Exception as e2:
                    print(f"Échec de l'installation globale : {e2}")
        print("\nLa wheel officielle pour pystk/PySuperTuxKart doit être installée manuellement.")
        print("Télécharge ce fichier :")
        print("  https://github.com/philkr/pystk/releases/download/v1.1.3/PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl")
        print("Place-le dans le dossier setup/ puis exécute :")
        print("  .\\venv\\Scripts\\activate")
        print("  pip install PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl")
        print("(Assure-toi que le venv est activé)")
        sys.exit(1)
    else:
        # Linux/Mac ou autre version de Python
        print("Merci d'installer pystk manuellement selon ta plateforme :")
        print("https://github.com/philkr/pystk/releases")
        print("ou https://github.com/supertuxkart/stk-code/tree/master/tools/pystk")
        sys.exit(1)

def create_data_dirs():
    """Crée le dossier de données pour les trajectoires si besoin."""
    os.makedirs("data/trajectories", exist_ok=True)
    print("Dossier data/trajectories prêt.")

def main():
    """Routine principale du setup : vérifie la version, crée le venv, installe les dépendances, pystk, etc."""
    print("=== Setup automatique SuperTuxKart IL ===")
    check_python_version()
    if not is_venv():
        create_venv()
        print("\nActive l'environnement virtuel avant de continuer :")
        if os.name == "nt":
            print("  venv\\Scripts\\activate")
        else:
            print("  source venv/bin/activate")
        print("Puis relance : python setup_project.py")
        sys.exit(0)
    install_requirements()
    install_pystk()
    create_data_dirs()
    print("\nSetup terminé ! Tu peux maintenant :")
    print("  - Collecter des données : python data/collector.py ...")
    print("  - Entraîner ton agent   : python training/train.py ...")
    print("  - Évaluer ton agent     : python evaluation/eval.py ...")

if __name__ == "__main__":
    main() 