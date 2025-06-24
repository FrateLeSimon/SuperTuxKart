# Étude 1 : *How Forza’s Drivatar Actually Works*

## Introduction

Cet article, publié sur *Game Developer*, décrit le fonctionnement du système de **Drivatar**, une IA développée par Turn 10 Studios pour la licence de jeux vidéo *Forza*. Le but est de reproduire un style de conduite humain basé sur des données collectées, afin de générer des agents IA réalistes et personnalisés. Cela permet de pouvoir affronter ses contacts sans qu'il soit connectés.

## Objectif

Explorer comment une IA peut simuler un comportement de conduite humain crédible, non via des règles fixes, mais par modélisation comportementale, en exploitant l’apprentissage machine.

## Méthodologie

- **Modélisation comportementale** : approche basée sur des **réseaux bayésiens** qui correspond modèles probabilistes graphiques qui représentent les relations de dépendance entre différentes variables aléatoires afin d’effectuer des inférences et des prédictions en tenant compte de l’incertitude.
- **Données** : trajectoires, styles (freinage tardif, agressivité, prudence…).
- **Infrastructure** : 
  - Simulation physique à 360 Hz (météo, adhérence, masse…).
  - Stockage et mise à jour dans le cloud (depuis *Forza Motorsport 5*).
- **Couche comportementale** : s’ajuste à la trajectoire optimale fournie par l’IA physique.

## Fonctionnement du système

1. **Modélisation probabiliste** :
   - Le comportement du joueur est analysé et encapsulé dans un Drivatar.
   - Ce dernier peut rouler dans des conditions jamais rencontrées par le joueur, tout en conservant son style (nouvelle piste, météo différente).

2. **Simulation physique et comportementale** :
   - La physique de la course reste indépendante.
   - L’IA applique un style de conduite personnel sur cette base physique.

3. **Contraintes et filtrages** :
   - Évitement des comportements non compétitifs (ex. : marche arrière, rewind).
   - Systèmes correctifs comme le **rubber-banding** qui est une technique utilisée dans les jeux vidéo, notamment de course, qui ajuste dynamiquement la vitesse ou la performance des adversaires pour maintenir une compétition serrée, en ralentissant les leaders ou en accélérant les retardataires pour équilibrer l’expérience.

## Limites

- Certains comportements sont volontairement exclus pour éviter les biais.
- Validation stricte nécessaire pour éviter des IA incohérentes.
- Malgré les progrès, certains ajustements humains restent indispensables.

## Conclusion

Drivatar est un exemple avancé d’intelligence artificielle **orientée style humain**. Il illustre la possibilité de créer des agents capables de simuler des comportements crédibles dans des contextes complexes, en utilisant des approches de machine learning orientées sur la personnalité plutôt que sur la performance optimale.

## Référence

- Game Developer. (2021). *How Forza’s Drivatar Actually Works*. [En ligne] https://www.gamedeveloper.com/design/how-forza-s-drivatar-actually-works