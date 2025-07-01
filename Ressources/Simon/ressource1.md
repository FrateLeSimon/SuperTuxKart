# Imitation Learning for Agnostic Battery Charging: A DAGGER-Based Approach
## Apprentissage par imitation pour la charge de batteries agnostique : une approche basée sur DAgger

Cet article propose une application originale de l’algorithme DAgger (Dataset Aggregation) au domaine de la charge de batteries, dans un contexte agnostique, c’est-à-dire sans connaissance précise des paramètres système ni accès aux états internes de la batterie. L’objectif est d’apprendre une politique de contrôle sûre et efficace en imitant un expert de type MPC (Model Predictive Control), tout en restant compatible avec les contraintes du monde réel.

---

### Motivation

- Les contrôleurs MPC sont puissants mais supposent :
  - des paramètres connus,
  - une observabilité complète,
  - des ressources de calcul élevées.
- Ces hypothèses sont souvent irréalistes sur des batteries vieillissantes ou en systèmes embarqués.
- Le clonage comportemental (behavioral cloning) est simple mais souffre de problèmes de généralisation.

---

### Méthodologie

Les auteurs adaptent DAgger à un contexte de POMDP (Processus de décision markovien partiellement observable), en s’appuyant sur :

- une fenêtre d’historique des observations (tension, température, courant passé),
- un apprentissage itératif où :
  - on collecte à chaque itération les décisions de l’expert et de l’agent imitateur,
  - on met à jour le modèle avec un Réseau de Neurones Récurrent (LSTM).

Ce cadre ne nécessite pas d'accès aux états internes de la batterie, et reste robuste aux variations de paramètres (vieillissement, conditions extrêmes…).

---

### Protocole expérimental

- Utilisation d’un simulateur électrochimique réaliste basé sur le modèle *Single Particle Model* couplé à une dynamique thermique.
- L’expert est un contrôleur MPC avec connaissance complète du système.
- L’agent est entraîné sur 15 itérations DAgger, en couvrant un large éventail de conditions batterie.

---

### Résultats

Comparaison avec un agent appris par clonage comportemental :

| Critère                         | DAgger                    | Clonage comportemental       |
|---------------------------------|----------------------------|-------------------------------|
| Précision des actions           | meilleure                  | plus d’erreurs                |
| Respect des contraintes thermiques | 0,08 K en moyenne         | 0,4 K en moyenne              |
| Robustesse aux variations       | élevée                     | moins stable                  |
| Suivi de tension et de charge   | équivalent                 | équivalent                    |

DAgger maintient mieux la sécurité tout en restant compétitif en performance globale.

---

### Contributions

- Première application de DAgger à un problème de contrôle de batterie en conditions réalistes.
- Proposition d’un cadre d’apprentissage par imitation dans un POMDP, sans supervision directe.
- Validation sur 100 simulations aléatoires, montrant la généralisation et la robustesse de la méthode.

---

### Conclusion et perspectives

L’approche DAgger adaptée au POMDP démontre la faisabilité d’un contrôle intelligent sans modèle explicite. Prochaine étape : prise en compte de l’incertitude, adaptation en temps réel, et tests sur batteries physiques réelles.
