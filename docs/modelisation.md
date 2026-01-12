# 📐 Modélisation Mathématique

## Introduction

Ce document présente la modélisation mathématique rigoureuse du problème d'optimisation de trajets urbains. Nous utilisons les outils de la théorie des graphes et de l'optimisation combinatoire.

---

## 1. Graphe Urbain : Définitions Formelles

### 1.1 Définition du Graphe

Un **réseau routier** est modélisé par un graphe orienté pondéré :

**G = (V, E, w)**

où :

- **V** : ensemble fini de sommets (intersections, carrefours)
  ```
  V = {v₀, v₁, v₂, ..., vₙ₋₁}  avec |V| = n
  ```

- **E ⊆ V × V** : ensemble des arêtes orientées (routes, segments)
  ```
  E = {(vᵢ, vⱼ) | il existe une route directe de vᵢ vers vⱼ}
  avec |E| = m
  ```

- **w : E → ℝ⁺** : fonction de pondération (coût de traversée)
  ```
  w(vᵢ, vⱼ) = coût pour aller de vᵢ à vⱼ
  ```

### 1.2 Propriétés du Graphe

1. **Graphe orienté** : (vᵢ, vⱼ) ∈ E ⇏ (vⱼ, vᵢ) ∈ E
   - Permet de modéliser les sens uniques

2. **Poids positifs** : ∀e ∈ E, w(e) > 0
   - Assure la terminaison des algorithmes

3. **Connexité** : Pour tout couple (s, t), il existe un chemin de s à t
   - Garantit l'existence d'une solution

### 1.3 Représentations

#### Matrice d'adjacence

**A ∈ ℝⁿˣⁿ** définie par :

```
A[i][j] = {
  w(vᵢ, vⱼ)  si (vᵢ, vⱼ) ∈ E
  +∞         sinon
}
```

- **Complexité spatiale** : O(n²)
- **Avantage** : Accès en O(1)
- **Inconvénient** : Coûteux pour les graphes peu denses

#### Liste d'adjacence

Pour chaque sommet vᵢ ∈ V, on stocke :

```
Adj[vᵢ] = {(vⱼ, w(vᵢ, vⱼ)) | (vᵢ, vⱼ) ∈ E}
```

- **Complexité spatiale** : O(n + m)
- **Avantage** : Optimal pour graphes peu denses
- **Utilisation** : Préférée dans ce projet

---

## 2. Fonctions de Coût

### 2.1 Distance Euclidienne

Pour une arête e = (vᵢ, vⱼ) avec coordonnées (xᵢ, yᵢ) et (xⱼ, yⱼ) :

```
w_distance(e) = √[(xⱼ - xᵢ)² + (yⱼ - yᵢ)²]
```

**Interprétation** : Distance "à vol d'oiseau"

**Propriétés** :
- Symétrique : w(vᵢ, vⱼ) = w(vⱼ, vᵢ)
- Respecte l'inégalité triangulaire

### 2.2 Temps de Trajet

```
w_temps(e) = distance(e) / vitesse(e)
```

où `vitesse(e)` dépend du type de route :
- Autoroute : 110 km/h
- Route nationale : 80 km/h
- Rue urbaine : 50 km/h

**Interprétation** : Temps nécessaire pour parcourir l'arête

### 2.3 Trafic Dynamique

```
w_trafic(e, t) = w_temps(e) × facteur_congestion(e, t)
```

où `facteur_congestion(e, t) ∈ [1, 5]` dépend de :
- L'heure t (heures de pointe)
- Le type de route
- Des événements aléatoires

**Modèle simplifié** :
```
facteur(t) = 1 + 2 × sin²(π(t - 8)/12)  pour t ∈ [7h, 19h]
```

---

## 3. Problème du Plus Court Chemin

### 3.1 Définition d'un Chemin

Un **chemin** P de s à t est une séquence de sommets :

```
P = (v₀ = s, v₁, v₂, ..., vₖ = t)
```

telle que ∀i ∈ {0, ..., k-1}, (vᵢ, vᵢ₊₁) ∈ E

### 3.2 Coût d'un Chemin

Le **coût total** d'un chemin P est :

```
w(P) = Σᵢ₌₀ᵏ⁻¹ w(vᵢ, vᵢ₊₁)
```

### 3.3 Formulation du Problème

**Entrée** :
- Graphe G = (V, E, w)
- Sommet source s ∈ V
- Sommet cible t ∈ V

**Sortie** :
- Chemin P* de s à t tel que :

```
P* = argmin{w(P) | P est un chemin de s à t}
```

**Problème d'optimisation** :

```
minimiser   Σ w(eᵢ)
            eᵢ ∈ P

sous contraintes:
  - P commence en s
  - P termine en t
  - P est un chemin valide (arêtes consécutives)
```

### 3.4 Complexité du Problème

- **Classe** : Polynomial (P)
- **Méthode** : Programmation dynamique
- **Cas particuliers** :
  - Poids tous égaux : BFS en O(n + m)
  - Graphe acyclique : Tri topologique en O(n + m)
  - Poids positifs : Dijkstra en O((n + m) log n)

---

## 4. Distance et Heuristique

### 4.1 Distance Réelle (pour A*)

La **distance réelle** entre deux sommets :

```
δ(s, t) = min{w(P) | P chemin de s à t}
```

### 4.2 Fonction Heuristique

Une **heuristique** h : V → ℝ⁺ estime le coût restant jusqu'à la cible.

**Définitions** :

1. **Admissible** : ∀v ∈ V, h(v) ≤ δ(v, t)
   - Ne surestime jamais le coût réel

2. **Consistante** : ∀(u, v) ∈ E, h(u) ≤ w(u, v) + h(v)
   - Respecte l'inégalité triangulaire

**Heuristique utilisée** (distance euclidienne) :

```
h(v) = √[(x_v - x_t)² + (y_v - y_t)²]
```

**Preuve d'admissibilité** :
- La ligne droite est le chemin le plus court
- Donc h(v) ≤ distance réelle sur le graphe

---

## 5. Propriétés Mathématiques

### 5.1 Principe d'Optimalité de Bellman

Si P* = (s, ..., u, ..., v, ..., t) est un plus court chemin de s à t, alors :
- Le sous-chemin de s à u est un plus court chemin de s à u
- Le sous-chemin de u à v est un plus court chemin de u à v

**Conséquence** : Permet la programmation dynamique

### 5.2 Sous-structure Optimale

```
δ(s, t) = min{δ(s, v) + w(v, t) | (v, t) ∈ E}
```

**Équation de récurrence** :

```
δ(s, v) = min{δ(s, u) + w(u, v) | (u, v) ∈ E}
```

avec condition initiale : δ(s, s) = 0

---

## 6. Métrique de Comparaison

Pour comparer les algorithmes, nous utilisons :

### 6.1 Temps d'exécution

```
T(n, m) = temps CPU en secondes
```

### 6.2 Nombre d'opérations

- **Sommets visités** : |V_explored|
- **Arêtes relaxées** : nombre de mises à jour de distance

### 6.3 Qualité de la solution

```
Ratio = w(P_trouvé) / w(P_optimal)
```

Pour Dijkstra et A* avec heuristique admissible : Ratio = 1 (optimal)

---

## 7. Généralisations

### 7.1 Problème à k destinations

Trouver le plus court chemin de s vers k cibles {t₁, ..., tₖ}

**Solution** : Exécuter Dijkstra depuis s (calcule tous les plus courts chemins)

### 7.2 Optimisation multi-objectifs

Minimiser plusieurs critères simultanément :

```
min (w_temps(P), w_distance(P), w_coût(P))
```

**Solution** : Front de Pareto, compromis

---

## Conclusion

Cette modélisation mathématique fournit le cadre théorique rigoureux nécessaire pour :
1. Justifier les algorithmes implémentés
2. Analyser leur complexité
3. Garantir l'optimalité des solutions
4. Comparer les approches

La partie suivante (algorithmes.md) détaille les algorithmes de résolution.


