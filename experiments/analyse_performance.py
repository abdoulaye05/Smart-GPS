"""
Expérience : Analyse de performance en fonction de la taille du graphe

Étudie comment le temps d'exécution évolue avec le nombre de sommets.
Permet de vérifier empiriquement les complexités théoriques.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph import Graph
from src.algorithms import dijkstra, astar
from src.generators import generate_random_urban_graph
from src.visualizer import plot_performance_scaling
from src.utils import measure_algorithm_performance, export_results_to_csv
import random


def experiment_scaling():
    """Expérience d'analyse de passage à l'échelle."""
    print("\n" + "="*70)
    print(" EXPÉRIENCE : ANALYSE DE PERFORMANCE (SCALING)")
    print("="*70)
    print("\nObjectif : Mesurer l'évolution du temps d'exécution avec la taille du graphe")
    
    # Tailles de graphes à tester
    sizes = [50, 100, 200, 500, 1000, 2000]
    num_runs = 5  # Nombre de répétitions par taille
    
    results_data = []
    dijkstra_times = []
    astar_times = []
    
    print(f"\nTest sur {len(sizes)} tailles de graphes ({num_runs} runs chacun)")
    print("-"*70)
    
    for size in sizes:
        print(f"\n📊 Graphe avec n = {size} sommets...")
        
        # Générer graphe
        graph = generate_random_urban_graph(
            num_vertices=size,
            avg_degree=5,
            width=2000,
            height=2000
        )
        
        # Choisir source et cible aléatoires
        vertices = list(graph.vertices.keys())
        source = random.choice(vertices)
        target = random.choice([v for v in vertices if v != source])
        
        # Mesurer Dijkstra
        print("  • Test Dijkstra...", end=" ")
        perf_dijkstra = measure_algorithm_performance(
            dijkstra,
            graph,
            source,
            target,
            num_runs=num_runs
        )
        
        if perf_dijkstra["success"]:
            dijkstra_times.append(perf_dijkstra["time_ms"]["mean"])
            print(f"{perf_dijkstra['time_ms']['mean']:.2f} ms (moyenne)")
        else:
            dijkstra_times.append(0)
            print("ÉCHEC")
        
        # Mesurer A*
        print("  • Test A*...", end=" ")
        perf_astar = measure_algorithm_performance(
            astar,
            graph,
            source,
            target,
            num_runs=num_runs
        )
        
        if perf_astar["success"]:
            astar_times.append(perf_astar["time_ms"]["mean"])
            print(f"{perf_astar['time_ms']['mean']:.2f} ms (moyenne)")
        else:
            astar_times.append(0)
            print("ÉCHEC")
        
        # Calculer speedup
        speedup = (dijkstra_times[-1] / astar_times[-1]) if astar_times[-1] > 0 else 0
        
        # Stocker résultats
        results_data.append({
            "n_vertices": size,
            "m_edges": graph.num_edges_count(),
            "dijkstra_time_ms": dijkstra_times[-1],
            "astar_time_ms": astar_times[-1],
            "speedup": speedup,
            "dijkstra_visited": perf_dijkstra.get("visited_nodes", {}).get("mean", 0),
            "astar_visited": perf_astar.get("visited_nodes", {}).get("mean", 0)
        })
        
        print(f"  • Speedup : {speedup:.2f}x")
    
    # Afficher tableau récapitulatif
    print("\n" + "="*70)
    print(" RÉSULTATS RÉCAPITULATIFS")
    print("="*70)
    
    print(f"\n{'n':<8} {'m':<8} {'Dijkstra (ms)':<15} {'A* (ms)':<15} {'Speedup':<10}")
    print("-"*60)
    
    for data in results_data:
        print(f"{data['n_vertices']:<8} {data['m_edges']:<8} "
              f"{data['dijkstra_time_ms']:<15.2f} {data['astar_time_ms']:<15.2f} "
              f"{data['speedup']:<10.2f}x")
    
    print("-"*60)
    
    # Créer visualisation
    os.makedirs("figures", exist_ok=True)
    
    plot_performance_scaling(
        sizes=sizes,
        dijkstra_times=dijkstra_times,
        astar_times=astar_times,
        title="Analyse de Performance : Dijkstra vs A*",
        save_path="figures/exp_performance_scaling.png"
    )
    
    # Exporter résultats
    export_results_to_csv(results_data, "figures/performance_results.csv")
    
    # Analyse
    print("\n📊 ANALYSE :")
    
    # Complexité empirique (approximation)
    if len(sizes) >= 3:
        ratio_size = sizes[-1] / sizes[0]
        ratio_time_dijk = dijkstra_times[-1] / dijkstra_times[0] if dijkstra_times[0] > 0 else 0
        ratio_time_astar = astar_times[-1] / astar_times[0] if astar_times[0] > 0 else 0
        
        print(f"  • Taille du graphe : ×{ratio_size:.1f}")
        print(f"  • Temps Dijkstra   : ×{ratio_time_dijk:.1f}")
        print(f"  • Temps A*         : ×{ratio_time_astar:.1f}")
        print()
        print("  • Complexité empirique Dijkstra : O(n^{:.2f})".format(
            __log_ratio(ratio_time_dijk, ratio_size)
        ))
        print("  • Complexité empirique A*       : O(n^{:.2f})".format(
            __log_ratio(ratio_time_astar, ratio_size)
        ))
        print()
        print("  Note : Théoriquement O((n+m) log n) ≈ O(n log n) pour graphes peu denses")
    
    # Speedup moyen
    avg_speedup = sum(d['speedup'] for d in results_data) / len(results_data)
    print(f"\n  • Speedup moyen : {avg_speedup:.2f}x")
    print(f"  • A* est en moyenne {avg_speedup:.1f} fois plus rapide que Dijkstra")
    
    print("\n✓ Expérience terminée !")
    print("✓ Graphique sauvegardé : figures/exp_performance_scaling.png")
    print("✓ Données CSV : figures/performance_results.csv")


def __log_ratio(y_ratio, x_ratio):
    """Calcule l'exposant approximatif : y = x^k => k = log(y) / log(x)"""
    import math
    try:
        return math.log(y_ratio) / math.log(x_ratio)
    except (ValueError, ZeroDivisionError):
        return 0


if __name__ == "__main__":
    experiment_scaling()


