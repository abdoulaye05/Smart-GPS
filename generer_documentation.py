#!/usr/bin/env python3
"""
Générateur de Documentation HTML Interactive
Crée une belle page web avec formules mathématiques, exemples et visualisations
"""

def generer_html():
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPS Intelligent - Documentation Complète</title>
    
    <!-- MathJax pour les formules mathématiques -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <!-- Highlight.js pour la coloration syntaxique -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    
    <!-- Font Awesome pour les icônes -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 40px;
            margin: 20px 0;
        }
        
        header {
            text-align: center;
            padding: 60px 20px;
            color: white;
        }
        
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        h2 {
            color: #667eea;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        h3 {
            color: #764ba2;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 1.5em;
        }
        
        .formula {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .highlight-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .highlight-box h3 {
            color: white;
        }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        pre {
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
        }
        
        pre code {
            background: none;
            padding: 0;
            color: inherit;
        }
        
        .icon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .icon-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .icon-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .icon-item i {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .success { color: #28a745; }
        .warning { color: #ffc107; }
        .danger { color: #dc3545; }
        .info { color: #17a2b8; }
        
        .toc {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .toc ul {
            list-style: none;
        }
        
        .toc li {
            padding: 8px 0;
        }
        
        .toc a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        
        .toc a:hover {
            text-decoration: underline;
        }
        
        .authors {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin: 40px 0;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
            margin: 10px 5px;
        }
        
        .btn:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: white;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <header>
        <h1><i class="fas fa-map-marked-alt"></i> GPS Intelligent</h1>
        <p class="subtitle">Documentation Complète du Projet</p>
        <p style="margin-top: 20px;">Modélisation Mathématique et Algorithmique d'un Système de Navigation</p>
    </header>
    
    <div class="container">
        <!-- Auteurs -->
        <div class="authors">
            <h2 style="color: white; border: none;"><i class="fas fa-users"></i> Équipe Projet</h2>
            <h3 style="color: white; margin-top: 20px;">Diallo Abdoulaye • Semih Taskin • Muller Arthur</h3>
            <p style="margin-top: 10px;">BUT Informatique - Semestre 5</p>
            <p>Novembre 2025</p>
        </div>
        
        <!-- Table des Matières -->
        <div class="card">
            <h2><i class="fas fa-list"></i> Table des Matières</h2>
            <div class="toc">
                <ul>
                    <li><a href="#introduction">1. Introduction</a></li>
                    <li><a href="#modelisation">2. Modélisation Mathématique</a></li>
                    <li><a href="#algorithmes">3. Algorithmes Implémentés</a></li>
                    <li><a href="#temps">4. Modèle de Temps Réaliste</a></li>
                    <li><a href="#architecture">5. Architecture du Projet</a></li>
                    <li><a href="#resultats">6. Résultats et Analyses</a></li>
                    <li><a href="#webapp">7. Application Web</a></li>
                    <li><a href="#conclusion">8. Conclusion</a></li>
                </ul>
            </div>
        </div>
        
        <!-- 1. Introduction -->
        <div class="card" id="introduction">
            <h2><i class="fas fa-flag-checkered"></i> 1. Introduction</h2>
            
            <h3>1.1 Problématique</h3>
            <div class="highlight-box">
                <h3><i class="fas fa-question-circle"></i> Question Centrale</h3>
                <p>Comment <strong>modéliser mathématiquement</strong> un système de navigation GPS et implémenter des algorithmes efficaces pour calculer le plus court chemin en milieu urbain ?</p>
            </div>
            
            <h3>1.2 Objectifs</h3>
            <div class="icon-grid">
                <div class="icon-item">
                    <i class="fas fa-project-diagram"></i>
                    <h4>Modélisation</h4>
                    <p>Représenter une ville comme un graphe pondéré</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-calculator"></i>
                    <h4>Algorithmes</h4>
                    <p>Implémenter Dijkstra et A*</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-clock"></i>
                    <h4>Temps Réel</h4>
                    <p>Modèle de temps urbain réaliste</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-globe"></i>
                    <h4>Interface Web</h4>
                    <p>Application interactive</p>
                </div>
            </div>
        </div>
        
        <!-- 2. Modélisation Mathématique -->
        <div class="card" id="modelisation">
            <h2><i class="fas fa-brain"></i> 2. Modélisation Mathématique</h2>
            
            <h3>2.1 Représentation en Graphe</h3>
            <p>Une ville est modélisée par un <strong>graphe pondéré non orienté</strong> :</p>
            
            <div class="formula">
                $$G = (V, E, w)$$
            </div>
            
            <p>Où :</p>
            <ul>
                <li><strong>\\(V\\)</strong> : ensemble des sommets (intersections)</li>
                <li><strong>\\(E \\subseteq V \\times V\\)</strong> : ensemble des arêtes (routes)</li>
                <li><strong>\\(w: E \\rightarrow \\mathbb{R}^+\\)</strong> : fonction de poids (distance)</li>
            </ul>
            
            <h3>2.2 Problème d'Optimisation</h3>
            <p>Trouver un chemin \\(P = (v_0, v_1, ..., v_k)\\) tel que :</p>
            
            <div class="formula">
                $$\\min_{P} \\sum_{i=0}^{k-1} w(v_i, v_{i+1})$$
                <p style="margin-top: 10px;">Sous contraintes :</p>
                $$v_0 = s \\quad \\text{(départ)}$$
                $$v_k = t \\quad \\text{(arrivée)}$$
                $$(v_i, v_{i+1}) \\in E \\quad \\forall i$$
            </div>
            
            <h3>2.3 Calcul des Poids</h3>
            <p>Distance euclidienne entre deux sommets :</p>
            
            <div class="formula">
                $$w(v_1, v_2) = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
            </div>
            
            <div class="highlight-box">
                <h3><i class="fas fa-lightbulb"></i> Note</h3>
                <p>Si les coordonnées sont en degrés (latitude/longitude), 1° ≈ 111 km.</p>
            </div>
        </div>
        
        <!-- 3. Algorithmes -->
        <div class="card" id="algorithmes">
            <h2><i class="fas fa-microchip"></i> 3. Algorithmes Implémentés</h2>
            
            <h3>3.1 Algorithme de Dijkstra</h3>
            
            <h4><i class="fas fa-info-circle"></i> Principe</h4>
            <p>Exploration <strong>exhaustive</strong> du graphe par distances croissantes.</p>
            
            <h4><i class="fas fa-tachometer-alt"></i> Complexité</h4>
            <div class="formula">
                $$O((n + m) \\log n)$$
                <p style="margin-top: 10px;">Avec \\(n = |V|\\) sommets et \\(m = |E|\\) arêtes</p>
            </div>
            
            <h4><i class="fas fa-code"></i> Pseudo-code</h4>
            <pre><code class="language-python">def dijkstra(G, s, t):
    distances[v] ← ∞ pour tout v ∈ V
    distances[s] ← 0
    Q ← file de priorité avec tous les sommets
    
    tant que Q n'est pas vide:
        u ← extraire_min(Q)
        si u = t: retourner chemin
        
        pour chaque voisin v de u:
            nouvelle_distance ← distances[u] + w(u, v)
            si nouvelle_distance < distances[v]:
                distances[v] ← nouvelle_distance
                parent[v] ← u</code></pre>
            
            <h3>3.2 Algorithme A*</h3>
            
            <h4><i class="fas fa-rocket"></i> Principe</h4>
            <p>Utilise une <strong>heuristique</strong> pour guider la recherche vers la cible.</p>
            
            <h4><i class="fas fa-function"></i> Fonction de Coût</h4>
            <div class="formula">
                $$f(n) = g(n) + h(n)$$
                <p style="margin-top: 10px;">Où :</p>
                $$g(n) = \\text{coût réel depuis le départ}$$
                $$h(n) = \\text{heuristique (estimation du coût restant)}$$
            </div>
            
            <h4><i class="fas fa-ruler"></i> Heuristique : Distance Euclidienne</h4>
            <div class="formula">
                $$h(n) = \\sqrt{(x_n - x_t)^2 + (y_n - y_t)^2}$$
            </div>
            
            <div class="highlight-box">
                <h3><i class="fas fa-check-circle"></i> Admissibilité</h3>
                <p>Cette heuristique est <strong>admissible</strong> car :</p>
                <p style="margin-top: 10px;">$$h(n) \\leq \\text{coût réel restant}$$</p>
                <p style="margin-top: 10px;">(La distance en ligne droite est toujours ≤ distance par routes)</p>
            </div>
            
            <h3>3.3 Comparaison</h3>
            <table>
                <thead>
                    <tr>
                        <th>Critère</th>
                        <th>Dijkstra</th>
                        <th>A*</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Complexité</strong></td>
                        <td>\\(O((n+m) \\log n)\\)</td>
                        <td>\\(O((n+m) \\log n)\\)</td>
                    </tr>
                    <tr>
                        <td><strong>Optimalité</strong></td>
                        <td class="success"><i class="fas fa-check"></i> Oui</td>
                        <td class="success"><i class="fas fa-check"></i> Oui (si h admissible)</td>
                    </tr>
                    <tr>
                        <td><strong>Sommets visités</strong></td>
                        <td>Plus nombreux</td>
                        <td class="success">30-50% de moins</td>
                    </tr>
                    <tr>
                        <td><strong>Vitesse pratique</strong></td>
                        <td>Standard</td>
                        <td class="success">2-3× plus rapide</td>
                    </tr>
                    <tr>
                        <td><strong>Heuristique</strong></td>
                        <td class="danger"><i class="fas fa-times"></i> Non</td>
                        <td class="success"><i class="fas fa-check"></i> Oui</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 4. Modèle de Temps -->
        <div class="card" id="temps">
            <h2><i class="fas fa-stopwatch"></i> 4. Modèle de Temps Réaliste</h2>
            
            <h3>4.1 Problématique</h3>
            <p>Le modèle naïf est <strong>incorrect</strong> en milieu urbain :</p>
            
            <div class="formula">
                $$t = \\frac{d}{v}$$
                <p style="margin-top: 10px; color: #dc3545; font-weight: bold;">❌ FAUX en milieu urbain</p>
            </div>
            
            <p>Car il ignore :</p>
            <ul>
                <li>Le temps de démarrage</li>
                <li>Les feux rouges</li>
                <li>Les arrêts</li>
            </ul>
            
            <h3>4.2 Modèle Proposé</h3>
            <div class="highlight-box">
                <h3><i class="fas fa-star"></i> Formule du Temps Réaliste</h3>
                <div class="formula" style="background: rgba(255,255,255,0.1); border-color: white;">
                    $$t(d) = t_0 + \\frac{d}{v}$$
                </div>
                <p style="margin-top: 15px;">Où :</p>
                <ul style="margin-top: 10px;">
                    <li><strong>\\(t_0\\)</strong> = temps incompressible (démarrage, arrêt, feux)</li>
                    <li><strong>\\(d\\)</strong> = distance en km</li>
                    <li><strong>\\(v\\)</strong> = vitesse moyenne en km/h</li>
                </ul>
            </div>
            
            <h3>4.3 Paramètres Calibrés</h3>
            <table>
                <thead>
                    <tr>
                        <th>Moyen</th>
                        <th>\\(v\\) (km/h)</th>
                        <th>\\(t_0\\) (s)</th>
                        <th>Justification</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>🚗 Voiture</td>
                        <td>50</td>
                        <td>15</td>
                        <td>Démarrage + 1 feu + arrêt</td>
                    </tr>
                    <tr>
                        <td>🚴 Vélo</td>
                        <td>15</td>
                        <td>8</td>
                        <td>Plus agile (moins de feux)</td>
                    </tr>
                    <tr>
                        <td>🚶 À pied</td>
                        <td>5</td>
                        <td>5</td>
                        <td>Démarrage très rapide</td>
                    </tr>
                </tbody>
            </table>
            
            <h3>4.4 Propriétés Mathématiques</h3>
            
            <h4><i class="fas fa-wave-square"></i> Continuité</h4>
            <div class="formula">
                $$t(d) \\in C^{\\infty}(\\mathbb{R}^+)$$
            </div>
            
            <h4><i class="fas fa-chart-line"></i> Croissance</h4>
            <div class="formula">
                $$\\frac{dt}{dd} = \\frac{1}{v} > 0$$
                <p style="margin-top: 10px;">✅ Le temps croît <strong>linéairement</strong> avec la distance</p>
            </div>
            
            <h4><i class="fas fa-arrow-down"></i> Temps Minimum</h4>
            <div class="formula">
                $$t(0) = t_0 > 0$$
                <p style="margin-top: 10px;">✅ Même pour \\(d \\to 0\\), il y a un temps minimum réaliste</p>
            </div>
            
            <h3>4.5 Exemple de Calcul</h3>
            <div class="highlight-box">
                <h4><i class="fas fa-calculator"></i> Trajet de 31 mètres à pied</h4>
                <p style="margin-top: 15px;"><strong>Données :</strong></p>
                <ul>
                    <li>\\(d = 0.031\\) km</li>
                    <li>\\(v = 5\\) km/h</li>
                    <li>\\(t_0 = 5\\) s</li>
                </ul>
                <p style="margin-top: 15px;"><strong>Calcul :</strong></p>
                <div class="formula" style="background: rgba(255,255,255,0.1); border-color: white;">
                    $$t = 5 + \\frac{0.031}{5} \\times 3600 = 5 + 22.3 = 27.3 \\text{ s}$$
                </div>
                <p style="margin-top: 15px;"><strong class="success"><i class="fas fa-check-circle"></i> Réaliste !</strong></p>
            </div>
        </div>
        
        <!-- 5. Architecture -->
        <div class="card" id="architecture">
            <h2><i class="fas fa-sitemap"></i> 5. Architecture du Projet</h2>
            
            <h3>5.1 Structure Modulaire</h3>
            <pre><code class="language-bash">ProjetS5_maths/
├── 🧠 src/                    # Cœur mathématique
│   ├── graph.py              # Classes Vertex, Edge, Graph
│   ├── algorithms.py         # Dijkstra, A*
│   ├── generators.py         # Génération de graphes
│   ├── utils.py              # Utilitaires
│   └── visualizer.py         # Visualisations
│
├── 🌐 webapp_demo.py         # Interface web Streamlit
├── 🧪 experiments/           # Expériences scientifiques
├── ✅ tests/                 # Tests unitaires (25 tests)
└── 📚 docs/                  # Documentation</code></pre>
            
            <h3>5.2 Flux de Données</h3>
            <div class="icon-grid">
                <div class="icon-item">
                    <i class="fas fa-user"></i>
                    <h4>1. Utilisateur</h4>
                    <p>Demande un trajet</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-globe"></i>
                    <h4>2. Interface Web</h4>
                    <p>webapp_demo.py</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-brain"></i>
                    <h4>3. Algorithme</h4>
                    <p>src/algorithms.py</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-chart-line"></i>
                    <h4>4. Résultat</h4>
                    <p>Chemin optimal</p>
                </div>
            </div>
            
            <h3>5.3 Principes</h3>
            <table>
                <thead>
                    <tr>
                        <th>Principe</th>
                        <th>Implémentation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Séparation des responsabilités</strong></td>
                        <td>Logique (src/) ≠ Interface (webapp/)</td>
                    </tr>
                    <tr>
                        <td><strong>Réutilisabilité</strong></td>
                        <td>Même code pour webapp, expériences, tests</td>
                    </tr>
                    <tr>
                        <td><strong>Testabilité</strong></td>
                        <td>Code pur sans dépendances UI</td>
                    </tr>
                    <tr>
                        <td><strong>Maintenabilité</strong></td>
                        <td>1 bug corrigé = tout est corrigé</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 6. Résultats -->
        <div class="card" id="resultats">
            <h2><i class="fas fa-chart-bar"></i> 6. Résultats et Analyses</h2>
            
            <h3>6.1 Validations</h3>
            <div class="icon-grid">
                <div class="icon-item">
                    <i class="fas fa-check-circle success"></i>
                    <h4>Tests Unitaires</h4>
                    <p>25/25 tests passés</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-equals success"></i>
                    <h4>Optimalité</h4>
                    <p>Dijkstra = A*</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-bolt success"></i>
                    <h4>Efficacité</h4>
                    <p>A* 30-50% plus rapide</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-tachometer-alt success"></i>
                    <h4>Complexité</h4>
                    <p>O(n log n) vérifié</p>
                </div>
            </div>
            
            <h3>6.2 Points Forts</h3>
            <table>
                <thead>
                    <tr>
                        <th>Aspect</th>
                        <th>Réalisation</th>
                        <th>Niveau</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Mathématiques</strong></td>
                        <td>Modélisation rigoureuse + preuves</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                    <tr>
                        <td><strong>Algorithmique</strong></td>
                        <td>2 algorithmes implémentés + comparés</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                    <tr>
                        <td><strong>Architecture</strong></td>
                        <td>Code modulaire et réutilisable</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                    <tr>
                        <td><strong>Tests</strong></td>
                        <td>25 tests automatisés</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                    <tr>
                        <td><strong>Documentation</strong></td>
                        <td>5 fichiers MD + doc HTML</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                    <tr>
                        <td><strong>Interface</strong></td>
                        <td>Webapp interactive</td>
                        <td class="success"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 7. Webapp -->
        <div class="card" id="webapp">
            <h2><i class="fas fa-laptop-code"></i> 7. Application Web</h2>
            
            <h3>7.1 Fonctionnalités</h3>
            <ul>
                <li><i class="fas fa-map success"></i> Visualisation du réseau urbain sur carte</li>
                <li><i class="fas fa-mouse-pointer success"></i> Sélection interactive départ/arrivée</li>
                <li><i class="fas fa-random success"></i> Génération aléatoire de points</li>
                <li><i class="fas fa-exchange-alt success"></i> Comparaison Dijkstra vs A*</li>
                <li><i class="fas fa-car success"></i> Choix du moyen de transport (voiture/vélo/pied)</li>
                <li><i class="fas fa-clock success"></i> Calcul de temps réaliste</li>
                <li><i class="fas fa-chart-line success"></i> Statistiques détaillées</li>
            </ul>
            
            <h3>7.2 Lancement</h3>
            <div class="highlight-box">
                <pre><code class="language-bash"># Terminal
cd ProjetS5_maths
source venv/bin/activate  # Windows: venv\\Scripts\\activate
streamlit run webapp_demo.py</code></pre>
                <p style="margin-top: 15px;"><strong><i class="fas fa-arrow-right"></i> L'application s'ouvre dans le navigateur sur http://localhost:8501</strong></p>
            </div>
            
            <h3>7.3 Captures d'Écran</h3>
            <p><em>L'application affiche :</em></p>
            <ul>
                <li>Carte interactive avec le réseau de routes</li>
                <li>Chemin optimal en rouge sur la carte</li>
                <li>Métriques : distance, temps, étapes</li>
                <li>Détails de l'algorithme : sommets visités, arêtes explorées</li>
                <li>Itinéraire détaillé étape par étape</li>
            </ul>
        </div>
        
        <!-- 8. Conclusion -->
        <div class="card" id="conclusion">
            <h2><i class="fas fa-flag-checkered"></i> 8. Conclusion</h2>
            
            <h3>8.1 Objectifs Atteints</h3>
            <div class="icon-grid">
                <div class="icon-item">
                    <i class="fas fa-check-circle success"></i>
                    <h4>Modélisation</h4>
                    <p>Graphe pondéré rigoureux</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-check-circle success"></i>
                    <h4>Algorithmes</h4>
                    <p>Dijkstra + A* opérationnels</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-check-circle success"></i>
                    <h4>Modèle Temps</h4>
                    <p>Formule mathématique justifiée</p>
                </div>
                <div class="icon-item">
                    <i class="fas fa-check-circle success"></i>
                    <h4>Application</h4>
                    <p>Interface web interactive</p>
                </div>
            </div>
            
            <h3>8.2 Compétences Développées</h3>
            <table>
                <thead>
                    <tr>
                        <th>Domaine</th>
                        <th>Compétences</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><i class="fas fa-brain"></i> <strong>Mathématiques</strong></td>
                        <td>Modélisation, théorie des graphes, optimisation</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-code"></i> <strong>Algorithmique</strong></td>
                        <td>Dijkstra, A*, analyse de complexité</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-laptop-code"></i> <strong>Développement</strong></td>
                        <td>Python, POO, architecture modulaire</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-vial"></i> <strong>Tests</strong></td>
                        <td>Pytest, tests unitaires, validation</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-globe"></i> <strong>Web</strong></td>
                        <td>Streamlit, Folium, interfaces interactives</td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-book"></i> <strong>Documentation</strong></td>
                        <td>Markdown, LaTeX, HTML</td>
                    </tr>
                </tbody>
            </table>
            
            <h3>8.3 Perspectives</h3>
            <div class="highlight-box">
                <h4><i class="fas fa-rocket"></i> Extensions Possibles</h4>
                <ul style="margin-top: 15px;">
                    <li><strong>Données réelles</strong> : Intégration OpenStreetMap complète</li>
                    <li><strong>Trafic dynamique</strong> : Modélisation des heures de pointe</li>
                    <li><strong>Multi-critères</strong> : Optimiser temps + coût + confort</li>
                    <li><strong>Machine Learning</strong> : Prédiction du trafic</li>
                    <li><strong>Autres algorithmes</strong> : Bellman-Ford, Floyd-Warshall</li>
                </ul>
            </div>
        </div>
        
        <!-- Commandes Utiles -->
        <div class="card">
            <h2><i class="fas fa-terminal"></i> Commandes Rapides</h2>
            
            <h3><i class="fas fa-play-circle"></i> Lancer l'Application Web</h3>
            <pre><code class="language-bash">cd ProjetS5_maths
source venv/bin/activate
streamlit run webapp_demo.py</code></pre>
            
            <h3><i class="fas fa-vial"></i> Exécuter les Tests</h3>
            <pre><code class="language-bash">cd ProjetS5_maths
source venv/bin/activate
pytest tests/ -v</code></pre>
            
            <h3><i class="fas fa-chart-line"></i> Lancer les Expériences</h3>
            <pre><code class="language-bash">cd ProjetS5_maths
source venv/bin/activate
python3 experiments/comparaison_algos.py</code></pre>
            
            <h3><i class="fas fa-file-code"></i> Fichiers Importants</h3>
            <table>
                <thead>
                    <tr>
                        <th>Fichier</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>README.md</code></td>
                        <td>Documentation principale du projet</td>
                    </tr>
                    <tr>
                        <td><code>webapp_demo.py</code></td>
                        <td>Application web interactive</td>
                    </tr>
                    <tr>
                        <td><code>src/algorithms.py</code></td>
                        <td>Implémentation Dijkstra & A*</td>
                    </tr>
                    <tr>
                        <td><code>tests/test_algorithms.py</code></td>
                        <td>Tests unitaires des algorithmes</td>
                    </tr>
                    <tr>
                        <td><code>docs/modele_temps_reel.md</code></td>
                        <td>Documentation du modèle mathématique</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Références -->
        <div class="card">
            <h2><i class="fas fa-graduation-cap"></i> Références Bibliographiques</h2>
            <ul>
                <li><strong>Dijkstra, E. W.</strong> (1959). "A note on two problems in connexion with graphs". <em>Numerische Mathematik</em>, 1, 269-271.</li>
                <li><strong>Hart, P. E., Nilsson, N. J., & Raphael, B.</strong> (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". <em>IEEE Transactions on Systems Science and Cybernetics</em>, 4(2), 100-107.</li>
                <li><strong>Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C.</strong> (2009). <em>Introduction to Algorithms</em> (3rd ed.). MIT Press.</li>
            </ul>
        </div>
    </div>
    
    <footer>
        <p><i class="fas fa-heart"></i> Fait avec passion par l'équipe ProjetS5 • BUT Informatique 2025</p>
        <p style="margin-top: 10px; opacity: 0.8;">Diallo Abdoulaye • Semih Taskin • Muller Arthur</p>
    </footer>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    print("🚀 Génération de la documentation HTML...")
    
    html_content = generer_html()
    
    # Sauvegarder
    output_file = "Documentation_GPS_Intelligent.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Documentation générée : {output_file}")
    print(f"\n📖 Pour ouvrir : double-cliquez sur le fichier ou tapez :")
    print(f"   open {output_file}  (Mac)")
    print(f"   start {output_file}  (Windows)")
    print(f"   xdg-open {output_file}  (Linux)")

