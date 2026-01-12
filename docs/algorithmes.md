# 🧮 Algorithmes de Plus Court Chemin

## Table des Matières

1. [Algorithme de Dijkstra](#1-algorithme-de-dijkstra)
2. [Algorithme A* (A-étoile)](#2-algorithme-a-a-étoile)
3. [Comparaison théorique](#3-comparaison-théorique)

---

## 1. Algorithme de Dijkstra

### 1.1 Principe

L'algorithme de Dijkstra (1959) résout le problème du plus court chemin depuis une source vers tous les autres sommets dans un graphe à poids positifs.

**Idée principale** : Exploration progressive des sommets par ordre croissant de distance depuis la source.

### 1.2 Invariant

À chaque itération :
- **Ensemble S** : sommets dont la distance minimale est définitivement connue
- **Ensemble Q** : sommets restants avec distance provisoire

**Propriété** : ∀u ∈ S, ∀v ∈ Q : d[u] ≤ d[v]

### 1.3 Pseudo-code

```
DIJKSTRA(G, w, s):
    // Initialisation
    pour chaque sommet v ∈ V:
        d[v] ← +∞              // Distance provisoire
        parent[v] ← NULL       // Prédécesseur
    d[s] ← 0                   // Distance source = 0
    
    Q ← V                       // File de priorité (tous les sommets)
    
    // Boucle principale
    tant que Q ≠ ∅:
        u ← EXTRACT-MIN(Q)      // Sommet de distance minimale
        
        pour chaque voisin v de u:
            // Relaxation
            si d[v] > d[u] + w(u, v):
                d[v] ← d[u] + w(u, v)
                parent[v] ← u
    
    retourner d, parent
```

### 1.4 Opération de Relaxation

**Définition** : Tester si on peut améliorer la distance vers v en passant par u.

```
RELAX(u, v, w):
    si d[v] > d[u] + w(u, v):
        d[v] ← d[u] + w(u, v)
        parent[v] ← u
```

**Analogie** : Comme un ressort qu'on relâche vers une position de moindre énergie.

### 1.5 Reconstruction du Chemin

```
RECONSTRUCT-PATH(parent, s, t):
    chemin ← []
    v ← t
    tant que v ≠ NULL:
        chemin.prepend(v)
        v ← parent[v]
    retourner chemin
```

### 1.6 Preuve de Correction

**Théorème** : À la fin de l'algorithme, ∀v ∈ V : d[v] = δ(s, v)

**Preuve par induction** :
1. **Initialisation** : d[s] = 0 = δ(s, s) ✓
2. **Hérédité** : Supposons la propriété vraie pour tous les sommets de S
3. **Soit u** le prochain sommet extrait (min de Q)
4. **Par l'absurde** : supposons ∃ chemin P de s à u avec w(P) < d[u]
5. Soit y le premier sommet de P hors de S
6. Soit x son prédécesseur dans P (x ∈ S)
7. On a : d[y] ≤ d[x] + w(x, y) ≤ w(P_s→y) < w(P) < d[u]
8. **Contradiction** : car u a été choisi comme minimum de Q

### 1.7 Complexité

**Avec file de priorité (tas binaire)** :

- **Initialisation** : O(n)
- **Extractions** : n × O(log n) = O(n log n)
- **Relaxations** : m × O(log n) = O(m log n)

**Total** : **O((n + m) log n)**

**Avec tas de Fibonacci** : O(n log n + m)

**Complexité spatiale** : O(n + m)

---

## 2. Algorithme A* (A-étoile)

### 2.1 Principe

A* (Hart et al., 1968) est une version **informée** de Dijkstra qui utilise une **heuristique** pour guider la recherche vers la cible.

**Idée** : Prioriser les sommets qui semblent prometteurs pour atteindre la cible rapidement.

### 2.2 Fonction de Coût

Pour chaque sommet v, A* maintient :

```
f(v) = g(v) + h(v)
```

où :
- **g(v)** : coût réel depuis la source s jusqu'à v
- **h(v)** : coût **estimé** de v jusqu'à la cible t (heuristique)
- **f(v)** : coût total estimé d'un chemin s → v → t

### 2.3 Heuristique

**Définition** : h : V → ℝ⁺ estime le coût restant jusqu'à la cible.

**Conditions pour garantir l'optimalité** :

1. **Admissible** : ∀v, h(v) ≤ δ(v, t)
   - Ne jamais surestimer le coût réel

2. **Consistante** : ∀(u, v) ∈ E, h(u) ≤ w(u, v) + h(v)
   - Inégalité triangulaire

**Heuristique choisie** : Distance euclidienne

```
h(v) = √[(x_v - x_t)² + (y_v - y_t)²]
```

**Justification** :
- Admissible ✓ : la ligne droite est le chemin le plus court
- Consistante ✓ : découle de l'inégalité triangulaire euclidienne

### 2.4 Pseudo-code

```
A-STAR(G, w, s, t, h):
    // Initialisation
    pour chaque sommet v ∈ V:
        g[v] ← +∞
        parent[v] ← NULL
    g[s] ← 0
    f[s] ← h(s)
    
    OPEN ← {s}           // File de priorité par f(v)
    CLOSED ← ∅           // Sommets déjà explorés
    
    tant que OPEN ≠ ∅:
        u ← EXTRACT-MIN(OPEN)    // Minimum de f(v)
        
        si u = t:
            retourner RECONSTRUCT-PATH(parent, s, t)
        
        CLOSED ← CLOSED ∪ {u}
        
        pour chaque voisin v de u:
            si v ∈ CLOSED:
                continuer
            
            g_tentative ← g[u] + w(u, v)
            
            si v ∉ OPEN:
                OPEN ← OPEN ∪ {v}
            sinon si g_tentative ≥ g[v]:
                continuer
            
            // Meilleur chemin trouvé
            parent[v] ← u
            g[v] ← g_tentative
            f[v] ← g[v] + h(v)
    
    retourner ÉCHEC    // Pas de chemin
```

### 2.5 Différences avec Dijkstra

| Aspect | Dijkstra | A* |
|--------|----------|-----|
| **Priorité** | g(v) | f(v) = g(v) + h(v) |
| **Direction** | Omnidirectionnelle | Guidée vers la cible |
| **Heuristique** | Non (h = 0) | Oui |
| **Sommets visités** | Beaucoup | Moins (si bonne h) |
| **Garantie optimalité** | Toujours | Si h admissible |

**Remarque** : Dijkstra = A* avec h(v) = 0 pour tout v

### 2.6 Preuve de Correction

**Théorème** : Si h est admissible, A* trouve un plus court chemin.

**Preuve (esquisse)** :
1. Soit P* le plus court chemin de s à t
2. Soit P le chemin trouvé par A*
3. Supposons w(P) > w(P*) (contradiction)
4. Soit v le premier sommet de P* non encore exploré quand t a été atteint
5. On a : f(v) = g(v) + h(v) ≤ g(v) + δ(v, t) = w(P*_{s→v→t}) = w(P*)
6. Or t a été choisi avant v, donc : f(t) ≤ f(v)
7. Mais f(t) = g(t) = w(P) et h(t) = 0
8. Donc : w(P) ≤ w(P*) : **contradiction** ✓

### 2.7 Complexité

**Pire cas** : O((n + m) log n) comme Dijkstra

**Meilleur cas** : O(m) si l'heuristique guide parfaitement

**En pratique** : 
- Nombre de sommets explorés ≪ Dijkstra
- Temps d'exécution significativement réduit

**Facteur de branchement effectif** :
```
b* = (N + 1)^(1/d)
```
où N = sommets explorés, d = profondeur de la solution

---

## 3. Comparaison Théorique

### 3.1 Tableau Comparatif

| Critère | Dijkstra | A* |
|---------|----------|-----|
| **Complexité temporelle** | O((n + m) log n) | O((n + m) log n) |
| **Complexité spatiale** | O(n + m) | O(n + m) |
| **Optimalité** | ✓ Toujours | ✓ Si h admissible |
| **Sommets explorés** | Tous accessibles | Sous-ensemble (si h efficace) |
| **Usage mémoire** | Modéré | Plus élevé (OPEN + CLOSED) |
| **Cas d'usage** | Tous les plus courts chemins | Un seul chemin s → t |
| **Nécessite heuristique** | Non | Oui |

### 3.2 Quand Utiliser Chaque Algorithme ?

**Dijkstra** :
- ✓ Calcul des plus courts chemins depuis s vers **tous** les sommets
- ✓ Pas d'information spatiale disponible
- ✓ Graphe dense
- ✓ Implémentation simple garantie

**A*** :
- ✓ Calcul d'un **seul** plus court chemin s → t
- ✓ Information géométrique disponible (coordonnées)
- ✓ Graphe peu dense
- ✓ Optimisation du temps de calcul critique

### 3.3 Impact de la Qualité de l'Heuristique

**h(v) = 0** : A* = Dijkstra

**h(v) = δ(v, t)** : A* explore uniquement le plus court chemin (optimal)

**h(v) ≈ δ(v, t)** : A* très efficace

**h(v) ≫ δ(v, t)** : A* peut devenir sous-optimal (si h non admissible)

**Compromis** : 
```
h efficace ⟺ h(v) proche de δ(v, t) ET h admissible
```

---

## 4. Variantes et Extensions

### 4.1 Dijkstra Bidirectionnel

**Idée** : Lancer deux recherches simultanées depuis s et t jusqu'à ce qu'elles se rencontrent.

**Complexité** : O(n log n + m) dans le meilleur cas

### 4.2 A* avec Contraintes

**Exemples** :
- Éviter certaines zones (contraintes géographiques)
- Limiter le nombre de virages
- Optimisation multi-objectifs

### 4.3 Algorithmes Plus Avancés

- **Contraction Hierarchies** : Prétraitement pour requêtes ultra-rapides
- **ALT (A*, Landmarks, Triangle)** : Heuristiques basées sur des points de référence
- **D* (Dynamic A*)** : Recalcul efficace lors de changements du graphe

---

## 5. Implémentation : Considérations Pratiques

### 5.1 Structure de Données Cruciale

**File de priorité** :
- Python : `heapq` (tas binaire min)
- Opérations : `heappush`, `heappop` en O(log n)

### 5.2 Optimisations

1. **Arrêt anticipé** : Terminer dès que t est atteint (A*)
2. **Éviter les doublons** : Utiliser un ensemble `visited`
3. **Mise à jour des priorités** : Gérer correctement les réinsertion

### 5.3 Cas Limites

- Graphe non connexe : retourner None ou ∞
- Source = cible : retourner chemin vide, coût 0
- Poids négatifs : algorithme de Bellman-Ford nécessaire

---

## Conclusion

Les algorithmes de Dijkstra et A* sont des outils fondamentaux en optimisation de graphes :

- **Dijkstra** : Garantie d'optimalité, usage universel
- **A*** : Performance supérieure avec information heuristique

Dans le contexte d'un GPS urbain, **A* est préféré** car :
1. On cherche un seul chemin (origine → destination)
2. Les coordonnées géographiques fournissent une excellente heuristique
3. Le gain de performance est significatif sur de grands réseaux

La section suivante (analyse_complexite.md) approfondit l'analyse empirique.


