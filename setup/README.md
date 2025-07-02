# Setup & Environnement - SuperTuxKart IL

Ce dossier contient tout ce qui concerne l'installation, la configuration de l'environnement, et l'automatisation du projet.

## Installation recommandée

**1. Place-toi dans ce dossier (`setup/`)**
```bash
cd setup
```

**2. Lance le script d'installation automatique**
- **Windows** : double-clique sur `install_all.bat` ou lance :
  ```
  .\install_all.bat
  ```
- **Linux/Mac** :
  ```bash
  bash install_all.sh
  ```

> Ces scripts créent le venv dans `setup/venv/`, installent toutes les dépendances, activent le venv et relancent le setup automatiquement.

## Installation manuelle (avancée)
- Tu peux lancer `setup_project.py` à la main si tu veux contrôler chaque étape.

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

## Utilisation du pipeline
- Place-toi dans le dossier `/supertuxkart_il/` et utilise les scripts de collecte, entraînement, évaluation (voir le README de ce dossier).

## Compatibilité
- Python 3.11 obligatoire (pas 3.12+)
- SuperTuxKart doit être installé sur ta machine

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

Pour le code source, voir `/supertuxkart_il/README.md`. 