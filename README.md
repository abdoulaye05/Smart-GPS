# 🚀 Optimisation de Trajets Urbains : GPS Intelligent

**Projet de Modélisation Mathématique et Algorithmique**

*BUT Informatique - Semestre 5*

---

## 👥 Auteurs

- Diallo Abdoulaye
- Semih Taskin
- Muller Arthur

**Date de création** : Novembre 2025

---

## 📖 Vue d'Ensemble

Ce projet explore la **modélisation mathématique** et l'**implémentation algorithmique** d'un système de navigation GPS intelligent. Il combine théorie des graphes, optimisation et programmation Python pour résoudre le problème classique du **plus court chemin** dans un contexte urbain réaliste.

### 🎯 Objectifs

- **Mathématiques** : Modélisation rigoureuse d'une ville sous forme de graphe pondéré
- **Algorithmique** : Implémentation et comparaison de **3 algorithmes** (Dijkstra, A*, Bellman-Ford)
- **Informatique** : Développement Python structuré avec visualisations interactives
- **Analyse** : Étude comparative des performances et complexités
- **Application** : Interface web interactive avec choix des algorithmes et moyens de transport

---

## 🚀 Démarrage Rapide (Pour les Néophytes)

### Étape 1 : Installation

```bash
# 1. Cloner le dépôt (ou télécharger le projet)
git clone <url-du-depot>
cd ProjetS5_maths

# 2. Créer un environnement virtuel Python
python3 -m venv venv

# 3. Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

### Étape 2 : Lancer l'Application Web (Le Plus Simple)

```bash
streamlit run webapp_demo.py
```

L'application s'ouvrira automatiquement dans votre navigateur ! 🎉

### Étape 3 : Comprendre le Projet

1. **Lire la documentation HTML** : Visitez [https://smart-gps.netlify.app](https://smart-gps.netlify.app) ou ouvrez `docs/index.html` localement
2. **Explorer le code** : Commencez par `src/graph.py` puis `src/algorithms.py`
3. **Lire la documentation** : Consultez les fichiers dans `docs/`

---

## 📐 Modélisation Mathématique

### Graphe Urbain

Un réseau routier est modélisé par un graphe **G = (V, E, w)** où :

- **V** : ensemble des sommets (intersections)
- **E ⊆ V × V** : ensemble des arêtes (routes)
- **w : E → ℝ⁺** : fonction de pondération (coût)

### Problème d'Optimisation

**Trouver le chemin de coût minimal** entre un sommet source `s` et un sommet cible `t` :

```
min Σ w(eᵢ) pour tout chemin P de s à t
```

📚 **Pour plus de détails** : Voir `docs/modelisation.md`

---

## 🏗️ Structure du Projet

```
ProjetS5_maths/
│
├── README.md                    # Ce fichier
├── STRUCTURE.md                 # Structure détaillée
├── requirements.txt             # Dépendances Python
├── docs/index.html                      # Documentation HTML complète (aussi sur [Netlify](https://smart-gps.netlify.app))
│
├── src/                         # Code source
│   ├── graph.py                 # Structures de graphes
│   ├── algorithms.py            # 3 algorithmes (Dijkstra, A*, Bellman-Ford)
│   ├── generators.py            # Génération de graphes urbains
│   ├── visualizer.py            # Visualisations
│   └── utils.py                 # Utilitaires
│
├── docs/                        # Documentation technique
│   ├── modelisation.md          # Modélisation mathématique
│   ├── algorithmes.md           # Explications algorithmiques
│   ├── analyse_complexite.md    # Analyse de complexité
│   ├── modele_temps_reel.md     # Modèle de temps réaliste
│   └── conclusion.md            # Conclusion
│
├── experiments/                 # Expériences et tests
│   ├── comparaison_algos.py    # Comparaison des 3 algorithmes
│   ├── impact_trafic.py        # Effet du trafic
│   └── analyse_performance.py  # Mesures de performance
│
├── tests/                       # Tests unitaires
│   ├── test_graph.py
│   ├── test_algorithms.py
│   └── test_temps_reel.py
│
├── figures/                     # Visualisations générées
│
└── webapp_demo.py              # Application web interactive ⭐
```

📚 **Pour plus de détails** : Voir `STRUCTURE.md`

---

## 🔧 Installation Détaillée

### Prérequis

- **Python 3.8+** (testé avec Python 3.14)
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour cloner le dépôt)

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :
- `numpy` : Calculs numériques
- `matplotlib` : Visualisations
- `streamlit` : Application web
- `folium` : Cartes interactives
- `streamlit-folium` : Intégration Streamlit + Folium

### 🎯 Scripts de Lancement Rapide

Pour faciliter l'utilisation du projet, des scripts sont fournis qui automatisent l'installation et le lancement.

#### Sur macOS/Linux : `run.sh`

**Ce que fait `run.sh`** :

1. ✅ **Vérifie Python** : S'assure que Python 3 est installé
2. ✅ **Crée l'environnement virtuel** : Si nécessaire, crée `venv/`
3. ✅ **Active l'environnement** : Active automatiquement l'environnement virtuel
4. ✅ **Installe les dépendances** : Installe les paquets depuis `requirements.txt`
5. ✅ **Affiche un menu** : Propose 5 options pour lancer différentes parties du projet

**Utilisation** :

```bash
# Sur macOS/Linux
./run.sh

# Si vous avez une erreur de permission
chmod +x run.sh
./run.sh
```

**Menu proposé** :

1. **Démonstration interactive (console)** : Lance `demo.py`
2. **Expériences complètes** : Lance `experiments/comparaison_algos.py`
3. **Tests unitaires** : Lance `pytest tests/ -v`
4. **Application web interactive** : Lance `streamlit run webapp_demo.py`
5. **Documentation HTML** : Ouvre `docs/index.html` ou visite [https://smart-gps.netlify.app](https://smart-gps.netlify.app)

#### Sur Windows : `run.bat`

**Ce que fait `run.bat`** :

Même fonctionnalité que `run.sh` mais adapté pour Windows (fichier batch).

**Utilisation** :

```cmd
# Double-cliquez sur run.bat
# OU dans l'invite de commande :
run.bat
```

**Menu proposé** :

1. **Démonstration interactive** : Lance `demo.py`
2. **Expériences complètes** : Lance `experiments/comparaison_algos.py`
3. **Tests unitaires** : Lance `pytest tests/ -v`
4. **Documentation** : Liste les fichiers de documentation

💡 **Astuce** : C'est la méthode la plus simple pour démarrer ! Les scripts gèrent tout automatiquement (environnement virtuel, dépendances, etc.).

---

## 🚀 Utilisation

### Application Web Interactive (Recommandé)

```bash
streamlit run webapp_demo.py
```

**Fonctionnalités** :
- ✅ Sélection de départ/arrivée
- ✅ Choix de l'algorithme (Dijkstra, A*, Bellman-Ford)
- ✅ Choix du moyen de transport (voiture, vélo, à pied)
- ✅ Calcul du temps réaliste avec modèle mathématique
- ✅ Comparaison côte à côte des 3 algorithmes
- ✅ Visualisation interactive sur carte

### Exemple de Code Python

```python
from src.graph import Graph
from src.algorithms import dijkstra, astar, bellman_ford
from src.generators import generate_random_urban_graph

# Créer un graphe urbain
graph = generate_random_urban_graph(
    num_vertices=100,
    avg_degree=4,
    width=0.02,
    height=0.02
)

# Calculer le plus court chemin avec Dijkstra
result = dijkstra(graph, source=0, target=50)

if result.success:
    print(f"Distance : {result.cost:.2f} km")
    print(f"Chemin : {result.path}")
    print(f"Sommets visités : {result.visited_nodes}")
```

### Expériences et Comparaisons

```bash
# Comparaison complète des 3 algorithmes
python experiments/comparaison_algos.py

# Démonstration interactive (console)
python demo.py
```

### Tests Unitaires

```bash
# Lancer tous les tests
pytest tests/ -v

# Lancer un fichier de test spécifique
pytest tests/test_algorithms.py -v
```

---

## 📊 Algorithmes Implémentés

### 1. Dijkstra ⭐

- **Complexité** : O((|V| + |E|) log |V|)
- **Usage** : Graphes avec poids positifs
- **Garantie** : Trouve toujours le plus court chemin
- **Fichier** : `src/algorithms.py`

### 2. A* (A-étoile) ⭐

- **Complexité** : O((|V| + |E|) log |V|)
- **Usage** : Avec heuristique (distance euclidienne)
- **Avantage** : Plus rapide que Dijkstra (explore moins de nœuds)
- **Fichier** : `src/algorithms.py`

### 3. Bellman-Ford 🛡️

- **Complexité** : O(|V| × |E|)
- **Usage** : Graphes avec **poids négatifs possibles**
- **Bonus** : Détecte les cycles négatifs
- **Fichier** : `src/algorithms.py`

### Comparaison

| Algorithme | Poids Négatifs | Heuristique | Complexité | Cas d'Usage |
|------------|---------------|-------------|------------|-------------|
| Dijkstra | ❌ | ❌ | O((n+m) log n) | Standard |
| A* | ❌ | ✅ | O((n+m) log n) | Plus rapide |
| Bellman-Ford | ✅ | ❌ | O(n·m) | Poids négatifs |

📚 **Pour plus de détails** : Voir `docs/algorithmes.md`

---

## 📚 Documentation

### Documentation HTML Interactive

🌐 **Documentation en ligne** : [https://smart-gps.netlify.app](https://smart-gps.netlify.app)

Ou ouvrez localement `docs/index.html` dans votre navigateur pour une documentation complète avec :
- ✅ Formules mathématiques (LaTeX)
- ✅ Visualisations et figures
- ✅ Exemples de code
- ✅ Analyse des résultats

### Documentation Markdown

- **`docs/modelisation.md`** : Modélisation mathématique rigoureuse
- **`docs/algorithmes.md`** : Explications détaillées des algorithmes
- **`docs/analyse_complexite.md`** : Analyse de complexité algorithmique
- **`docs/modele_temps_reel.md`** : Modèle de temps réaliste (t = t₀ + d/v)
- **`docs/conclusion.md`** : Conclusion et perspectives

### Guide de Présentation

- **`COMMENT_PRESENTER.md`** : Guide complet pour la soutenance

---

## 🤝 Contribution (Pour les Néophytes)

### Comment Contribuer ?

Ce projet est ouvert aux contributions ! Voici comment procéder :

#### 1. Fork le Projet (GitHub)

1. Allez sur le dépôt GitHub du projet
2. Cliquez sur le bouton **"Fork"** (en haut à droite)
3. Vous avez maintenant une copie du projet dans votre compte

#### 2. Cloner Votre Fork

```bash
git clone https://github.com/VOTRE-USERNAME/ProjetS5_maths.git
cd ProjetS5_maths
```

#### 3. Créer une Branche

```bash
# Créer une nouvelle branche pour votre contribution
git checkout -b ma-contribution

# Exemples de noms de branches :
# - fix-bug-dijkstra
# - add-new-algorithm
# - improve-documentation
# - add-tests
```

#### 4. Faire vos Modifications

- Modifiez le code ou la documentation
- Ajoutez des commentaires clairs
- Testez vos modifications

#### 5. Commiter vos Changements

```bash
# Ajouter les fichiers modifiés
git add .

# Créer un commit avec un message clair
git commit -m "Description de votre modification"

# Exemples de messages :
# - "Fix: Correction du calcul de distance dans Dijkstra"
# - "Add: Ajout de tests pour Bellman-Ford"
# - "Docs: Amélioration de la documentation des algorithmes"
```

#### 6. Pousser vers GitHub

```bash
git push origin ma-contribution
```

#### 7. Créer une Pull Request

1. Allez sur votre fork GitHub
2. Cliquez sur **"Compare & pull request"**
3. Remplissez le formulaire :
   - **Titre** : Description courte de votre contribution
   - **Description** : Détails de ce que vous avez fait et pourquoi
4. Cliquez sur **"Create pull request"**

### Types de Contributions Bienvenues

- 🐛 **Correction de bugs** : Signaler ou corriger des erreurs
- ✨ **Nouvelles fonctionnalités** : Ajouter des algorithmes ou améliorations
- 📚 **Documentation** : Améliorer la clarté et la complétude
- 🧪 **Tests** : Ajouter des tests unitaires
- 🎨 **Interface** : Améliorer l'application web
- 🔍 **Optimisation** : Améliorer les performances

### Bonnes Pratiques

1. **Code clair** : Utilisez des noms de variables explicites
2. **Commentaires** : Expliquez le "pourquoi", pas le "comment"
3. **Tests** : Ajoutez des tests pour vos nouvelles fonctionnalités
4. **Documentation** : Mettez à jour la documentation si nécessaire
5. **Messages de commit** : Soyez clairs et concis

### Besoin d'Aide ?

- 📖 Lisez la documentation dans `docs/`
- 🔍 Explorez le code existant dans `src/`
- 🧪 Regardez les tests dans `tests/` pour comprendre l'utilisation
- 💬 Créez une issue sur GitHub pour poser une question

---

## 🧪 Tests

### Lancer les Tests

```bash
# Tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_algorithms.py -v
pytest tests/test_graph.py -v
```

### Couverture de Tests

- ✅ **25 tests unitaires** au total
- ✅ Tests sur les graphes (10 tests)
- ✅ Tests sur les algorithmes (10 tests)
- ✅ Tests sur le modèle de temps (5 tests)

---

## 🎓 Concepts Mathématiques

- **Théorie des graphes** : représentations, parcours, plus court chemin
- **Optimisation combinatoire** : problème d'optimisation
- **Complexité algorithmique** : analyse asymptotique (Big O)
- **Heuristiques** : admissibilité, consistance (A*)

---

## 🔍 Analyse Critique

### Points Forts

- ✅ Modélisation réaliste du réseau urbain
- ✅ Comparaison rigoureuse des algorithmes
- ✅ Visualisations claires et pédagogiques
- ✅ Application web interactive
- ✅ Documentation complète et accessible

### Limites

- ⚠️ Graphes statiques (pas de mise à jour en temps réel)
- ⚠️ Simulation simplifiée du trafic
- ⚠️ Pas de prise en compte des feux de circulation

### Perspectives

- 🔮 Intégration de données réelles (OpenStreetMap)
- 🔮 Algorithmes dynamiques (Contraction Hierarchies)
- 🔮 Machine Learning pour prédiction du trafic
- 🔮 Interface mobile (React Native / Flutter)

---

## 📖 Références

1. Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
2. Hart, P. E., et al. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
3. Cormen, T. H., et al. (2009). "Introduction to Algorithms" (3rd ed.)
4. Bellman, R. (1958). "On a routing problem"

---

## 📄 Licence

Ce projet est réalisé dans un cadre pédagogique (BUT Informatique).

Voir `LICENSE` pour plus de détails.

---

## 🆘 Aide et Support

### Problèmes Courants

**Q : L'application web ne démarre pas**  
→ Vérifiez que vous avez activé l'environnement virtuel et installé les dépendances

**Q : Les tests échouent**  
→ Assurez-vous d'avoir installé toutes les dépendances : `pip install -r requirements.txt`

**Q : Comment comprendre le code ?**  
→ Commencez par `src/graph.py` puis `src/algorithms.py`. Lisez les commentaires et la documentation dans `docs/`

**Q : Comment contribuer ?**  
→ Voir la section [Contribution](#-contribution-pour-les-néophytes) ci-dessus

---

## 📊 Statistiques du Projet

- **Lignes de code** : ~5000
- **Fichiers Python** : 15+
- **Tests unitaires** : 25
- **Documentation** : 5 fichiers Markdown + 1 HTML
- **Algorithmes** : 3 (Dijkstra, A*, Bellman-Ford)
- **Figures** : 12+ visualisations

---**Diallo Abdoulaye • Semih Taskin • Muller Arthur**  
**BUT Informatique S5 - Novembre 2025**
