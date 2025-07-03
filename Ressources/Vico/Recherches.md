---

# Inteligência Artificial e a Ilusão do Percepto Afetivo

Cette dissertation de master porte sur l’application de l’intelligence artificielle (IA) faible dans le développement de jeux vidéo. L’étude se concentre sur le système **Drivatar**, utilisé dans les jeux *Forza Motorsport* (Turn10 Studios & Microsoft). Le Drivatar simule le comportement humain grâce à l’apprentissage automatique, créant une illusion de présence humaine chez le joueur.

**Chapitres principaux :**

1. **Préparation du terrain**  
   Définitions fondamentales : jeu vidéo, IA, système, apprentissage automatique, algorithmes, interactivité.

2. **Développement des jeux vidéo**  
   Parcours historique : des prototypes analogiques (Tennis for Two) à l’ère numérique, innovations clés (consoles, bots, NPC).

3. **IA faible et émotions fortes**  
   Combinaison de multiples IA spécialisées pour générer une illusion réaliste de comportement humain. Le Drivatar en est l’exemple central il reproduit fidèlement le style de conduite du joueur, voire anticipe ses réactions sur de nouvelles pistes.

> **Objectif :** révéler les stratégies par lesquelles ces IA faibles suscitent des réponses émotionnelles fortes, même en « solo ».  
> **Conclusion :** le Drivatar procure une expérience riche et sociale grâce à une collecte massive de données réelles.

---

# Racing Game AI – Artificial Intelligence for Games

Ce rapport examine les techniques d’IA employées dans les jeux de course automobile, structuré autour de cinq points :

1. **Représentation du circuit**  
   - Approche minimaliste basée sur des nœuds liés  
   - Méthode par secteurs géométriques (lignes de course, lignes de dépassement, types de virages, restrictions)

2. **Trajectoires idéales (*Racing Lines*)**  
   - Lignes fixes enregistrées par des pilotes experts  
   - Lignes dynamiques calculées en temps réel selon conditions et opportunités

3. **Modèles de conduite IA**  
   - Contrôle « user‐like » (accélération, freinage, direction)  
   - Réseaux de neurones artificiels (ANN) pour imiter la conduite  
   - *Drivatar* (Forza Motorsport) : apprentissage des styles de conduite via 5 « leçons » de virages, métriques sur entrée/sortie de virage, régularité

4. **Optimisation des réglages**  
   - Algorithmes génétiques pour trouver les meilleurs réglages selon piste et conditions  
   - Systèmes experts (chaîne de conditions *if–then*) pour choix de pneus, suspension, etc.

5. **Spectateurs et piétons**  
   - Animations fixes pour les foules  
   - Machines à états finis pour réactions (choc, effroi)  
   - Comportements de groupe (*flocking*) et scripts pour environnements immersifs

> **Résultat :** synthèse des méthodes actuelles et propositions novatrices pour rendre les IA de course plus crédibles et adaptatives.

---

# Machine Learning and Games

Cet article retrace l’histoire et l’impact mutuel entre apprentissage automatique et jeux vidéo :

- **Apprentissage du jeu** : jeux comme bancs d’essai (ex. TD-Gammon pour le backgammon).  
- **Modélisation des joueurs** : adapter la stratégie selon adversaires/alliés (Poker).  
- **Capture du comportement** : avatars imitant fidèlement les utilisateurs (Drivatar).  
- **Sélection & stabilité des modèles** : compromis entre expressivité et interprétabilité.  
- **Optimisation pour l’adaptabilité** : ajuster la difficulté pour une expérience ludique équilibrée.  
- **Interprétation des modèles** : rendre visibles les processus décisionnels de l’IA.  
- **Performance technique** : fonctionnement en ressources limitées.

> **Illustrations pratiques** : *Neverwinter Nights*, Omaha Poker, Bridge, Échecs.  
> **Conclusion :** fort potentiel sous-exploité pour enrichir immersion et adaptation en jeux vidéo.

---

# Data Quality in Imitation Learning

En robotique, l’apprentissage par imitation (IL) souffre du manque de données massives ; la **qualité** des démonstrations devient cruciale. Cet article propose une formalisation de la qualité des données via le prisme du *distribution shift*.

## Propriétés clés

1. **Divergence d’action**   
   Écart entre la politique experte et la politique apprise ; faible divergence → meilleure généralisation.

2. **Diversité des transitions**   
   Variabilité (bruit) des transitions état→état ; un peu de bruit améliore la robustesse, trop en dissipe l’apprentissage.

## Apports

- Uniformiser la simple recherche de couverture d’états (diversité d’états) n’est pas optimal ; il faut équilibrer **cohérence des actions** et **diversité contrôlée**.
- Montrer théoriquement et empiriquement que **bruit modéré** dans les données peut faciliter la généralisation.
- Propositions de curation de données :
  - **Minimiser l’entropie** des actions démontrées (consistance).  
  - **Introduire un bruit systémique** mesuré pour augmenter la couverture sans sur-étaler l’apprentissage.  
  - **Contrôler la longueur d’horizon** pour limiter l’accumulation d’erreurs.

> **Conclusion :** cadre formel + recommandations pratiques pour récolter et sélectionner des démonstrations de haute qualité en apprentissage par imitation.  