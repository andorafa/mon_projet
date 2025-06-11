# Structure des branches et justification du merge dans `main`

## 🎯 Cette branche `main` contient uniquement le backend

Ce projet (mon_projet) suit une structure multi-branche :

- 🧪 Le **développement actif du backend** se fait dans la branche [`creation-apirest`](https://github.com/andorafa/mon_projet/tree/creation-apirest)
- 📱 Le code de l'**application mobile Flutter** est dans [`mobile-app`](https://github.com/andorafa/mon_projet/tree/mobile-app)

---

### 🛠️ Pourquoi le backend est fusionné dans `main` ?

Le code du backend a été temporairement fusionné dans la branche `main` **uniquement** pour permettre l’analyse de code avec **SonarQube** (version gratuite).

➡️ En effet, **SonarCloud gratuit n’analyse que la branche `main`**, d’où cette intégration technique.

> 🚨 **Important** : pour le moment aucun développement actif ne se fait dans `main`.  
> Toutes les fonctionnalités backend continuent d’évoluer dans `creation-apirest`.

---

✅ CI/CD, tests, sécurité, et couverture sont toujours configurés sur `creation-apirest`.  
Ce merge dans `main` est purement **fonctionnel pour les outils de qualité de code.**
