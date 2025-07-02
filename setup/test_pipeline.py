"""
Script de test automatique du pipeline SuperTuxKart IL.
- Vérifie l'import de pystk
- Collecte un mini-dataset temporaire
- Entraîne l'agent sur ces données
- Évalue l'agent
- Nettoie tout à la fin
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import subprocess
import shutil

def run(cmd, cwd=None):
    """Exécute une commande shell et stoppe le script en cas d'erreur."""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Erreur lors de l'exécution : {cmd}")
        sys.exit(1)

def main():
    print("=== Test automatique du pipeline SuperTuxKart IL ===")

    # Vérification de l'import pystk
    try:
        import pystk
        print("✔ pystk importé avec succès.")
    except ImportError:
        print("❌ pystk n'est pas installé ou le venv n'est pas activé.")
        sys.exit(1)

    # Création d'un dossier temporaire pour le test
    test_data_dir = os.path.abspath("test_data")
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    os.makedirs(test_data_dir, exist_ok=True)

    # 1. Collecte de données (1 épisode, 5 steps)
    run("python -m supertuxkart_il.data.collector --save_dir test_data/trajectories --episodes 1 --max_steps 5 --noise_std 0.01 --track lighthouse", cwd="..")

    # 2. Entraînement (1 epoch, batch size 1)
    run("python -m supertuxkart_il.training.train --data_dir test_data/trajectories --epochs 1 --batch_size 1 --lr 1e-3", cwd="..")

    # 3. Évaluation (1 épisode, 5 steps)
    run("python -m supertuxkart_il.evaluation.eval --model_path imitation_agent.pth --episodes 1 --max_steps 5 --track lighthouse", cwd="..")

    # Nettoyage du dossier temporaire et du modèle
    shutil.rmtree(test_data_dir)
    if os.path.exists("imitation_agent.pth"):
        os.remove("imitation_agent.pth")

    print("\n✅ Test pipeline réussi ! Tout fonctionne correctement.")

if __name__ == "__main__":
    main() 