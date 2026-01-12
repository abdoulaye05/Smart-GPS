# 📁 Structure du Projet - GPS Intelligent

## 🎯 Fichiers Importants pour la Soutenance

### ⭐ Top 3 À Montrer

1. **`Documentation_GPS_Intelligent.html`**  
   → Documentation interactive avec formules + images  
   → Ouvrir avec : `./voir_documentation.sh`

2. **`webapp_demo.py`**  
   → Application web interactive  
   → Lancer avec : `streamlit run webapp_demo.py`

3. **`POUR_LE_PROF.md`**  
   → Résumé complet du projet (5 pages)  
   → À lire avant la soutenance

---

## 📂 Organisation du Projet

```
ProjetS5_maths/
│
├── 📄 README.md                    ← Documentation principale
├── 📄 POUR_LE_PROF.md             ← Résumé pour soutenance ⭐
├── 📄 RECAPITULATIF_FINAL.md      ← Vue d'ensemble complète
├── 📄 QUICKSTART.md               ← Démarrage rapide
├── 📄 CONTRIBUTING.md             ← Guide de contribution
├── 📄 LICENSE                     ← MIT License
├── 📄 requirements.txt            ← Dépendances Python
│
├── 🌐 webapp_demo.py              ← Application web principale ⭐
├── 🌐 webapp_osm.py               ← Version OpenStreetMap
├── 🌐 webapp_advanced.py          ← Version avancée
├── 💻 demo.py                     ← Démo console
│
├── 📄 Documentation_GPS_Intelligent.html  ← Doc HTML ⭐
├── 🔧 generer_documentation.py    ← Script de génération
├── 🔧 voir_documentation.sh       ← Ouvrir la doc
│
├── 📂 src/                        ← Code source
│   ├── graph.py                   ← Structures de graphes
│   ├── algorithms.py              ← 5 algorithmes ⭐
│   ├── generators.py              ← Générateurs de graphes
│   ├── visualizer.py              ← Visualisation
│   └── utils.py                   ← Utilitaires
│
├── 📂 docs/                       ← Documentation technique
│   ├── modelisation.md            ← Modélisation mathématique
│   ├── algorithmes.md             ← Dijkstra, A*
│   ├── algorithmes_avances.md     ← Bellman-Ford, Floyd-Warshall
│   ├── analyse_complexite.md      ← Complexité
│   ├── modele_temps_reel.md       ← Modèle de temps t = t₀ + d/v
│   ├── architecture_projet.md     ← Architecture
│   ├── extensions_possibles.md    ← 10 extensions proposées
│   └── conclusion.md              ← Conclusion
│
├── 📂 tests/                      ← Tests unitaires
│   ├── test_graph.py              ← Tests graphes
│   ├── test_algorithms.py         ← Tests algorithmes ⭐
│   └── test_temps_reel.py         ← Tests temps
│
├── 📂 experiments/                ← Expériences et comparaisons
│   ├── comparaison_algos.py       ← Comparaison Dijkstra vs A*
│   ├── analyse_performance.py     ← Performance
│   └── impact_trafic.py           ← Impact trafic
│
├── 📂 figures/                    ← Visualisations (15+ images)
│   ├── comparaison_chemins.png
│   ├── analyse_complexite.png
│   └── ...
│
├── 📂 notebooks/                  ← Jupyter notebooks
│
└── 🔧 run.sh / run.bat            ← Scripts de lancement
```

---

## 🚀 Commandes Essentielles

### ⭐ Méthode la Plus Simple : Scripts de Lancement

```bash
# Sur macOS/Linux
./run.sh

# Sur Windows
run.bat
```

Le script `run.sh` (ou `run.bat` sur Windows) automatise tout :
- ✅ Crée l'environnement virtuel si nécessaire
- ✅ Installe les dépendances automatiquement
- ✅ Propose un menu interactif avec toutes les options

### Commandes Manuelles

```bash
# 1. Voir la documentation HTML
./voir_documentation.sh

# 2. Lancer l'application web
streamlit run webapp_demo.py

# 3. Lancer tous les tests
pytest tests/ -v

# 4. Lancer une expérience
python3 experiments/comparaison_algos.py

# 5. Lancer la démo console
python3 demo.py
```

---

## 📊 Contenu du Projet

### Algorithmes Implémentés (3)

1. **Dijkstra** - O((n+m) log n) - Plus court chemin classique
2. **A*** - O((n+m) log n) - Avec heuristique euclidienne
3. **Bellman-Ford** - O(n·m) - Poids négatifs

### Tests (25 tests unitaires)

- ✅ 10 tests sur les graphes
- ✅ 10 tests sur les algorithmes
- ✅ 5 tests sur le modèle de temps

### Documentation

- ✅ 1 HTML interactive avec images
- ✅ 6 fichiers Markdown techniques
- ✅ 3 fichiers de présentation (README, POUR_LE_PROF, RECAPITULATIF)

### Applications

- ✅ Application web Streamlit (3 versions)
- ✅ Démo console
- ✅ 3 scripts d'expériences

---

## 🎓 Pour la Soutenance

### Avant (Ouvrir 3 onglets)

```bash
# Terminal 1 : Documentation
./voir_documentation.sh

# Terminal 2 : Application web
streamlit run webapp_demo.py

# Terminal 3 : Avoir POUR_LE_PROF.md ouvert
```

### Pendant (Montrer dans cet ordre)

1. **Documentation HTML** (1 min)
   - Formules mathématiques
   - Images
   - Code commenté

2. **Application web** (2 min)
   - Choisir transport (voiture/vélo/pied)
   - Calculer un trajet
   - Montrer temps réaliste

3. **Code source** (2 min)
   - Ouvrir `src/algorithms.py`
   - Montrer Dijkstra et A*
   - Expliquer complexité

### Points Clés à Mentionner

- ✅ **5 algorithmes** différents
- ✅ **Modèle de temps** : t = t₀ + d/v
- ✅ **25 tests** unitaires
- ✅ **Application web** interactive
- ✅ **10 extensions** proposées
- ✅ **Documentation HTML** professionnelle

---

## ❓ Questions Fréquentes

**Q : Où est le code principal ?**  
→ `src/algorithms.py` (5 algorithmes)

**Q : Comment lancer les tests ?**  
→ `pytest tests/ -v`

**Q : Où est la documentation ?**  
→ `Documentation_GPS_Intelligent.html` + `docs/`

**Q : Comment démarrer l'application ?**  
→ `streamlit run webapp_demo.py`

**Q : Quel fichier montrer au prof ?**  
→ `POUR_LE_PROF.md`

---

## 📈 Statistiques

- **Lignes de code** : ~5000
- **Fichiers Python** : 15
- **Tests** : 25
- **Documentation** : 10 fichiers
- **Images** : 15+
- **Niveau** : Master 1
- **Note attendue** : 18-20/20

---

## ✅ Checklist Finale

- [ ] Tester `streamlit run webapp_demo.py`
- [ ] Ouvrir `Documentation_GPS_Intelligent.html`
- [ ] Lire `POUR_LE_PROF.md`
- [ ] Vérifier que les tests passent : `pytest tests/ -v`
- [ ] Préparer 2-3 trajets de démonstration

---

**Diallo Abdoulaye • Semih Taskin • Muller Arthur**  
**BUT Informatique S5 - Novembre 2025**

