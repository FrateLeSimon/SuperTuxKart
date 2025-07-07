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
- **Collecte de données (par un humain)** :
  ```bash
  python data/human_collector.py --save_dir data/human_trajectories --episodes 1 --max_steps 1000 --track lighthouse
  ```
  > Contrôle au clavier : flèches (direction/accélération/frein), shift (drift). Les données sont enregistrées automatiquement à chaque frame.

- **Entraînement de l'agent** :
  ```bash
  python training/train.py --data_dir data/trajectories --epochs 10 --batch_size 32 --lr 1e-3
  # ou pour entraîner sur tes propres parties :
  python training/train.py --data_dir data/human_trajectories --epochs 10 --batch_size 32 --lr 1e-3
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

## Collecte de trajectoires humaines (tuto)

Tu veux que l'IA t'imite ? Voici comment enregistrer tes propres parties :

1. **Active le venv**
   - Windows :
     ```
     venv\Scripts\activate
     ```
   - Linux/Mac :
     ```
     source venv/bin/activate
     ```
2. **Place-toi dans le dossier du code source**
   ```bash
   cd supertuxkart_il
   ```
3. **Lance la collecte**
   ```bash
   python data/human_collector.py --save_dir data/human_trajectories --episodes 1 --max_steps 1000 --track lighthouse
   ```
   - Contrôle au clavier : ZQSD (direction/accélération/frein), espace (drift)
   - Les données sont enregistrées automatiquement à chaque frame dans `data/human_trajectories/`
   - Tu peux relancer pour enregistrer plusieurs parties (elles seront numérotées)

4. **Entraîne l'IA sur tes propres données**
   ```bash
   python training/train.py --data_dir data/human_trajectories --epochs 10 --batch_size 32 --lr 1e-3
   ```

5. **Évalue l'agent comme d'habitude**
   ```bash
   python evaluation/eval.py --model_path imitation_agent.pth --episodes 5 --max_steps 1000 --track lighthouse
   ```

**Astuce :** Tu peux mélanger des données humaines et automatiques dans le même dossier pour entraîner un agent hybride.

---

### Comment fonctionne la collecte humaine (pour les développeurs)

Le script `human_collector.py` permet d'enregistrer des trajectoires de jeu contrôlées par un humain, pour entraîner l'IA à imiter un joueur réel.

- **Initialisation** : le script utilise l'environnement `SimplePyTux` (wrapper Gym autour de SuperTuxKart via pystk).
- **Capture des entrées** : la librairie `pynput` écoute les touches du clavier en temps réel. Le mapping est :
  - Z = accélérer
  - S = freiner
  - Q = gauche
  - D = droite
  - Espace = drift
- **À chaque frame** :
  - Le script lit les touches pressées et les convertit en action `[steer, acc, brake, drift]`.
  - Il applique cette action dans l'environnement et récupère l'état du jeu (image, vitesse, rotation).
  - Il sauvegarde l'état et l'action dans un fichier `.pt` dans un dossier dédié à l'épisode.
- **Format des données** :
  ```python
  {
      'state': {
          'image': ...,
          'velocity': ...,
          'rotation': ...
      },
      'action': np.array([steer, acc, brake, drift], dtype=np.float32)
  }
  ```
- **Compatibilité** : ce format est identique à celui de la collecte automatique (expert), donc l'IA peut s'entraîner sur des données humaines, automatiques, ou mixtes sans rien changer au pipeline.
- **Extensible** : le mapping clavier peut être modifié facilement, et on peut ajouter la prise en charge d'autres périphériques si besoin.

Ce script rend l'imitation learning humain simple, robuste et totalement intégré au projet.

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