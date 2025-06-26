# Étude 4 : *Human Behavior Models for Game-Theoretic Agents: Case of Crowd Tipping*  
*(Silverman, Johns, Cornwell, O’Brien, 2006)*

## Introduction

Cette étude propose un cadre général pour intégrer des comportements humains réalistes dans des agents virtuels utilisés dans des simulateurs (ex. : formation antiterroriste ou gestion de foule). L’objectif est de rendre ces agents plus crédibles en tenant compte de facteurs psychologiques comme le stress, les émotions, la mémoire ou encore les capacités cognitives humaines.

## Objectif

Créer un modèle de comportement permettant à des agents virtuels de réagir de manière plus humaine dans des environnements complexes, en intégrant :

- La **pression émotionnelle et psychologique** (ex. : peur, colère),
- La **prise de décision sous stress ou incertitude**,
- Les **réactions collectives**, notamment dans les foules.

## Méthodologie

Les auteurs développent une **architecture cognitive** composée de quatre sous-systèmes principaux :

### 1. Système cognitif

- Traite les **intentions**, **croyances** et **motivations** de l’agent.
- S’appuie sur une structure de prise de décision proche des humains : choix basé sur les objectifs, l’utilité perçue, et la mémoire d’expériences passées.

### 2. Système émotionnel

- Génère des **réactions émotionnelles** (ex. : peur, joie) à partir d’événements ou d’objectifs affectés.
- S’inspire du **modèle OCC** (une théorie bien connue de l’évaluation des émotions).
- Affecte directement les décisions de l’agent (ex. : un agent apeuré peut fuir au lieu d’attaquer).

### 3. Système physiologique (stress)

- Modélise le **niveau de stress** à partir de plusieurs facteurs (pression temporelle, danger perçu, fatigue…).
- Utilise une formule globale appelée **iSTRESS** pour combiner ces facteurs.
- Le stress influence la **stratégie de décision** de l’agent : calme, hésitant, impulsif, etc.

### 4. Système moteur / expressif

- Transforme les décisions en **actions visibles** (paroles, gestes, mouvements).
- Permet également de **montrer les émotions** : un agent stressé pourra trembler ou fuir.

## Étude de cas : gestion d’une foule

Les chercheurs appliquent leur modèle à une **simulation de manifestation**. Trois types d’agents sont simulés :

- **Civils**, qui peuvent fuir, se regrouper ou devenir agressifs,
- **Terroristes**, qui cherchent à déclencher des émeutes,
- **Forces de sécurité**, qui doivent contrôler la foule sans l’escalader.

Le modèle permet d’observer des **dynamiques collectives** (effet de groupe, panique, contagion émotionnelle) et d’identifier des **moments critiques** où un simple événement peut déclencher une émeute (tipping point).

## Limites

Les auteurs soulignent plusieurs défis :

- **Validation difficile** : les comportements simulés doivent correspondre à des données réelles, ce qui nécessite des études humaines approfondies.
- **Modélisation incomplète** : certains aspects du comportement humain restent mal compris ou peu documentés.
- **Complexité de mise en œuvre** : le réalisme vient avec un coût en temps de calcul et en conception.

## Perspectives

Les pistes envisagées incluent :

- L’amélioration des **ontologies de préoccupations** (valeurs, objectifs moraux) pour personnaliser les comportements,
- Le développement d’**outils de création d’agents** plus accessibles aux concepteurs de simulations,
- La mise en place de **tests de validation comportementale** pour garantir la crédibilité des simulations.

## Conclusion

Ce travail jette les bases d’une nouvelle génération d’agents virtuels plus crédibles, en s’appuyant sur la **psychologie cognitive, émotionnelle et sociale**. Il montre que des systèmes complexes, bien structurés, peuvent simuler des décisions humaines dans des contextes critiques, comme la gestion de foule, et servir à l’entraînement ou à la recherche.

## Référence

- Silverman, B., Johns, M., Cornwell, J., O’Brien, K. (2006). *Human Behavior Models for Game-Theoretic Agents: Case of Crowd Tipping*.  
  [En ligne] https://core.ac.uk/download/pdf/76379137.pdf
