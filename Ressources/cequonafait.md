-Vico push ses ressource (Prioritaire !!!!!!!) **OK**
-Simon arrive au CESI (Facultatif...) +1 (9h06) **OK**
-Vico fume sa clope (malheuresement obligatoire) (trop souvent) **OK**
-Revoir le document scientifique avec l'aide du ChatGPT premium de Matteo
-Simon nous rebrief sur ce que fais le code avant pour nous permettre d'ecrire le rapport autour de ça
-Vico allume le pc **OK**
-Vico connecte ses neurones (y'en a plus que 2) **NTM MATTEO**


OBJECTIF : IMITATION LEARNING 
Mots clés: IA, DAGGER
Généralisation:

Problèmatique
Piste de solutions


Plan:
- intro sur ah les ia etc ca va vite la famille restez branchés, puis y'a   plusieurs manière des les incorporer dans les jeux vidéos notamment afin de reproduire le plus fidelement possibles des comportements humains.
- Etudes : 
    DRIVATAR vidéo + ressource 
    DAGGER
    Racing Game AI – Artificial Intelligence for Games (différentes ia dans jeux de courses)
    Data Quality in Imitation Learning (les données d'entrées tout ça là, notion de divergence d'action et de diversité des transitions)
    
    Tout sujet pertinent d'être gardé par rapport à notre experimentation sur super tux kart.
- Experimentation :
    Description de SuperTuxKart
    Comment on a alimenté l'IA
    comment on a fait conduire l'IA (bancale pour l'instant)
- Resultat
- Anneexes
- Glossaire
- Conclusio




<!-- 
Notre travail qu'est ce qu'on a fait ??
- D'abord on a voulu entrainer notre modele en apprentissage par imitation (imitation learning) sur supertuxkart (un jeu de course)
Pour ce faire nous avons enregistré plusieurs fois par seconde nos inputs (touches pressées) et screenshot,
ensuite avec pytorch on créer le modele
ensuite on peut émuler le modele. mais on a arreté cette méthode par ce que c'est trop long d'avoir un dataset asser consequent
pour avior une IA correcte (le temps de jeux necessaire ne pouvant etre determiné cela aurait pu nous prendre des
semaine sans garantis de resultat) -->


INSERE LE BRIEFING ICI SIMON


## Apprentissage par imitation sur SuperTuxKart

Dans un premier temps, nous avons choisi d’entraîner un modèle en **apprentissage par imitation** (*imitation learning*) sur le jeu **SuperTuxKart**. L’objectif était de permettre à une IA de reproduire le comportement d’un joueur humain, en se basant uniquement sur des captures d’écran du jeu et les actions correspondantes.

---

### 1. Acquisition des données

Nous avons conçu un script Python utilisant `pygame`, `pyautogui` et `cv2` pour enregistrer :

- des **captures d’écran** régulières (environ 10 par seconde),
- les **données de la manette** PS4 : axes analogiques, boutons, D-pad.

Chaque session de jeu générait :

- un dossier `images/` contenant les captures d’écran au format `.jpg`,
- un fichier `labels.csv` listant pour chaque image les valeurs normalisées des axes et l’état des boutons.

---

### 2. Entraînement du modèle

À partir du dataset, nous avons développé un modèle de type **CNN** avec PyTorch :

- **Entrée** : une image (224×224 pixels),
- **Sortie** : 
  - 2 valeurs continues pour les axes du joystick (gauche/droite, haut/bas),
  - plusieurs sorties binaires pour les boutons (ex : croix, carré).

Nous avons **entraîné 20 versions du modèle**, en variant certains hyperparamètres (learning rate, nombre d’epochs, taille du dataset), et sauvegardé les résultats dans des fichiers `model.pth`.

---

### 3. Inférence et contrôle du jeu

Une fois le modèle entraîné, nous avons conçu un second script pour l’utiliser en temps réel :

1. Le script capture en direct l’image du jeu.
2. Il l’envoie au modèle (`model.pth`) pour prédire l’action à effectuer.
3. Il utilise soit :
   - `vgamepad` pour simuler une manette Xbox,
   - `pyvigem` pour simuler une manette PS4 (DualShock 4),
   en injectant les prédictions (axes et boutons).

---

### 4. Limites rencontrées

Nous avons suspendu cette méthode en raison de plusieurs difficultés :

- Besoin d’une **grande quantité de données** pour que le comportement soit cohérent.
- Faible **généralisation** : l’IA ne sortait pas des trajectoires apprises.
- Forte dépendance à la **qualité et régularité** des données humaines.

---

Ce travail a posé les bases d’un apprentissage par imitation simple et reproductible, en environnement contrôlé, mais demande des optimisations pour des résultats fiables en jeu réel.


@simon ICI
