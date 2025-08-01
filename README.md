⚠️ Ce projet est protégé par la licence Creative Commons BY-NC-ND 4.0.  
Usage commercial, modification ou redistribution, réutilisation du code interdits.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/Licence-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)




# 📂 Structure des branches et justification du merge dans `main`

## 🎯 Cette branche `main` contient uniquement le backend

Ce projet (mon_projet) suit une structure multi-branche :

- 🧪 Le **code du backend** est dans la branche : 
           [`creation-apirest`](https://github.com/andorafa/mon_projet/tree/creation-apirest) 
           ou [`sauvegarde-reset-avant-synchro-back`](https://github.com/andorafa/mon_projet/tree/sauvegarde-reset-avant-synchro-back)

- 📱 Le code de l'**application mobile Flutter** est dans la branche
           [`mobile-app-secours`](https://github.com/andorafa/mon_projet/tree/mobile-app-secours)
           ou [`ma-branche-retour-mobile`](https://github.com/andorafa/mon_projet/tree/ma-branche-retour-mobile)

---

### 🛠️ Pourquoi le backend est fusionné dans `main` ?

Le code du backend a été temporairement fusionné dans la branche `main` **uniquement** pour permettre l’analyse de code avec **SonarQube** (version gratuite).

➡️ En effet, **SonarCloud gratuit n’analyse que la branche `main`**, d’où cette intégration technique.

> 🚨 **Important** : pour le moment aucun développement actif ne se fait dans `main`.  
> Pour le moment, toutes les fonctionnalités backend et mobile vont continuer (si besoin) d’évoluer dans `creation-apirest` ou `sauvegarde-reset-avant-synchro-back` et `mobile-app-secours` ou `ma-branche-retour-mobile`.

---

✅ CI/CD, tests, sécurité, et couverture sont toujours configurés sur `creation-apirest` ou `sauvegarde-reset-avant-synchro-back`.  
Ce merge dans `main` est purement **fonctionnel pour les outils de qualité de code.**

---

## 📊 Analyse SonarQube (qualité de code)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=andorafa_mon_projet&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=andorafa_mon_projet)

