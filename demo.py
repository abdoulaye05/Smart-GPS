#!/usr/bin/env python3
"""
Script de démonstration principal du projet GPS Intelligent.

Ce script illustre les fonctionnalités principales :
- Génération de graphes urbains
- Calcul de plus courts chemins (Dijkstra et A*)
- Visualisations
- Comparaisons de performance

Usage:
    python demo.py
"""

import os
from src.graph import Graph
from src.algorithms import dijkstra, astar, compare_algorithms
from src.generators import (
    generate_grid_graph,
    generate_random_urban_graph,
    generate_realistic_city
)
from src.visualizer import plot_graph, plot_path, plot_comparison
from src.utils import compare_and_print, generate_report_summary
import random


def demo_simple():
    """Démonstration simple sur un petit graphe."""
    print("\n" + "="*70)
    print(" DÉMO 1 : GRAPHE SIMPLE (Triangle)")
    print("="*70)
    
    # Créer un graphe triangulaire simple
    g = Graph(directed=False)
    g.add_vertex(0, 0.0, 0.0, "A")
    g.add_vertex(1, 10.0, 0.0, "B")
    g.add_vertex(2, 5.0, 8.66, "C")
    
    # Ajouter des arêtes avec différents poids
    # Chemin direct : A→B = 15.0
    # Chemin via C : A→C→B = 10.0 + 10.0 = 20.0
    # Le chemin optimal est donc A→B (direct) avec coût 15.0
    g.add_edge(0, 1, weight=15.0)  # Route directe (optimal)
    g.add_edge(0, 2, weight=10.0)  # Chemin alternatif via C
    g.add_edge(2, 1, weight=10.0)  # Complète le chemin via C
    
    print(g.summary())
    print("\nObjectif : Trouver le plus court chemin de A (0) à B (1)")
    
    # Comparer les algorithmes
    results = compare_algorithms(g, 0, 1)
    compare_and_print(results, g)
    
    # Visualiser
    os.makedirs("figures", exist_ok=True)
    plot_path(g, results['astar'].path, title="Démo 1 : Plus Court Chemin (Triangle)",
              save_path="figures/demo1_triangle.png")


def demo_grid():
    """Démonstration sur un graphe en grille."""
    print("\n" + "="*70)
    print(" DÉMO 2 : GRAPHE EN GRILLE (10×10)")
    print("="*70)
    
    # Générer grille
    g = generate_grid_graph(rows=10, cols=10, spacing=100, add_diagonals=False)
    print(g.summary())
    
    # Chemin du coin haut-gauche au coin bas-droite
    source, target = 0, g.num_vertices() - 1
    print(f"\nChemin : coin haut-gauche ({source}) → coin bas-droite ({target})")
    
    # Comparer
    results = compare_algorithms(g, source, target)
    compare_and_print(results, g)
    
    # Visualiser
    plot_path(g, results['astar'].path, path_color='blue',
              title="Démo 2 : Grille 10×10 - Plus Court Chemin",
              save_path="figures/demo2_grid.png")
    
    plot_comparison(results, g, title="Comparaison Dijkstra vs A* (Grille)",
                   save_path="figures/demo2_comparison.png")


def demo_urban():
    """Démonstration sur un graphe urbain réaliste."""
    print("\n" + "="*70)
    print(" DÉMO 3 : VILLE RÉALISTE")
    print("="*70)
    
    # Générer ville moyenne
    g = generate_realistic_city(size="medium")
    print(g.summary())
    
    # Choisir deux points aléatoires éloignés
    vertices = list(g.vertices.keys())
    source = vertices[0]
    target = vertices[-1]
    
    print(f"\nTrajet urbain : {source} → {target}")
    
    # Comparer
    results = compare_algorithms(g, source, target)
    compare_and_print(results, g)
    
    # Vérifier que tous les algorithmes trouvent le même chemin
    if results['dijkstra'].success and results['astar'].success and results['bellman_ford'].success:
        # Vérifier que les chemins sont identiques
        path_dijkstra = tuple(results['dijkstra'].path)
        path_astar = tuple(results['astar'].path)
        path_bf = tuple(results['bellman_ford'].path)
        
        # Vérifier que les coûts sont identiques (tolérance numérique)
        cost_dijkstra = results['dijkstra'].cost
        cost_astar = results['astar'].cost
        cost_bf = results['bellman_ford'].cost
        costs_equal = (abs(cost_dijkstra - cost_astar) < 0.01 and 
                       abs(cost_astar - cost_bf) < 0.01)
        
        paths_equal = (path_dijkstra == path_astar == path_bf)
        
        if paths_equal and costs_equal:
            print("\n✅ CONFIRMATION : Tous les algorithmes trouvent exactement le même chemin !")
        elif costs_equal:
            print("\n✅ CONFIRMATION : Tous les algorithmes trouvent le même coût optimal !")
            print(f"   (Chemins peuvent différer mais coût = {cost_dijkstra:.2f})")
        else:
            print("\n⚠️  ATTENTION : Les coûts diffèrent !")
            print(f"   Dijkstra: {cost_dijkstra:.2f}, A*: {cost_astar:.2f}, Bellman-Ford: {cost_bf:.2f}")
    
    # Visualiser le graphe complet
    plot_graph(g, node_size=20, title="Démo 3 : Réseau Urbain Réaliste",
               save_path="figures/demo3_city_full.png")
    
    # Visualiser le chemin optimal (tous les algorithmes trouvent le même)
    # On affiche celui de A* car c'est le plus rapide, mais c'est identique aux autres
    if results['astar'].success:
        title = "Démo 3 : Chemin Optimal (identique pour Dijkstra, A*, Bellman-Ford)"
        plot_path(g, results['astar'].path, path_color='red',
                  title=title,
                  save_path="figures/demo3_city_path.png")
    
    # Comparaison
    plot_comparison(results, g, title="Comparaison sur Réseau Urbain",
                   save_path="figures/demo3_comparison.png")


def demo_multiple_scenarios():
    """Démonstration avec plusieurs scénarios."""
    print("\n" + "="*70)
    print(" DÉMO 4 : COMPARAISON MULTI-SCÉNARIOS")
    print("="*70)
    
    scenarios = [
        ("Grille 15×15", generate_grid_graph(15, 15, 50)),
        ("Urbain 100 sommets", generate_random_urban_graph(100, 5, 1500, 1500)),
        ("Ville réaliste", generate_realistic_city("small"))
    ]
    
    all_results = {}
    
    for name, graph in scenarios:
        print(f"\n--- {name} ---")
        print(graph.summary())
        
        vertices = list(graph.vertices.keys())
        source = random.choice(vertices)
        target = random.choice([v for v in vertices if v != source])
        
        results = compare_algorithms(graph, source, target)
        all_results[name] = results
        
        print(f"Trajet : {source} → {target}")
        if results['astar'].success:
            print(f"  • Coût : {results['astar'].cost:.2f}")
            print(f"  • Dijkstra : {results['dijkstra'].execution_time * 1000:.2f} ms")
            print(f"  • A* : {results['astar'].execution_time * 1000:.2f} ms")
            # Protection contre division par zéro
            if results['astar'].execution_time > 0:
                speedup = results['dijkstra'].execution_time / results['astar'].execution_time
                print(f"  • Speedup : {speedup:.2f}x")
            else:
                print(f"  • Speedup : N/A (temps d'exécution trop court)")
    
    # Résumé
    print("\n" + "="*70)
    print(" RÉSUMÉ DES SCÉNARIOS")
    print("="*70)
    
    print(f"\n{'Scénario':<25} {'Sommets':<10} {'A* (ms)':<12} {'Speedup':<10}")
    print("-"*60)
    
    for name, results in all_results.items():
        if results['astar'].success:
            # Protection contre division par zéro
            if results['astar'].execution_time > 0:
                speedup = results['dijkstra'].execution_time / results['astar'].execution_time
                speedup_str = f"{speedup:.2f}x"
            else:
                speedup_str = "N/A"
            n = scenarios[[s[0] for s in scenarios].index(name)][1].num_vertices()
            print(f"{name:<25} {n:<10} {results['astar'].execution_time * 1000:<12.2f} {speedup_str:<10}")


def main():
    """Fonction principale."""
    print("\n" + "#"*70)
    print("  PROJET : OPTIMISATION DE TRAJETS URBAINS")
    print("  GPS Intelligent - BUT Informatique S5")
    print("#"*70)
    
    # Créer dossier figures
    os.makedirs("figures", exist_ok=True)
    
    # Menu
    print("\nChoisissez une démonstration :")
    print("  1. Graphe simple (triangle)")
    print("  2. Grille 10×10")
    print("  3. Ville réaliste")
    print("  4. Comparaison multi-scénarios")
    print("  5. Toutes les démos")
    print("  0. Quitter")
    
    try:
        choice = input("\nVotre choix (0-5) : ").strip()
    except KeyboardInterrupt:
        print("\n\nAu revoir !")
        return
    
    if choice == "1":
        demo_simple()
    elif choice == "2":
        demo_grid()
    elif choice == "3":
        demo_urban()
    elif choice == "4":
        demo_multiple_scenarios()
    elif choice == "5":
        demo_simple()
        demo_grid()
        demo_urban()
        demo_multiple_scenarios()
    elif choice == "0":
        print("\nAu revoir !")
        return
    else:
        print("\n⚠️  Choix invalide. Exécution de toutes les démos par défaut.\n")
        demo_simple()
        demo_grid()
        demo_urban()
    
    print("\n" + "="*70)
    print(" DÉMONSTRATION TERMINÉE")
    print("="*70)
    print("\n✓ Les visualisations ont été sauvegardées dans 'figures/'")
    print("\nPour aller plus loin :")
    print("  • Lancez les expériences : python experiments/comparaison_algos.py")
    print("  • Exécutez les tests : pytest tests/")
    print("  • Consultez la documentation : docs/")
    print()


if __name__ == "__main__":
    main()

