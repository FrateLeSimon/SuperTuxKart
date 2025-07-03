# SuperTuxKart IL - Organisation du projet

![Tested](https://img.shields.io/badge/pipeline-tested-brightgreen?style=flat-square)

Bienvenue ! Ce dépôt est organisé pour séparer clairement :
- **Le code source** (`/supertuxkart_il/`)
- **Les scripts d'installation et d'environnement** (`/setup/`)
- **Les ressources, assets, wheels, docs, etc.** (`/ressources/`)

---

## Dépendances principales

- Python 3.11 (**obligatoire**)
- torch
- numpy
- gym
- matplotlib
- pystk (voir instructions spécifiques ci-dessous)

La liste complète des dépendances et leurs versions exactes se trouve dans [setup/requirements.txt](setup/requirements.txt).

**Remarque importante :**  
L'installation de `pystk` nécessite une procédure particulière sous Windows/Python 3.11. Reporte-toi à la section "Installation de pystk" ci-dessous ou au [README du dossier setup](setup/README.md) pour plus de détails.

---

## Installation du projet

**1. Place-toi dans le dossier `setup/`**
```bash
cd setup
```

**2. Installation recommandée**
- **Windows** : double-clique sur `install_all.bat` ou lance :
  ```
  .\install_all.bat
  ```
- **Linux/Mac** :
  ```bash
  bash install_all.sh
  ```
> Ces scripts créent le venv dans `setup/venv/`, installent toutes les dépendances, activent le venv et relancent le setup automatiquement.

**3. Installation manuelle (avancée)**
- Tu peux lancer `setup_project.py` à la main si tu veux contrôler chaque étape.

---

## Activation de l'environnement virtuel
- **Windows** :
  ```
  venv\Scripts\activate
  ```
  ou double-clique sur `activate_venv.bat`
- **Linux/Mac** :
  ```
  source venv/bin/activate
  ```

---

## Installation de pystk (Windows 3.11)

Avant de lancer l'installation automatique, il est nécessaire de télécharger la wheel officielle de PySuperTuxKart (pystk) :

1. Télécharge la wheel ici :
   https://github.com/philkr/pystk/releases/download/v1.1.3/PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl
2. Place le fichier téléchargé dans le dossier `setup/` de ce projet.
3. Lance le script d'installation automatique (`install_all.bat` ou `python setup_project.py`).
   - Le script tentera d'installer la wheel automatiquement dans le bon environnement virtuel.

**Si l'installation automatique échoue, fais-le manuellement :**

1. Active le venv :
   ```powershell
   .\venv\Scripts\activate
   ```
2. Installe la wheel :
   ```powershell
   pip install PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl
   ```

Après cette étape, relance le script d'installation ou continue l'utilisation du projet normalement.

---

## Utilisation du pipeline

Après installation via `/setup/` :

- **Collecte de données (par l'expert automatique)** :
  ```bash
  python data/collector.py --save_dir data/trajectories --episodes 50 --max_steps 1000 --noise_std 0.05 --track lighthouse
  ```
- **Entraînement de l'agent** :
  ```bash
  python training/train.py --data_dir data/trajectories --epochs 10 --batch_size 32 --lr 1e-3
  ```
- **Évaluation de l'agent** :
  ```bash
  python evaluation/eval.py --model_path imitation_agent.pth --episodes 5 --max_steps 1000 --track lighthouse
  ```

> Place-toi dans le dossier `/supertuxkart_il/` pour utiliser ces scripts.

Pour tester automatiquement tout le pipeline (installation, collecte, entraînement, évaluation) :

Active d'abord le venv :
- **Windows** :
  ```
  venv\Scripts\activate
  ```
- **Linux/Mac** :
  ```
  source venv/bin/activate
  ```

Puis lance le test :
```bash
cd setup
python test_pipeline.py
```

---

## Structure du code source

- `agents/` : agents d'imitation (CNN+MLP)
- `baseline/` : contrôleur expert heuristique
- `data/` : collecte de trajectoires
- `environments/` : wrapper Gym pour SuperTuxKart
- `evaluation/` : scripts d'évaluation
- `training/` : scripts d'entraînement
- `utils/` : utilitaires (dataset, etc.)

---

## Compatibilité et remarques
- Python 3.11 obligatoire (pas 3.12+)
- SuperTuxKart doit être installé sur ta machine
- L'installation et la gestion du venv se font dans `/setup/`.
- Pour toute ressource, doc, ou asset, voir `/ressources/`.

---

## Structure du dépôt

```
/setup/           → install_all.bat, install_all.sh, setup_project.py, requirements.txt, activate_venv.bat, test_pipeline.py, etc.
/supertuxkart_il/ → code source du projet (agents, data, training, etc.)
/ressources/      → assets, wheels, documentation, notes, etc.
```

Pour toute question, consulte ce README ou les dossiers `/setup/` et `/supertuxkart_il/` pour plus de détails. 