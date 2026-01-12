"""
Expérience : Impact du trafic sur les trajets

Simule l'effet de la congestion routière sur les chemins optimaux
et compare comment les algorithmes s'adaptent.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import Graph
from src.algorithms import dijkstra, astar
from src.generators import generate_random_urban_graph, add_traffic_congestion
from src.visualizer import plot_path, plot_comparison
from src.utils import compare_and_print
import random


def experiment_traffic_impact():
    """Expérience sur l'impact du trafic."""
    print("\n" + "="*70)
    print(" EXPÉRIENCE : IMPACT DU TRAFIC ROUTIER")
    print("="*70)
    
    # Générer un graphe de base
    base_graph = generate_random_urban_graph(
        num_vertices=150,
        avg_degree=5,
        width=2000,
        height=2000
    )
    
    print("\n📍 Graphe de base généré")
    print(base_graph.summary())
    
    # Choisir source et cible
    vertices = list(base_graph.vertices.keys())
    source = random.choice(vertices)
    target = random.choice([v for v in vertices if v != source])
    
    print(f"\nTrajet : {source} → {target}")
    
    # Scénario 1 : Sans trafic
    print("\n" + "-"*70)
    print(" SCÉNARIO 1 : Trafic fluide (sans congestion)")
    print("-"*70)
    
    results_no_traffic = {
        'dijkstra': dijkstra(base_graph, source, target),
        'astar': astar(base_graph, source, target)
    }
    
    compare_and_print(results_no_traffic, base_graph)
    
    if results_no_traffic['astar'].success:
        plot_path(
            base_graph,
            results_no_traffic['astar'].path,
            path_color='green',
            title="Trajet Optimal - Trafic Fluide",
            save_path="figures/exp_traffic_no_congestion.png"
        )
    
    # Scénario 2 : Trafic modéré (30% des routes)
    print("\n" + "-"*70)
    print(" SCÉNARIO 2 : Trafic modéré (30% des routes congestionnées)")
    print("-"*70)
    
    # Copier le graphe et ajouter du trafic
    import copy
    graph_moderate = copy.deepcopy(base_graph)
    add_traffic_congestion(graph_moderate, congestion_factor=1.5, affected_ratio=0.3)
    
    results_moderate = {
        'dijkstra': dijkstra(graph_moderate, source, target),
        'astar': astar(graph_moderate, source, target)
    }
    
    compare_and_print(results_moderate, graph_moderate)
    
    if results_moderate['astar'].success:
        plot_path(
            graph_moderate,
            results_moderate['astar'].path,
            path_color='orange',
            title="Trajet Optimal - Trafic Modéré",
            save_path="figures/exp_traffic_moderate.png"
        )
    
    # Scénario 3 : Trafic dense (50% des routes)
    print("\n" + "-"*70)
    print(" SCÉNARIO 3 : Trafic dense (50% des routes congestionnées)")
    print("-"*70)
    
    graph_dense = copy.deepcopy(base_graph)
    add_traffic_congestion(graph_dense, congestion_factor=2.5, affected_ratio=0.5)
    
    results_dense = {
        'dijkstra': dijkstra(graph_dense, source, target),
        'astar': astar(graph_dense, source, target)
    }
    
    compare_and_print(results_dense, graph_dense)
    
    if results_dense['astar'].success:
        plot_path(
            graph_dense,
            results_dense['astar'].path,
            path_color='red',
            title="Trajet Optimal - Trafic Dense",
            save_path="figures/exp_traffic_dense.png"
        )
    
    # Analyse comparative
    print("\n" + "="*70)
    print(" ANALYSE COMPARATIVE DES SCÉNARIOS")
    print("="*70)
    
    print(f"\n{'Scénario':<25} {'Coût (A*)':<15} {'Augmentation':<15}")
    print("-"*55)
    
    cost_base = results_no_traffic['astar'].cost if results_no_traffic['astar'].success else 0
    
    scenarios = [
        ("Trafic fluide", results_no_traffic['astar']),
        ("Trafic modéré (30%)", results_moderate['astar']),
        ("Trafic dense (50%)", results_dense['astar'])
    ]
    
    for name, result in scenarios:
        if result.success:
            increase = ((result.cost - cost_base) / cost_base * 100) if cost_base > 0 else 0
            print(f"{name:<25} {result.cost:<15.2f} +{increase:<14.1f}%")
    
    print("-"*55)
    
    # Observations
    print("\n📊 Observations :")
    print("  • Le trafic augmente significativement le coût des trajets")
    print("  • A* reste efficace même avec congestion")
    print("  • Les chemins alternatifs deviennent plus attractifs")
    
    print("\n✓ Expérience terminée !")


if __name__ == "__main__":
    # Créer le dossier figures
    os.makedirs("figures", exist_ok=True)
    
    experiment_traffic_impact()


