# 🎤 Comment Présenter le Projet - Guide Simple

**Guide étape par étape pour la soutenance** 📋

---

## 🎯 **INTRODUCTION (30 secondes)**

### Ce que vous dites :

> "Bonjour, nous avons développé un **GPS intelligent** qui calcule les plus courts chemins dans une ville.
> 
> Nous avons implémenté **3 algorithmes** (Dijkstra, A*, Bellman-Ford) et créé une **application web interactive**.
> 
> Le projet combine **mathématiques** (théorie des graphes) et **informatique** (Python, Streamlit)."

---

## 📊 **PARTIE 1 : DÉMONSTRATION (3 minutes)**

### Étape 1 : Ouvrir la Documentation HTML (1 min)

**Ce que vous faites** :
```bash
./voir_documentation.sh
```

**Ce que vous dites** :
> "Voici notre documentation interactive. Elle contient :
> - Les formules mathématiques (modélisation du graphe)
> - Les algorithmes expliqués
> - Des graphiques de comparaison
> - Le modèle de temps réaliste : t = t₀ + d/v"

**Montrez** :
- ✅ Une formule mathématique
- ✅ Un graphique de comparaison
- ✅ Le code d'un algorithme

---

### Étape 2 : Lancer l'Application Web (2 min)

**Ce que vous faites** :
```bash
streamlit run webapp_demo.py
```

**Ce que vous dites** :
> "Maintenant, je vais vous montrer l'application web interactive."

**Puis vous montrez** :

1. **Le graphe** :
   > "Voici une ville modélisée avec 100 intersections (sommets) et leurs routes (arêtes)."

2. **Le sélecteur d'algorithmes** :
   > "On peut choisir entre 3 algorithmes :
   > - **A*** (le plus rapide, recommandé)
   > - **Dijkstra** (classique)
   > - **Bellman-Ford** (pour poids négatifs)"

3. **Le choix du transport** :
   > "On peut aussi choisir le moyen de transport : voiture, vélo, ou à pied.
   > Cela change la vitesse et le temps de trajet."

4. **Calculer un trajet** :
   - Sélectionnez un départ et une arrivée
   - Cliquez sur "Calculer le trajet"
   - Montrez le chemin en bleu sur la carte

5. **Les résultats** :
   > "Voici les résultats :
   > - Distance : X km
   > - Temps estimé : Y minutes (calculé avec notre modèle t = t₀ + d/v)
   > - Nombre de sommets visités : Z"

6. **Comparer les algorithmes** :
   - Calculez le même trajet avec **A***
   - Puis avec **Dijkstra**
   - Montrez la différence de temps :
   > "A* est 2× plus rapide car il utilise une heuristique pour se diriger vers la cible."

---

## 💻 **PARTIE 2 : CODE ET TECHNIQUE (2 minutes)**

### Étape 1 : Ouvrir le Code Source

**Ce que vous faites** :
- Ouvrez `src/algorithms.py` dans votre éditeur

**Ce que vous dites** :
> "Voici l'implémentation des algorithmes. Regardons Dijkstra :"

**Montrez** :
- ✅ La structure de la fonction `dijkstra()`
- ✅ L'utilisation de la file de priorité (heapq)
- ✅ La boucle principale

**Expliquez** :
> "Dijkstra utilise une file de priorité pour explorer les sommets par distance croissante.
> Complexité : O((n+m) log n) où n = sommets, m = arêtes."

---

### Étape 2 : Montrer A*

**Ce que vous dites** :
> "A* est similaire mais utilise une heuristique : f(v) = g(v) + h(v)
> où g(v) est la distance parcourue et h(v) est la distance euclidienne restante.
> Cela guide la recherche vers la cible, donc c'est plus rapide."

---

### Étape 3 : Montrer les Tests

**Ce que vous faites** :
```bash
pytest tests/ -v
```

**Ce que vous dites** :
> "Nous avons 31 tests unitaires qui vérifient :
> - La création des graphes
> - Les algorithmes (Dijkstra, A*, Bellman-Ford)
> - Le modèle de temps réaliste
> 
> Tous passent ✅"

---

## 📐 **PARTIE 3 : MATHÉMATIQUES (1 minute)**

### Ce que vous dites :

> "Pour la modélisation mathématique :
> 
> 1. **Graphe** : G = (V, E, w)
>    - V = sommets (intersections)
>    - E = arêtes (routes)
>    - w = poids (distances)
> 
> 2. **Problème d'optimisation** :
>    Trouver le chemin P qui minimise Σ w(e) pour e dans P
> 
> 3. **Modèle de temps** :
>    t = t₀ + d/v
>    - t₀ = temps incompressible (démarrage, arrêt)
>    - d = distance
>    - v = vitesse moyenne"

**Montrez** dans la documentation HTML :
- ✅ La formule du graphe
- ✅ La formule du temps

---

## 🏗️ **PARTIE 4 : ARCHITECTURE (30 secondes)**

### Ce que vous dites :

> "L'architecture est modulaire :
> - `src/` : Code source (graphes, algorithmes)
> - `docs/` : Documentation technique
> - `tests/` : Tests unitaires
> - `experiments/` : Scripts de comparaison
> - `figures/` : Visualisations"

**Montrez** rapidement la structure dans votre IDE.

---

## 🎯 **PARTIE 5 : RÉSULTATS ET COMPARAISON (1 minute)**

### Ce que vous dites :

> "Voici les résultats de nos expériences :
> 
> Sur un graphe de 200 sommets :
> - **A*** : 0.6 ms, visite 95 sommets
> - **Dijkstra** : 1.2 ms, visite 200 sommets
> - **Bellman-Ford** : 85 ms, visite 200 sommets
> 
> **Conclusion** : A* est **2× plus rapide** que Dijkstra car il utilise une heuristique."

**Montrez** un graphique de comparaison dans la documentation HTML.

---

## 🚀 **PARTIE 6 : EXTENSIONS (30 secondes)**

### Ce que vous dites :

> "Pour aller plus loin, nous avons identifié **10 extensions possibles** :
> - Optimisation multi-critères (distance + temps + coût)
> - Trafic dynamique selon l'heure
> - Points d'intérêt obligatoires
> - Machine Learning pour prédire le trafic
> - Etc.
> 
> Tout est documenté dans `docs/extensions_possibles.md`."

---

## ❓ **QUESTIONS PROBABLES ET RÉPONSES**

### Q1 : "Pourquoi A* est plus rapide ?"

**Réponse** :
> "A* utilise une **heuristique** (distance euclidienne) pour guider la recherche vers la cible.
> Au lieu d'explorer dans toutes les directions comme Dijkstra, il se dirige directement vers l'arrivée.
> Résultat : il visite **2× moins de sommets**."

---

### Q2 : "Quelle est la complexité ?"

**Réponse** :
> "Dijkstra et A* : **O((n+m) log n)** où n = sommets, m = arêtes.
> 
> Bellman-Ford : **O(n·m)** donc plus lent.
> 
> En pratique, A* est **2× plus rapide** que Dijkstra grâce à l'heuristique."

---

### Q3 : "Comment calculez-vous le temps ?"

**Réponse** :
> "Avec le modèle : **t = t₀ + d/v**
> 
> - t₀ = temps incompressible (15s pour voiture, 8s pour vélo, 5s à pied)
> - d = distance en km
> - v = vitesse moyenne (50 km/h voiture, 15 km/h vélo, 5 km/h à pied)
> 
> Ce modèle est **réaliste** car il prend en compte le temps de démarrage/arrêt."

---

### Q4 : "Pourquoi seulement 3 algorithmes ?"

**Réponse** :
> "Nous avons choisi les **3 plus pertinents** pour un GPS :
> - **A*** : Le plus rapide (recommandé)
> - **Dijkstra** : Classique, garanti optimal
> - **Bellman-Ford** : Supporte les poids négatifs
> 
> Floyd-Warshall calcule tous les chemins (O(n³)) donc trop lent.
> Bidirectionnel nécessite plus de travail pour être vraiment efficace."

---

### Q5 : "Comment avez-vous testé ?"

**Réponse** :
> "Nous avons **31 tests unitaires** qui vérifient :
> - La création des graphes
> - Les algorithmes sur différents types de graphes
> - Le modèle de temps
> - La cohérence entre algorithmes
> 
> Tous passent ✅"

---

## ⏱️ **TIMING TOTAL (5-7 minutes)**

| Partie | Temps | Action |
|--------|-------|--------|
| Introduction | 30s | Parler |
| Documentation HTML | 1min | Montrer |
| Application web | 2min | Démontrer |
| Code source | 1min | Expliquer |
| Tests | 30s | Lancer |
| Mathématiques | 1min | Expliquer |
| Architecture | 30s | Montrer |
| Résultats | 1min | Comparer |
| Extensions | 30s | Mentionner |
| **TOTAL** | **~8min** | |

---

## ✅ **CHECKLIST AVANT LA SOUTENANCE**

### Préparation (10 minutes avant)

- [ ] Ouvrir `POUR_LE_PROF.md` (avoir sous les yeux)
- [ ] Tester `streamlit run webapp_demo.py` (vérifier que ça marche)
- [ ] Tester `./voir_documentation.sh` (vérifier que ça s'ouvre)
- [ ] Préparer 2-3 trajets de démonstration (départ/arrivée)
- [ ] Ouvrir `src/algorithms.py` dans l'éditeur
- [ ] Préparer le terminal avec `pytest tests/ -v` prêt

### Pendant la présentation

- [ ] Parler clairement et lentement
- [ ] Montrer les choses concrètement (pas juste parler)
- [ ] Faire des pauses pour laisser le prof poser des questions
- [ ] Être confiant (vous avez fait un excellent travail !)

---

## 🎯 **PHRASES CLÉS À RETENIR**

1. **"3 algorithmes implémentés et testés"**
2. **"A* est 2× plus rapide grâce à l'heuristique"**
3. **"Modèle de temps réaliste : t = t₀ + d/v"**
4. **"31 tests unitaires, tous passent"**
5. **"Application web interactive avec choix d'algorithmes"**
6. **"Architecture modulaire et propre"**
7. **"10 extensions proposées pour aller plus loin"**

---

## 💡 **CONSEILS IMPORTANTS**

### ✅ À FAIRE

- **Montrez** plutôt que juste parler
- **Testez** l'application en direct
- **Soyez fiers** de votre travail
- **Expliquez simplement** (pas besoin de jargon)
- **Souriez** et soyez détendus

### ❌ À ÉVITER

- Ne pas juste lire les slides
- Ne pas parler trop vite
- Ne pas paniquer si une question est difficile
- Ne pas dire "je ne sais pas" (dites plutôt "je vais vérifier")

---

## 🏆 **CONCLUSION**

### Ce que vous dites :

> "Pour conclure :
> 
> Nous avons développé un GPS intelligent avec :
> - **3 algorithmes** testés et fonctionnels
> - **Application web** interactive
> - **Documentation** complète
> - **31 tests** unitaires
> 
> Le projet est **complet**, **testé** et **documenté**.
> 
> Merci pour votre attention !"

---

## 📞 **EN CAS DE PROBLÈME**

### L'application ne démarre pas ?

> "Laissez-moi vérifier... Ah, il faut activer l'environnement virtuel."

```bash
source venv/bin/activate
streamlit run webapp_demo.py
```

### Une question difficile ?

> "Excellente question ! Laissez-moi vérifier dans la documentation..."

*Ouvrez `POUR_LE_PROF.md` ou la documentation HTML*

---

## 🎉 **VOUS ÊTES PRÊTS !**

**Souvenez-vous** :
- ✅ Vous avez fait un **excellent travail**
- ✅ Le projet est **complet** et **testé**
- ✅ Vous **maîtrisez** le sujet
- ✅ **Soyez confiants** !

**Bonne chance !** 🚀✨

---

**Diallo Abdoulaye • Semih Taskin • Muller Arthur**  
**BUT Informatique S5 - Novembre 2025**


