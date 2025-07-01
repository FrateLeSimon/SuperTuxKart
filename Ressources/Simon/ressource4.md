# Hierarchical Imitation Learning of Team Behavior from Heterogeneous Demonstrations
## DTIL : Apprentissage par imitation hiérarchique du comportement d'équipe à partir de démonstrations hétérogènes

Ce travail présente **DTIL (Deep Team Imitation Learner)**, un cadre d’apprentissage par imitation multi-agent **hiérarchique**, conçu pour apprendre le comportement d’équipe à partir de démonstrations **hétérogènes** et **partiellement observables**.

Contrairement aux approches classiques d’apprentissage par imitation multi-agent (MAIL), qui supposent un comportement homogène entre les agents et les données, DTIL modélise explicitement :

- la **diversité** des comportements d’équipe,
- leur **sous-optimalité potentielle**,
- et les limites de l’observation partielle.

---

### Structure hiérarchique

Chaque agent est modélisé par deux niveaux de politique :

1. **Politique haut niveau** :
   - sélectionne des **sous-tâches discrètes** (ex. : défendre, avancer, couvrir un coéquipier).
2. **Politique bas niveau** :
   - exécute des **actions concrètes** au sein de la sous-tâche (ex. : se déplacer, tirer, se positionner).

L’apprentissage suit une procédure **Expectation-Maximization (EM)** :
- **E-step** : infère les sous-tâches latentes à partir des démonstrations.
- **M-step** : entraîne les deux politiques via **IQLearn**, une méthode d'apprentissage non-adversariale et scalable basée sur la correspondance des distributions d’occupation.

---

### Cadre théorique

- L’approche repose sur une **extension formelle du matching des mesures d’occupation** aux environnements **partiellement observables** et **multi-agents**.
- Des garanties théoriques assurent :
  - la **convergence** du processus,
  - et une **correspondance univoque** entre politiques hiérarchiques et distributions d’occupation.
- Cela garantit la cohérence de l’apprentissage, même avec un **étiquetage partiel**.

---

### Évaluations expérimentales

DTIL est testé sur plusieurs environnements coopératifs :

- **Multi-Jobs** (MJ-2, MJ-3) : agents avec tâches parallèles,
- **Movers and Flood** : navigation et coordination basées sur règles discrètes,
- **SMACv2** (*StarCraft II micromanagement*) : environnements complexes de contrôle d’escouades.

---

### Résultats

- DTIL **dépasse** les méthodes de référence :
  - **Behavior Cloning**, **MA-GAIL**, **MA-OptionGAIL**, etc.
- L’approche est particulièrement efficace pour :
  - capturer des **stratégies multimodales**,
  - **généraliser à partir de démonstrations imparfaites et non étiquetées**.
- Même avec **seulement 20 % de sous-tâches annotées**, DTIL apprend une coordination d’équipe efficace.

---

### Conclusion

- DTIL propose une solution **robuste, interprétable et scalable** pour l’apprentissage du **comportement collectif**.
- Il surmonte les limites des approches MAIL traditionnelles :
  - en s’adaptant aux **données imparfaites**,
  - et en intégrant les dynamiques réelles d’une équipe.
- Ce travail ouvre la voie à :
  - la **modélisation d’équipe automatisée**,
  - la **formation assistée par IA**,
  - et l’application à des systèmes **multi-agents en conditions réelles**.

