# Code source - SuperTuxKart IL

Ce dossier contient tout le code Python du pipeline d'imitation learning pour SuperTuxKart.

## Structure du code
- `agents/` : agents d'imitation (CNN+MLP)
- `baseline/` : contrôleur expert heuristique
- `data/` : collecte de trajectoires
- `environments/` : wrapper Gym pour SuperTuxKart
- `evaluation/` : scripts d'évaluation
- `training/` : scripts d'entraînement
- `utils/` : utilitaires (dataset, etc.)

## Utilisation du pipeline

Après installation via `/setup/` :

- Collecte de données :
  ```bash
  python data/collector.py --save_dir data/trajectories --episodes 50 --max_steps 1000 --noise_std 0.05 --track lighthouse
  ```
- Entraînement :
  ```bash
  python training/train.py --data_dir data/trajectories --epochs 10 --batch_size 32 --lr 1e-3
  ```
- Évaluation :
  ```bash
  python evaluation/eval.py --model_path imitation_agent.pth --episodes 5 --max_steps 1000 --track lighthouse
  ```

## Remarques
- L'installation et la gestion du venv se font dans `/setup/`.
- Pour toute ressource, doc, ou asset, voir `/ressources/`.

---

Pour l'installation, voir `/setup/README.md`. 