# Imitation Learning for Autonomous Agents in SuperTuxKart Ice Hockey
## Apprentissage par imitation pour agents autonomes dans SuperTuxKart (mode hockey)

Cette étude explore l’usage de l’**apprentissage par imitation** dans le jeu vidéo *SuperTuxKart*, plus précisément dans son mode de jeu **hockey**. L’objectif est de former un agent autonome capable de reproduire le comportement d’un agent expert, **sans faire appel à des démonstrations humaines**.

---

### Objectif

- Apprendre un comportement réaliste à partir d’un **agent IA performant** déjà intégré au jeu.
- Reproduire les décisions de l’agent expert à partir des états du jeu.

---

### Construction du dataset

- L’agent **expert sélectionné** est *jurgen* (un agent IA performant déjà intégré au jeu SuperTuxKart dans le mode hockey), choisi pour ses bonnes performances (buts marqués).
- À chaque étape :
  - extraction des **états du jeu** (positions, vitesses, angles),
  - association avec les **actions correspondantes** (accélération, direction, freinage).
- Les données sont transformées en **vecteurs de caractéristiques**.
- Entraînement d’un **réseau de neurones entièrement connecté** pour imiter les décisions de l’expert.

---

### Évaluation de DAgger

- DAgger (Dataset Aggregation) est également testé :
  - L’agent imitateur joue **en autonomie**,
  - L’expert est sollicité pour corriger ses actions → enrichissement du dataset.
- Dans ce contexte, **DAgger est moins performant** que l’apprentissage supervisé direct.
  - Raisons : **manque de diversité** des situations explorées, **faible généralisation**.

---

### Comparaison des politiques apprises

- Meilleures performances observées quand :
  - **Deux agents imitateurs indépendants** jouent ensemble.
  - Cela favorise la **diversité comportementale** et la complémentarité des décisions.
- À l’inverse, les agents DAgger :
  - obtiennent de **piètres résultats**,
  - suggérant des **limites en exploration** et en capacité d’adaptation.

---

### Conclusion

- L’apprentissage supervisé à partir d’un **expert artificiel** peut produire :
  - des comportements crédibles,
  - dans un **environnement de jeu dynamique et multi-agent**.
- L’étude met en lumière les **limites de DAgger** quand les corrections sont :
  - **peu variées**, 
  - ou **faiblement informatives**.

---

### En résumé

Cette expérimentation montre qu’un **apprentissage par imitation simple mais bien conçu**, même à partir d’un expert non humain, permet d’obtenir des agents autonomes **efficaces et crédibles**, à condition de maîtriser la **diversité des données** et la **qualité de l’exploration**.

