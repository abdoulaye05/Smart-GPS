# 📊 Analyse de Complexité

## Introduction

Ce document analyse rigoureusement la complexité théorique et empirique des algorithmes implémentés. Nous étudions leur comportement en fonction de la taille et de la structure du graphe.

---

## 1. Complexité Théorique

### 1.1 Notations

- **n = |V|** : nombre de sommets
- **m = |E|** : nombre d'arêtes
- **k** : degré moyen des sommets (m ≈ k·n)

**Types de graphes** :
- **Peu dense** : m = O(n), k = O(1)
- **Dense** : m = O(n²), k = O(n)
- **Planaire** : m = O(n), k ≤ 6 (graphes routiers réels)

### 1.2 Dijkstra : Analyse Détaillée

#### Avec Tableau Simple

```
DIJKSTRA-SIMPLE(G, s):
    Initialisation : O(n)
    Tant que Q ≠ ∅:                          // n itérations
        u ← trouver min dans Q               // O(n)
        pour chaque voisin v de u:           // k voisins en moyenne
            relaxation                        // O(1)
```

**Complexité** : O(n) + n × [O(n) + k × O(1)] = **O(n²)**

**Avantage** : Simple, pas de structure auxiliaire

#### Avec Tas Binaire (Heap)

```
DIJKSTRA-HEAP(G, s):
    Initialisation : O(n)
    Tant que Q ≠ ∅:                          // n itérations
        u ← heappop(Q)                       // O(log n)
        pour chaque voisin v de u:           // Σ deg(u) = 2m au total
            si amélioration:
                heappush/update              // O(log n)
```

**Complexité** :
- Extractions : n × O(log n) = O(n log n)
- Relaxations : m × O(log n) = O(m log n)

**Total** : **O((n + m) log n)**

#### Avec Tas de Fibonacci

**Opérations améliorées** :
- `decrease-key` : O(1) amorti au lieu de O(log n)

**Complexité** : **O(n log n + m)**

**Remarque** : En pratique, le tas binaire est souvent plus rapide (constantes cachées).

### 1.3 A* : Analyse Détaillée

#### Complexité Pire Cas

Dans le pire cas (heuristique inutile), A* = Dijkstra :

**O((n + m) log n)**

#### Complexité Meilleur Cas

Avec heuristique parfaite (h(v) = δ(v, t)) :
- A* explore uniquement les sommets sur le plus court chemin
- Soit k la longueur du chemin

**Complexité** : **O(k log k)** où k ≪ n

#### Complexité Attendue

Avec bonne heuristique :

```
O(b^d log(b^d)) = O(b^d · d)
```

où :
- **d** : profondeur de la solution
- **b** : facteur de branchement effectif

**Empiriquement** : b ≈ 1.2 à 2 pour graphes planaires avec distance euclidienne

### 1.4 Complexité Spatiale

| Algorithme | Espace |
|------------|--------|
| Dijkstra (tableau) | O(n) |
| Dijkstra (heap) | O(n + m) |
| A* | O(n + m) |

**A* utilise** :
- Ensemble OPEN : O(n) dans le pire cas
- Ensemble CLOSED : O(n)
- Stockage de g, f, parent : O(n)

---

## 2. Analyse Asymptotique

### 2.1 Croissance en Fonction de n

Pour un graphe planaire (m ≈ 3n) :

| n | Dijkstra (heap) | A* (meilleur cas) |
|---|-----------------|-------------------|
| 100 | ≈ 700 ops | ≈ 100 ops |
| 1 000 | ≈ 10 000 ops | ≈ 300 ops |
| 10 000 | ≈ 130 000 ops | ≈ 500 ops |
| 100 000 | ≈ 1 700 000 ops | ≈ 800 ops |

**Observation** : Gain factoriel avec A* sur grands graphes

### 2.2 Impact de la Densité

**Graphe peu dense** (m = O(n)) :
- Dijkstra : O(n log n)
- A* : O(n) dans le meilleur cas

**Graphe dense** (m = O(n²)) :
- Dijkstra : O(n² log n)
- A* : O(n² log n) pire cas, mais souvent O(n log n) en pratique

### 2.3 Théorème du Facteur de Branchement

**Définition** : Le facteur de branchement effectif b* vérifie :

```
N = 1 + b* + (b*)² + ... + (b*)^d = (b*^(d+1) - 1) / (b* - 1)
```

où :
- N : nombre de nœuds explorés
- d : profondeur de la solution

**Pour A*** :
```
b* = ((N + 1) · (b - 1))^(1/d) où b ≈ degré moyen
```

**Objectif** : b* → 1 (heuristique parfaite)

---

## 3. Analyse Empirique

### 3.1 Méthodologie

**Protocole expérimental** :
1. Générer des graphes de tailles variées (n ∈ {100, 500, 1000, 5000, 10000})
2. Pour chaque taille, générer 100 instances aléatoires
3. Mesurer :
   - Temps d'exécution (µs)
   - Sommets explorés
   - Arêtes relaxées
4. Calculer moyennes et écarts-types

**Environnement** :
- Python 3.x
- Module `time.perf_counter()` pour mesures précises
- Graphes planaires (représentatifs des réseaux routiers)

### 3.2 Hypothèses à Tester

**H1** : A* explore moins de sommets que Dijkstra
```
|V_explored^A*| < |V_explored^Dijkstra|
```

**H2** : A* est plus rapide que Dijkstra
```
T(A*) < T(Dijkstra)
```

**H3** : L'écart croît avec n
```
ratio(n) = T(Dijkstra, n) / T(A*, n)  croissant
```

**H4** : Qualité de l'heuristique corrélée à la performance
```
b* ∝ 1 / qualité(h)
```

### 3.3 Résultats Attendus

**Graphique 1** : Temps d'exécution vs. taille du graphe
- Axe X : n (échelle logarithmique)
- Axe Y : Temps (ms, échelle logarithmique)
- Courbes : Dijkstra (rouge), A* (bleu)
- Régression : ajustement en O(n log n)

**Graphique 2** : Sommets explorés
- Comparaison du ratio |V_explored| / |V|
- Dijkstra : ≈ 100% (explore tout)
- A* : ≈ 10-30% (guidé par heuristique)

**Graphique 3** : Facteur d'accélération
- Speedup = T_Dijkstra / T_A*
- Attendu : 2x à 10x selon n

### 3.4 Cas Pathologiques

**Cas 1** : Graphe en grille avec cible à l'opposé
- Dijkstra : explore cercles concentriques
- A* : explore "couloir" vers la cible
- Gain maximal

**Cas 2** : Cible entourée d'obstacles
- Les deux algorithmes doivent contourner
- Gain modéré

**Cas 3** : Source = cible
- Terminaison immédiate : O(1)

---

## 4. Analyse de Sensibilité

### 4.1 Impact de l'Heuristique

**Expérience** : Varier la qualité de h

```
h_α(v) = α · distance_euclidienne(v, t)
```

- α = 0 : A* = Dijkstra
- α = 1 : Heuristique normale (admissible)
- α > 1 : Heuristique non admissible (risque de sous-optimalité)

**Mesures** :
- Temps d'exécution
- Optimalité : w(P_trouvé) / w(P_optimal)

**Résultat attendu** :
- α < 1 : Perte de guidage
- α = 1 : Optimal
- α > 1 : Plus rapide mais risque d'erreur

### 4.2 Impact de la Densité

**Expérience** : Varier le degré moyen k

| Graphe | k | m | Dijkstra | A* |
|--------|---|---|----------|-----|
| Sparse | 2.5 | 1.25n | ≈ n log n | ≈ √n |
| Medium | 5 | 2.5n | ≈ 2n log n | ≈ n^0.6 |
| Dense | 10 | 5n | ≈ 5n log n | ≈ n^0.8 |

### 4.3 Impact de la Distribution Spatiale

**Types de graphes testés** :
1. **Grille régulière** : Prédictible, heuristique très efficace
2. **Graphe aléatoire** : Positions uniformes
3. **Graphe clustérisé** : Zones denses + zones sparses
4. **Graphe réaliste** : Basé sur données OpenStreetMap

---

## 5. Profiling et Optimisations

### 5.1 Profiling du Code

**Outils Python** :
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# ... exécution algorithme ...
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 fonctions
```

**Sections critiques attendues** :
1. Opérations sur le tas (40-50% du temps)
2. Calculs de distances (20-30%)
3. Gestion des structures (10-20%)

### 5.2 Optimisations Possibles

**1. Structures de données**
```python
# Utiliser dict avec hash plutôt que recherche linéaire
visited = set()  # O(1) au lieu de list (O(n))
```

**2. Calculs redondants**
```python
# Précalculer les heuristiques
h_cache = {v: heuristic(v, target) for v in V}
```

**3. Arrêt anticipé (A* uniquement)**
```python
if current == target:
    return reconstruct_path()  # Ne pas finir la boucle
```

**4. Utilisation de NumPy**
```python
# Vectorisation pour calculs de distances
distances = np.linalg.norm(positions - target_pos, axis=1)
```

### 5.3 Parallélisation

**Dijkstra bidirectionnel** :
- Lancer s → t et t → s en parallèle
- Arrêter quand les fronts se rencontrent
- Speedup théorique : ×2

---

## 6. Limites Théoriques

### 6.1 Borne Inférieure

**Théorème** : Tout algorithme de plus court chemin dans un graphe général nécessite au moins :

```
Ω(m + n log n)
```

**Preuve** : 
- Doit examiner toutes les arêtes : Ω(m)
- Doit trier/prioriser n sommets : Ω(n log n)

**Conséquence** : Dijkstra est asymptotiquement optimal (à une constante près)

### 6.2 A* : Limite de l'Heuristique

**Lemme** : Même avec heuristique parfaite, A* doit visiter au moins :

```
Ω(k)
```

sommets, où k = longueur du plus court chemin

**En pratique** : A* visite ≈ 2k à 5k sommets (branching)

---

## 7. Comparaison avec Autres Algorithmes

### 7.1 Bellman-Ford

**Avantages** :
- Gère les poids négatifs

**Inconvénients** :
- Complexité : O(n·m)
- Beaucoup plus lent que Dijkstra

### 7.2 Floyd-Warshall

**Usage** : Tous les plus courts chemins (n² paires)

**Complexité** : O(n³)

**Comparaison** : 
- Si on calcule tous les chemins : Dijkstra ×n = O(n²·log n + n·m) < O(n³) pour graphes peu denses

---

## 8. Conclusion de l'Analyse

### 8.1 Résumé

| Critère | Dijkstra | A* |
|---------|----------|-----|
| **Complexité théorique** | O((n+m) log n) | O((n+m) log n) |
| **Complexité pratique** | O(n log n) [planaire] | O(√n) - O(n) [planaire] |
| **Sommets explorés** | ≈ 100% de V | ≈ 10-30% de V |
| **Speedup** | Référence | 2× à 10× |
| **Optimalité** | Garantie | Si h admissible |
| **Cas d'usage** | Universel | Avec info géométrique |

### 8.2 Recommandations

**Utiliser Dijkstra** si :
- Calcul de tous les plus courts chemins depuis s
- Pas d'information géométrique
- Graphe très petit (n < 100)

**Utiliser A*** si :
- Un seul chemin s → t recherché
- Coordonnées disponibles
- Graphe moyen à grand (n > 500)
- Performance critique

### 8.3 Perspectives

**Algorithmes avancés pour aller plus loin** :
- **Contraction Hierarchies** : O(log n) après prétraitement O(n log n)
- **Transit Node Routing** : O(1) sur autoroutes
- **Hub Labeling** : O(k) où k = taille des labels

Ces algorithmes atteignent des performances remarquables sur graphes routiers réels (millions de sommets en millisecondes).

---

## Annexe : Formules de Complexité

### Relations Asymptotiques

```
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(2^n)
```

### Règles de Calcul

1. **Somme** : O(f) + O(g) = O(max(f, g))
2. **Produit** : O(f) × O(g) = O(f · g)
3. **Boucles imbriquées** : n × m = O(n·m)

### Approximations Utiles

- log₂(1000) ≈ 10
- log₂(1 000 000) ≈ 20
- √10 000 = 100


