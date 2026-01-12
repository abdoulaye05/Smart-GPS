# 🤝 Guide de Contribution

**Bienvenue ! Ce guide vous aidera à contribuer au projet, même si vous êtes débutant.**

---

## 📋 Table des Matières

1. [Pourquoi Contribuer ?](#pourquoi-contribuer)
2. [Comment Commencer ?](#comment-commencer)
3. [Workflow GitHub](#workflow-github)
4. [Types de Contributions](#types-de-contributions)
5. [Standards de Code](#standards-de-code)
6. [Processus de Pull Request](#processus-de-pull-request)

---

## 🎯 Pourquoi Contribuer ?

Contribuer à un projet open source est une excellente façon de :
- ✅ Apprendre de nouveaux concepts
- ✅ Améliorer vos compétences en programmation
- ✅ Collaborer avec d'autres développeurs
- ✅ Créer un portfolio de contributions

**Pas besoin d'être expert !** Même les petites contributions sont précieuses.

---

## 🚀 Comment Commencer ?

### Étape 1 : Explorer le Projet

Avant de contribuer, prenez le temps de comprendre le projet :

1. **Lire le README.md** : Vue d'ensemble du projet
2. **Lancer l'application** : `streamlit run webapp_demo.py`
3. **Explorer le code** : Commencez par `src/graph.py` et `src/algorithms.py`
4. **Lire la documentation** : Consultez les fichiers dans `docs/`

### Étape 2 : Trouver une Contribution

Voici des idées pour commencer :

#### 🐛 Pour les Débutants

- **Corriger des fautes d'orthographe** dans la documentation
- **Améliorer les commentaires** dans le code
- **Ajouter des exemples** dans la documentation
- **Traduire** la documentation dans une autre langue

#### 💻 Pour les Intermédiaires

- **Ajouter des tests unitaires** pour améliorer la couverture
- **Corriger des bugs** signalés dans les issues
- **Améliorer l'interface** de l'application web
- **Optimiser** le code existant

#### 🚀 Pour les Avancés

- **Implémenter de nouveaux algorithmes** (Floyd-Warshall, etc.)
- **Ajouter des fonctionnalités** à l'application web
- **Améliorer les visualisations**
- **Intégrer des données réelles** (OpenStreetMap)

### Étape 3 : Créer une Issue (Optionnel mais Recommandé)

Avant de commencer à coder, créez une issue sur GitHub pour :
- ✅ Discuter de votre idée
- ✅ Éviter le travail en double
- ✅ Obtenir des conseils

**Comment créer une issue** :
1. Allez sur le dépôt GitHub
2. Cliquez sur l'onglet **"Issues"**
3. Cliquez sur **"New Issue"**
4. Remplissez le formulaire avec :
   - **Titre** : Description courte
   - **Description** : Détails de ce que vous voulez faire

---

## 🔄 Workflow GitHub

### 1. Fork le Projet

1. Allez sur le dépôt GitHub du projet
2. Cliquez sur le bouton **"Fork"** (en haut à droite)
3. Vous avez maintenant une copie du projet dans votre compte

### 2. Cloner Votre Fork

```bash
# Remplacer VOTRE-USERNAME par votre nom d'utilisateur GitHub
git clone https://github.com/VOTRE-USERNAME/ProjetS5_maths.git
cd ProjetS5_maths
```

### 3. Ajouter le Dépôt Original comme Remote

```bash
# Remplacer ORIGINAL-OWNER par le propriétaire du dépôt original
git remote add upstream https://github.com/ORIGINAL-OWNER/ProjetS5_maths.git
```

Cela vous permettra de récupérer les mises à jour du projet original.

### 4. Créer une Branche

```bash
# Créer et basculer sur une nouvelle branche
git checkout -b ma-contribution

# Exemples de noms de branches :
# - fix-bug-dijkstra
# - add-tests-bellman-ford
# - improve-documentation
# - add-feature-transport-mode
```

**Convention de nommage** :
- `fix-` : Pour les corrections de bugs
- `add-` : Pour les nouvelles fonctionnalités
- `update-` : Pour les mises à jour
- `docs-` : Pour la documentation
- `test-` : Pour les tests

### 5. Faire vos Modifications

- Modifiez le code ou la documentation
- Ajoutez des commentaires clairs
- Testez vos modifications

**Tester vos modifications** :
```bash
# Lancer les tests
pytest tests/ -v

# Lancer l'application web
streamlit run webapp_demo.py
```

### 6. Commiter vos Changements

```bash
# Voir les fichiers modifiés
git status

# Ajouter les fichiers modifiés
git add .

# Créer un commit avec un message clair
git commit -m "Description de votre modification"
```

**Bonnes pratiques pour les messages de commit** :
- ✅ Utilisez l'impératif : "Add tests" pas "Added tests"
- ✅ Soyez concis mais descriptif
- ✅ Commencez par un préfixe : `Fix:`, `Add:`, `Update:`, `Docs:`

**Exemples** :
```
Fix: Correction du calcul de distance dans Dijkstra
Add: Tests unitaires pour Bellman-Ford
Update: Amélioration de l'interface web
Docs: Ajout d'exemples dans modelisation.md
```

### 7. Pousser vers GitHub

```bash
git push origin ma-contribution
```

Si c'est votre premier push, GitHub vous donnera une URL pour créer la branche à distance.

### 8. Créer une Pull Request

1. Allez sur votre fork GitHub
2. Vous verrez un message "Compare & pull request" - cliquez dessus
3. Remplissez le formulaire :
   - **Titre** : Description courte de votre contribution
   - **Description** : Détails de ce que vous avez fait et pourquoi
   - **Références** : Si votre PR résout une issue, mentionnez-la : "Fixes #123"
4. Cliquez sur **"Create pull request"**

### 9. Répondre aux Commentaires

Les mainteneurs du projet peuvent vous demander des modifications. C'est normal ! 

**Comment répondre** :
1. Faites les modifications demandées
2. Commitez les changements
3. Poussez vers la même branche
4. La Pull Request sera automatiquement mise à jour

---

## 📝 Types de Contributions

### 🐛 Correction de Bugs

1. **Identifier le bug** : Testez l'application et notez le problème
2. **Reproduire** : Créez un test qui reproduit le bug
3. **Corriger** : Modifiez le code pour corriger le bug
4. **Vérifier** : Assurez-vous que le test passe maintenant

### ✨ Nouvelles Fonctionnalités

1. **Discuter** : Créez une issue pour discuter de la fonctionnalité
2. **Implémenter** : Codez la fonctionnalité
3. **Tester** : Ajoutez des tests unitaires
4. **Documenter** : Mettez à jour la documentation

### 📚 Documentation

- Corriger des fautes d'orthographe
- Ajouter des exemples
- Clarifier des explications
- Ajouter des diagrammes

### 🧪 Tests

- Ajouter des tests pour améliorer la couverture
- Tester des cas limites
- Tester des cas d'erreur

---

## 📏 Standards de Code

### Style Python

Nous suivons le style **PEP 8** :

- ✅ Utilisez des noms de variables explicites
- ✅ Limitez les lignes à 80-100 caractères
- ✅ Utilisez 4 espaces pour l'indentation (pas de tabs)
- ✅ Ajoutez des docstrings pour les fonctions

**Exemple** :
```python
def calculate_shortest_path(graph, source, target):
    """
    Calcule le plus court chemin entre deux sommets.
    
    Args:
        graph: Le graphe sur lequel chercher
        source: Sommet de départ
        target: Sommet d'arrivée
    
    Returns:
        PathResult: Résultat contenant le chemin et le coût
    """
    # Votre code ici
    pass
```

### Commentaires

- ✅ Expliquez le **"pourquoi"**, pas le **"comment"**
- ✅ Utilisez des commentaires pour clarifier des parties complexes
- ✅ Évitez les commentaires évidents

**Bon** :
```python
# Utiliser A* car l'heuristique réduit l'exploration de 40%
result = astar(graph, source, target)
```

**Mauvais** :
```python
# Appeler la fonction astar
result = astar(graph, source, target)
```

### Tests

- ✅ Ajoutez des tests pour chaque nouvelle fonctionnalité
- ✅ Testez les cas normaux ET les cas limites
- ✅ Utilisez des noms de tests descriptifs

**Exemple** :
```python
def test_dijkstra_simple_path():
    """Test que Dijkstra trouve le chemin simple."""
    graph = Graph()
    graph.add_vertex(0, 0.0, 0.0)
    graph.add_vertex(1, 1.0, 1.0)
    graph.add_edge(0, 1, weight=5.0)
    
    result = dijkstra(graph, 0, 1)
    
    assert result.success
    assert result.cost == 5.0
    assert result.path == [0, 1]
```

---

## 🔄 Processus de Pull Request

### Avant de Soumettre

- [ ] J'ai testé mes modifications localement
- [ ] J'ai ajouté des tests si nécessaire
- [ ] J'ai mis à jour la documentation si nécessaire
- [ ] Mon code suit les standards du projet
- [ ] J'ai vérifié qu'il n'y a pas de conflits

### Template de Pull Request

```markdown
## Description
Brève description de ce que fait cette PR.

## Type de changement
- [ ] Correction de bug
- [ ] Nouvelle fonctionnalité
- [ ] Amélioration de la documentation
- [ ] Refactoring
- [ ] Tests

## Comment tester ?
1. Étape 1
2. Étape 2
3. Étape 3

## Checklist
- [ ] Mon code suit les standards du projet
- [ ] J'ai ajouté des tests
- [ ] J'ai mis à jour la documentation
- [ ] J'ai vérifié qu'il n'y a pas de conflits
```

---

## ❓ Questions Fréquentes

### Q : Je ne sais pas par où commencer
**R** : Commencez par lire le README.md et explorer le code. Les petites contributions (documentation, commentaires) sont parfaites pour débuter.

### Q : Mon code n'est pas parfait, dois-je quand même contribuer ?
**R** : Oui ! Personne n'est parfait. Les mainteneurs vous aideront à améliorer votre code.

### Q : Comment savoir si ma contribution est bonne ?
**R** : Si elle améliore le projet (même un peu), c'est une bonne contribution !

### Q : Que faire si ma Pull Request est rejetée ?
**R** : Ne vous découragez pas ! Demandez des explications et apprenez de la critique constructive.

---

## 🎉 Merci de Contribuer !

Votre contribution, même petite, est précieuse et appréciée ! 🚀

**Diallo Abdoulaye • Semih Taskin • Muller Arthur**  
**BUT Informatique S5 - Novembre 2025**


