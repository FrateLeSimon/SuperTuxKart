# Étude 3 : *A Game of Thrones – When Human Behavior Models Compete in Repeated Stackelberg Security Games*  
*(Nguyen, Yang, Tambe, et al., 2015)*

## Introduction

Cette étude s'intéresse à la manière dont des individus réagissent lorsqu’ils sont confrontés plusieurs fois à une situation où ils doivent choisir entre attaquer ou se défendre. L’objectif est de concevoir un modèle capable de prédire de manière réaliste les décisions humaines dans ce type de situations, dans le but d’aider à mieux protéger des ressources ou des zones sensibles (par exemple contre le braconnage ou des actes malveillants).

## Objectif

Les chercheurs cherchent à améliorer les modèles existants, souvent trop simplistes, en prenant en compte :

- La façon **imparfaite** dont les humains évaluent leurs chances de réussite,
- La **mémoire** des événements précédents et la manière dont elle influence leurs décisions futures,
- L’**adaptation** progressive de leur comportement au fil du temps.

## Méthodologie

Le modèle proposé, nommé **SHARP**, repose sur deux idées clés :

### 1. Pondération des probabilités perçues

Les humains ne réagissent pas de manière parfaitement logique lorsqu’ils évaluent des chances de succès. Par exemple, une personne peut sous-estimer une forte probabilité ou, à l'inverse, surestimer une faible probabilité. SHARP intègre cette manière de percevoir les risques pour mieux imiter les décisions humaines.

### 2. Adaptation au fil du temps

Lorsqu’un individu subit un échec (par exemple, une attaque échouée), il va chercher à **ajuster sa stratégie** dans les essais suivants. SHARP prend en compte :
- Les tentatives précédentes,
- Les lieux déjà attaqués,
- Les lieux similaires encore non attaqués mais jugés intéressants ou vulnérables.

Ces informations sont utilisées pour prédire les choix futurs de manière plus réaliste.

## Expérimentation : jeu de simulation contre le braconnage

Les chercheurs ont conçu un jeu où des participants jouaient le rôle de braconniers, face à un système défensif simulé par ordinateur. Le but était de tester comment les joueurs adaptaient leur stratégie lorsqu’ils tentaient de capturer des animaux situés à différents endroits. Ce test a été répété sur cinq parties successives avec les mêmes joueurs, afin d’observer leur comportement dans la durée.

## Résultats expérimentaux

Les observations montrent que :

- Le modèle SHARP réussit à prédire beaucoup plus fidèlement le comportement humain que les modèles précédents,
- Les défenseurs contrôlés par ordinateur réussissent mieux lorsqu’ils utilisent SHARP pour anticiper les décisions des attaquants,
- Les décisions des participants reflétaient clairement une perception déformée des chances de réussite, ce que SHARP prend en compte.

Les données ont également confirmé que les attaquants ont tendance à éviter les endroits déjà bien défendus, mais cherchent à tester d’autres cibles proches et apparemment moins risquées.

## Limites des modèles précédents

Avant SHARP, les modèles existants présentaient plusieurs faiblesses :

- Ils considéraient les joueurs comme entièrement rationnels, ce qui n’est pas le cas dans la réalité,
- Ils n’intégraient pas de mécanisme d’adaptation basé sur l’expérience passée,
- Ils utilisaient des calculs de probabilité trop simplifiés, ignorant la manière subjective dont les humains les interprètent.

## Apports du modèle SHARP

- Une représentation plus fidèle du raisonnement humain,
- Une capacité d’apprentissage basée sur les expériences précédentes,
- Une meilleure performance globale dans des situations où les décisions sont répétées et évoluent avec le temps.

## Conclusion

Le modèle SHARP marque une avancée importante dans la modélisation des comportements humains en contexte stratégique. Il montre qu’il est essentiel de tenir compte à la fois de la **perception biaisée du risque** et de **l’apprentissage par l’expérience** pour prédire efficacement les choix d’un individu dans des situations complexes. Ce type de modèle ouvre la voie à de nombreuses applications dans les domaines de la sécurité, de la surveillance ou de la gestion des conflits.

## Référence

- Nguyen, M., Yang, R., Tambe, M., et al. (2015). *A Game of Thrones: When Human Behavior Models Compete in Repeated Stackelberg Security Games*.  
  [En ligne] https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=650309c3be39fbb69fe38ab3709ac6190e478b75
