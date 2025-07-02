# SuperTuxKart IL - Organisation du projet

![Tested](https://img.shields.io/badge/pipeline-tested-brightgreen?style=flat-square)

Bienvenue ! Ce dépôt est organisé pour séparer clairement :
- **Le code source** (`/supertuxkart_il/`)
- **Les scripts d'installation et d'environnement** (`/setup/`)
- **Les ressources, assets, wheels, docs, etc.** (`/ressources/`)

---

## Installation du projet

**1. Ouvre un terminal et place-toi dans le dossier du projet**

**2. Va dans le dossier `setup/`**
```bash
cd setup
```

**3. Télécharge la wheel officielle de PySuperTuxKart (pystk) pour Windows 3.11**
- [Lien direct](https://github.com/philkr/pystk/releases/download/v1.1.3/PySuperTuxKart-1.1.3-cp311-cp311-win_amd64.whl)
- Place le fichier téléchargé dans le dossier `setup/`.

**4. Lance le script d'installation automatique**
- **Windows** : double-clique sur `install_all.bat` ou lance :
  ```
  .\install_all.bat
  ```
- **Linux/Mac** :
  ```bash
  bash install_all.sh
  ```

> Ces scripts créent le venv dans `setup/venv/`, installent toutes les dépendances, activent le venv et relancent le setup automatiquement. Tu n'as rien d'autre à faire.

**5. (Optionnel) Installation manuelle avancée**
- Tu peux lancer `setup_project.py` à la main si tu veux contrôler chaque étape (voir `setup/README.md`).

**6. Activation du venv pour utiliser le pipeline**
- **Windows** :
  ```
  venv\Scripts\activate
  ```
- **Linux/Mac** :
  ```
  source venv/bin/activate
  ```

**7. Lancer les scripts du pipeline**
- Place-toi dans le dossier `/supertuxkart_il/` et utilise les scripts de collecte, entraînement, évaluation (voir le README de ce dossier).

---

## Si l'installation automatique de pystk échoue (Windows 3.11)

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

## Test automatique du pipeline

> Après avoir terminé l'installation, tu peux vérifier que tout fonctionne avec :

```bash
cd setup
python test_pipeline.py
```

Le script vérifie pystk, collecte un mini-dataset, entraîne et évalue l'agent, puis nettoie tout. Si tout passe, l'installation et le pipeline sont OK !

---

## Structure du dépôt

```
/setup/           → install_all.bat, install_all.sh, setup_project.py, requirements.txt, activate_venv.bat, test_pipeline.py, etc.
/supertuxkart_il/ → code source du projet (agents, data, training, etc.)
/ressources/      → assets, wheels, documentation, notes, etc.
```

---

Pour toute question, consulte le README détaillé dans `/setup/` ou `/supertuxkart_il/`. 