# Imitation Learning at All Levels of Game AI
## Apprentissage par imitation à tous les niveaux de l’IA dans les jeux vidéo

Ce travail de **Thurau, Sagerer et Bauckhage** propose un cadre complet d’**apprentissage par imitation** pour des agents artificiels dans les jeux vidéo, en prenant **Quake II** comme étude de cas. L'approche repose sur l'idée que les comportements humains dans les jeux émergent de **processus cognitifs hiérarchisés**. Le modèle proposé imite les **comportements stratégiques, tactiques et réactifs** à partir de parties enregistrées de joueurs humains.

---

### Objectif

- Aller au-delà des IA classiques fondées sur des règles (ex. : A*, automates finis).
- Utiliser les **démos de jeu** comme source riche de données comportementales (positions, vitesses, visée, objets ramassés, adversaires…).
- Générer des comportements crédibles, cohérents et variés via apprentissage hiérarchique.

---

### Architecture comportementale hiérarchique

1. **Comportement stratégique** :
   - Objectifs à long terme (ex. : contrôle de zones, navigation).
   - Appris via **Neural Gas** + **champs de potentiel** + **traînées de phéromones**.

2. **Comportement tactique** :
   - Décisions contextuelles (ex. : embuscade, changement d’arme).
   - Modélisé avec une architecture **Mixture of Experts**.

3. **Comportement réactif** :
   - Réactions locales immédiates (ex. : viser, esquiver, tirer).
   - Acquis via des **cartes auto-organisatrices (SOM)** combinées à des **MLP spécialisés**.

---

### Modélisation des mouvements

- Pour reproduire les **mouvements réalistes des joueurs** :
  - Analyse en composantes principales (**PCA**) sur les trajectoires.
  - Extraction de **primitives de mouvement**.
  - Génération d’actions fluides et probabilistes, y compris des actions complexes (saut, rocket-jump…).

---

### Contributions clés

- Pipeline complet d’apprentissage à partir de démos **sans script manuel**.
- Architecture cognitive multi-niveaux pour générer des comportements crédibles.
- Intégration du **comportement** et de la **cinématique du mouvement**.
- Validation expérimentale dans un jeu FPS compétitif, avec des agents au comportement proche de celui de vrais joueurs.

---

### Conclusion

L’étude montre que l’apprentissage par imitation, lorsqu’il est couplé à un modèle cognitif hiérarchique, peut produire des agents :
- **intelligents**, 
- **naturels**, 
- et **adaptatifs**.

Les perspectives incluent l’unification des modules comportementaux dans un **agent cohérent unique**, capable de prendre des décisions robustes à tous les niveaux hiérarchiques.

