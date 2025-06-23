# Résumé de l’étude : *Observation of the Evolution of Hide and Seek AI*

## Introduction

Cette étude analyse l'émergence de comportements complexes chez des agents d'intelligence artificielle dans un environnement compétitif de cache-cache. Le travail s’inspire des recherches d’OpenAI sur les dynamiques multi-agents où les stratégies se développent sans supervision directe, uniquement par apprentissage par renforcement.

## Objectif

L’objectif est d’observer si des stratégies sophistiquées peuvent émerger naturellement chez des agents, dans un environnement simple, uniquement via des signaux de récompense rudimentaires. Le jeu de cache-cache sert de cadre pour étudier cette dynamique.

## Méthodologie

- **Environnement** : simulation 3D avec agents, murs, blocs, et rampes.
- **Agents** :
  - *Hiders* (cacheurs) : doivent se cacher.
  - *Seekers* (chercheurs) : doivent trouver les cacheurs.
- **Apprentissage** : chaque groupe d’agents est entraîné via l’algorithme PPO (Proximal Policy Optimization), sans accès aux stratégies de l’autre groupe.
- **Récompenses** :
  - Les cacheurs gagnent des points s’ils ne sont pas vus.
  - Les chercheurs gagnent des points s’ils voient un cacheur.
- **Autocurriculum** : l’évolution du niveau d’un groupe pousse l’autre à s’adapter, créant une boucle d’apprentissage dynamique.

## Résultats observés

Des comportements émergents apparaissent en plusieurs phases successives :

1. **Exploration aléatoire** : les agents se déplacent sans stratégie.
2. **Manipulation d’objets** : les cacheurs apprennent à utiliser les blocs pour se construire des abris.
3. **Utilisation des rampes** : les chercheurs apprennent à placer les rampes pour accéder aux cacheurs.
4. **Contre-stratégies** : les cacheurs bloquent les rampes ou les enferment pour éviter leur usage.

Ces comportements ne sont pas programmés manuellement. Ils apparaissent uniquement par adaptation aux objectifs de victoire. À chaque innovation d’un groupe correspond une contre-mesure du groupe opposé.

## Analyse

- **Cacheurs** :
  - Apprentissage de la coopération.
  - Utilisation stratégique de l’environnement.
  - Anticipation des déplacements ennemis.

- **Chercheurs** :
  - Placement des rampes pour franchir les obstacles.
  - Détection de zones à risque.
  - Tentatives d’exploration coordonnées (dans une certaine mesure).

L’étude démontre que l’apprentissage compétitif peut générer des comportements proches de ceux observés chez les humains, y compris l’usage d’outils, sans que ces comportements soient codés explicitement.

## Limites

- La performance des chercheurs plafonne autour de 30 %.
- Les stratégies sont dépendantes de l’environnement simulé.
- Certains comportements sont fragiles : une modification du scénario ou des objets peut casser les stratégies apprises.

## Conclusion

L’expérience montre que dans un environnement compétitif avec des règles simples, des agents peuvent développer des comportements complexes de façon autonome. Ces résultats confirment l’intérêt des environnements multi-agents et de l’autocurriculum pour l’émergence de l’intelligence artificielle collective, sans supervision humaine.

## Références

- Baker, B. et al. (2020). *Emergent Tool Use From Multi-Agent Autocurricula*. arXiv:1909.07528.
- Observation et reproduction dans le cadre du projet étudiant.  
