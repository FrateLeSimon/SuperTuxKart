# Image-Based Video Game Asset Generation and Evaluation Using Deep Learning: A Systematic Review
## Génération et évaluation d’assets visuels pour jeux vidéo via Deep Learning : une revue systématique

Cet article propose une **revue systématique** des techniques de deep learning appliquées à la **génération et à l’évaluation d’assets visuels** dans les jeux vidéo. L’étude couvre **99 publications évaluées par les pairs entre 2016 et 2023** et fournit une analyse structurée des méthodes, des tendances, des types de contenus visés, et des pratiques d’évaluation dans ce domaine émergent.

---

### Techniques analysées

- **GANs (Generative Adversarial Networks)** : modèle dominant tout au long de la période.
- **Diffusion Models (DMs)** : forte croissance d’intérêt depuis 2022.
- Ces modèles sont utilisés pour générer automatiquement des contenus graphiques variés.

---

### Types d’assets ciblés

- **Textures 2D/3D**
- **Génération de niveaux et de cartes**
- **Modélisation de visages et de personnages**
- **Synthèse de typographies et de polices**
- **Transfert de style**
- Domaines moins explorés : **logos**, **interfaces utilisateur (UI)**, **icônes**.

---

### Méthodes d’évaluation

Les approches d’évaluation sont classées en trois grandes catégories :

1. **Objectifs** : FID, IS, PSNR
2. **Perceptifs** : CLIP Score, SSIM, NIMA
3. **Humains** : études utilisateurs, revues par des experts

--> Les auteurs soulignent l’importance des évaluations **subjectives et qualitatives**, surtout pour des contenus à usage **visuel et interactif**.

---

### Limites identifiées

- **Manque de jeux de données standards** pour entraîner et comparer les modèles.
- **Problèmes de reproductibilité** des expériences.
- **Peu d’attention portée à l’éthique** (ex. : provenance des images, droits d’auteur).
- Appel à des **bonnes pratiques** : benchmarks ouverts, transparence, design centré utilisateur.

---

### Conclusion

- Le deep learning joue un rôle croissant dans la **création automatisée d’assets** pour jeux vidéo.
- Cette revue propose une **feuille de route** claire pour les travaux futurs :
  - diversification des applications,
  - standardisation des outils d’évaluation,
  - adoption de pratiques **éthiques et responsables**.

En somme, les **modèles génératifs profonds** permettent d’**accélérer et enrichir** la production graphique en jeu vidéo — à condition de relever les défis méthodologiques, qualitatifs et éthiques qui l’accompagnent.
