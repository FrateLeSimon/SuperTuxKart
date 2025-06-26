# MEGA-DAgger: Imitation Learning with Multiple Imperfect Experts
## MEGA-DAgger : Apprentissage par imitation avec plusieurs experts imparfaits

MEGA-DAgger est une méthode d'apprentissage par imitation conçue pour :

- exploiter **plusieurs experts imparfaits** dans des environnements à haut risque (ex. : conduite autonome),
- surpasser les limites des méthodes classiques comme **DAgger** et **HG-DAgger**, qui supposent un expert unique et fiable.

### Objectif

Apprendre une **politique de décision** qui :

- égalise au minimum les meilleurs experts** disponibles,
- tout en **minimisant les comportements risqués**.

---

### Mécanismes clés de MEGA-DAgger

1. **Filtrage basé sur la sécurité**
   - Utilise les **Control Barrier Functions (CBFs)** pour vérifier si une démonstration est sécurisée.
   - Si un expert agit dangereusement (proximité d’obstacle, vitesse excessive), la donnée est **tronqué et exclu** du dataset.
   - Ainsi on évite d’apprendre sur des transitions non sûres.

2. **Résolution des conflits entre experts**
   - Plusieurs experts peuvent proposer des actions différentes à un même instant.
   - MEGA-DAgger compare l’état courant (ex. : scan LiDAR) aux états passés (**similarité cosinus**).
   - Sélection de l’action selon un **score** :
     - sécurité (via CBF),
     - progression vers l’objectif.

3. **Sélection dynamique de l’expert**
   - À chaque itération, l’algorithme identifie l’expert **le plus adapté au contexte** :
     - configuration de piste,
     - trafic,
     - bruit, etc.
   - Permet d’exploiter les **forces complémentaires** sans lisser les comportements.

---

### Expérimentation

- **Environnement** : simulateur réaliste *f1tenth-gym* (une voiture simulée sur une piste).
- **Agents** : réseaux de neurones entraînés sur données LiDAR brutes.
- **Comparaison** : méthodes de référence (HG-DAgger, etc.).

#### Résultats :
- MEGA-DAgger **dépasse les autres méthodes** sur :
  - le taux de collisions,
  - le nombre de tours complétés,
  - la vitesse moyenne,
  - la robustesse.
- Dans certains cas, la politique apprise **fait mieux que tous les experts pris individuellement**.

---

### Validation réelle

- Tests réussis sur un robot **F1TENTH physique**, prouvant la validité au-delà de la simulation.

---

### Perspectives

- Apprentissage automatisé des **niveaux de confiance envers chaque expert**.
- Intégration d’**experts humains dans la boucle**.
- Généralisation vers d’autres domaines critiques où les démonstrations imparfaites sont la norme.

---

### Conclusion

MEGA-DAgger propose une **approche robuste, sûre et évolutive** d’apprentissage par imitation :

- adaptée aux **situations réelles complexes**,
- capable d’agréger des comportements **imparfaits mais complémentaires**,
- sans avoir besoin de **fonction de récompense explicite**.

Une avancée prometteuse pour l’IA embarquée dans des environnements incertains et interactifs.

