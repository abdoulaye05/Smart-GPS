"""
Expérience : Comparaison entre Dijkstra, A* et Bellman-Ford

Compare les trois algorithmes sur différents types de graphes urbains
et analyse leurs performances relatives.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import Graph
from src.algorithms import dijkstra, astar, bellman_ford, compare_algorithms
from src.generators import (
    generate_grid_graph,
    generate_random_urban_graph,
    generate_clustered_urban_graph
)
from src.visualizer import plot_path, plot_comparison
from src.utils import compare_and_print, export_results_to_json
import random


def experiment_grid_graph():
    """Expérience sur graphe en grille."""
    print("\n" + "="*70)
    print(" EXPÉRIENCE 1 : GRAPHE EN GRILLE (Type Manhattan)")
    print("="*70)
    
    # Générer graphe en grille
    graph = generate_grid_graph(rows=20, cols=20, spacing=50, add_diagonals=False)
    print(f"\n{graph.summary()}")
    
    # Choisir source et cible (coins opposés)
    source = 0  # Coin haut-gauche
    target = graph.num_vertices() - 1  # Coin bas-droite
    
    print(f"\nRecherche du plus court chemin : {source} → {target}")
    
    # Comparer les algorithmes
    results = compare_algorithms(graph, source, target)
    
    # Afficher résultats
    compare_and_print(results, graph)
    
    # Visualiser les chemins
    if results['dijkstra'].success:
        plot_path(
            graph,
            results['dijkstra'].path,
            path_color='red',
            title="Dijkstra - Graphe en Grille",
            save_path="figures/exp1_dijkstra_grid.png"
        )
    
    if results['astar'].success:
        plot_path(
            graph,
            results['astar'].path,
            path_color='blue',
            title="A* - Graphe en Grille",
            save_path="figures/exp1_astar_grid.png"
        )
    
    # Comparaison visuelle
    plot_comparison(
        results,
        graph,
        title="Comparaison Dijkstra vs A* (Grille 20×20)",
        save_path="figures/exp1_comparison_grid.png"
    )
    
    return results


def experiment_random_urban():
    """Expérience sur graphe urbain aléatoire."""
    print("\n" + "="*70)
    print(" EXPÉRIENCE 2 : GRAPHE URBAIN ALÉATOIRE")
    print("="*70)
    
    # Générer graphe aléatoire
    graph = generate_random_urban_graph(
        num_vertices=200,
        avg_degree=5,
        width=2000,
        height=2000
    )
    print(f"\n{graph.summary()}")
    
    # Choisir source et cible aléatoires
    vertices = list(graph.vertices.keys())
    source = random.choice(vertices)
    target = random.choice([v for v in vertices if v != source])
    
    print(f"\nRecherche du plus court chemin : {source} → {target}")
    
    # Comparer les algorithmes
    results = compare_algorithms(graph, source, target)
    
    # Afficher résultats
    compare_and_print(results, graph)
    
    # Visualiser
    if results['astar'].success:
        plot_path(
            graph,
            results['astar'].path,
            path_color='green',
            title="A* - Graphe Urbain Aléatoire (200 sommets)",
            save_path="figures/exp2_astar_random.png"
        )
    
    plot_comparison(
        results,
        graph,
        title="Comparaison Dijkstra vs A* (Graphe Aléatoire)",
        save_path="figures/exp2_comparison_random.png"
    )
    
    return results


def experiment_clustered_city():
    """Expérience sur graphe avec structure en clusters."""
    print("\n" + "="*70)
    print(" EXPÉRIENCE 3 : VILLE AVEC QUARTIERS (Clusters)")
    print("="*70)
    
    # Générer ville avec clusters
    graph = generate_clustered_urban_graph(
        num_clusters=5,
        vertices_per_cluster=30,
        cluster_radius=150,
        world_size=2000
    )
    print(f"\n{graph.summary()}")
    
    # Choisir source et cible dans des clusters différents
    vertices = list(graph.vertices.keys())
    source = vertices[0]  # Premier cluster
    target = vertices[-1]  # Dernier cluster
    
    print(f"\nRecherche du plus court chemin : {source} → {target}")
    print("(Entre deux quartiers éloignés)")
    
    # Comparer les algorithmes
    results = compare_algorithms(graph, source, target)
    
    # Afficher résultats
    compare_and_print(results, graph)
    
    # Visualiser
    if results['astar'].success:
        plot_path(
            graph,
            results['astar'].path,
            path_color='purple',
            title="A* - Ville avec Quartiers",
            save_path="figures/exp3_astar_clustered.png"
        )
    
    plot_comparison(
        results,
        graph,
        title="Comparaison Dijkstra vs A* (Ville Clustérisée)",
        save_path="figures/exp3_comparison_clustered.png"
    )
    
    return results


def experiment_all():
    """Lance toutes les expériences et résume."""
    print("\n" + "#"*70)
    print("  SUITE COMPLÈTE D'EXPÉRIENCES")
    print("#"*70)
    
    # Créer le dossier figures s'il n'existe pas
    os.makedirs("figures", exist_ok=True)
    
    # Expérience 1 : Grille
    results1 = experiment_grid_graph()
    
    # Expérience 2 : Aléatoire
    results2 = experiment_random_urban()
    
    # Expérience 3 : Clustérisé
    results3 = experiment_clustered_city()
    
    # Résumé global
    print("\n" + "#"*70)
    print("  RÉSUMÉ GLOBAL DES EXPÉRIENCES")
    print("#"*70)
    
    all_results = {
        "Grille 20×20": results1,
        "Urbain Aléatoire (200 sommets)": results2,
        "Ville Clustérisée (150 sommets)": results3
    }
    
    print(f"\n{'Graphe':<35} {'Dijkstra (ms)':<15} {'A* (ms)':<15} {'Bellman-Ford (ms)':<20} {'Speedup A*':<12}")
    print("-"*100)
    
    for name, results in all_results.items():
        if results['dijkstra'].success and results['astar'].success and results['bellman_ford'].success:
            t_dijk = results['dijkstra'].execution_time * 1000
            t_astar = results['astar'].execution_time * 1000
            t_bf = results['bellman_ford'].execution_time * 1000
            speedup = t_dijk / t_astar if t_astar > 0 else float('inf')
            
            print(f"{name:<35} {t_dijk:<15.2f} {t_astar:<15.2f} {t_bf:<20.2f} {speedup:<12.2f}x")
    
    print("-"*100)
    
    # Sauvegarder résultats
    export_data = {}
    for name, results in all_results.items():
        export_data[name] = {
            "dijkstra": {
                "cost": results['dijkstra'].cost,
                "visited": results['dijkstra'].visited_nodes,
                "time_ms": results['dijkstra'].execution_time * 1000,
                "success": results['dijkstra'].success
            },
            "astar": {
                "cost": results['astar'].cost,
                "visited": results['astar'].visited_nodes,
                "time_ms": results['astar'].execution_time * 1000,
                "success": results['astar'].success
            },
            "bellman_ford": {
                "cost": results['bellman_ford'].cost,
                "visited": results['bellman_ford'].visited_nodes,
                "time_ms": results['bellman_ford'].execution_time * 1000,
                "success": results['bellman_ford'].success
            }
        }
    
    export_results_to_json(export_data, "figures/results_comparaison.json")
    
    print("\n✓ Toutes les expériences sont terminées !")
    print("✓ Les visualisations ont été sauvegardées dans le dossier 'figures/'")


if __name__ == "__main__":
    experiment_all()

