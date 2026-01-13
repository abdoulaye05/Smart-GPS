"""
Module utilitaire pour le projet.

Contient des fonctions auxiliaires pour :
- Mesure de performance
- Export de résultats
- Statistiques
"""

import time
import json
import csv
from typing import Dict, List, Any, Callable
from functools import wraps
from .graph import Graph
from .algorithms import PathResult


def timeit(func: Callable) -> Callable:
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction.
    
    Usage:
        @timeit
        def ma_fonction():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️  {func.__name__} : {(end - start) * 1000:.2f} ms")
        return result
    return wrapper


def measure_algorithm_performance(
    algorithm: Callable,
    graph: Graph,
    source: int,
    target: int,
    num_runs: int = 10
) -> Dict[str, Any]:
    """
    Mesure les performances d'un algorithme sur plusieurs exécutions.
    
    Args:
        algorithm: Fonction d'algorithme (dijkstra ou astar)
        graph: Le graphe
        source: Sommet source
        target: Sommet cible
        num_runs: Nombre d'exécutions
        
    Returns:
        Dictionnaire avec statistiques (moyenne, min, max, écart-type)
    """
    times = []
    visited_nodes = []
    relaxed_edges = []
    costs = []
    
    for _ in range(num_runs):
        result = algorithm(graph, source, target)
        
        if result.success:
            times.append(result.execution_time * 1000)  # en ms
            visited_nodes.append(result.visited_nodes)
            relaxed_edges.append(result.relaxed_edges)
            costs.append(result.cost)
    
    if not times:
        return {"success": False}
    
    import statistics
    
    return {
        "success": True,
        "num_runs": num_runs,
        "time_ms": {
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "min": min(times),
            "max": max(times)
        },
        "visited_nodes": {
            "mean": statistics.mean(visited_nodes),
            "min": min(visited_nodes),
            "max": max(visited_nodes)
        },
        "relaxed_edges": {
            "mean": statistics.mean(relaxed_edges),
            "min": min(relaxed_edges),
            "max": max(relaxed_edges)
        },
        "cost": {
            "mean": statistics.mean(costs),
            "stdev": statistics.stdev(costs) if len(costs) > 1 else 0
        }
    }


def export_results_to_json(
    results: Dict[str, Any],
    filename: str
) -> None:
    """
    Exporte des résultats au format JSON.
    
    Args:
        results: Dictionnaire de résultats
        filename: Nom du fichier de sortie
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✓ Résultats exportés : {filename}")


def export_results_to_csv(
    data: List[Dict[str, Any]],
    filename: str
) -> None:
    """
    Exporte des résultats au format CSV.
    
    Args:
        data: Liste de dictionnaires
        filename: Nom du fichier de sortie
    """
    if not data:
        print("⚠️  Aucune donnée à exporter")
        return
    
    keys = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ Résultats exportés : {filename}")


def print_path_result(
    result: PathResult,
    algorithm_name: str = "Algorithme"
) -> None:
    """
    Affiche joliment les résultats d'un algorithme.
    
    Args:
        result: Résultat de l'algorithme
        algorithm_name: Nom de l'algorithme
    """
    print(f"\n{'='*60}")
    print(f"  {algorithm_name}")
    print(f"{'='*60}")
    
    if result.success:
        print(f"✓ Chemin trouvé !")
        print(f"  • Coût total         : {result.cost:.2f}")
        print(f"  • Longueur du chemin : {len(result.path)} sommets")
        print(f"  • Sommets visités    : {result.visited_nodes}")
        print(f"  • Exploration        : {result.visited_nodes / graph.num_vertices() * 100:.1f}% du graphe")
        print(f"  • Arêtes relaxées    : {result.relaxed_edges}")
        print(f"  • Temps d'exécution  : {result.execution_time * 1000:.2f} ms")
        
        if len(result.path) <= 20:
            print(f"  • Chemin             : {' → '.join(map(str, result.path))}")
    else:
        print("✗ Aucun chemin trouvé")
        print(f"  • Sommets visités    : {result.visited_nodes}")
        print(f"  • Temps d'exécution  : {result.execution_time * 1000:.2f} ms")
    
    print(f"{'='*60}\n")


def compare_and_print(
    results: Dict[str, PathResult],
    graph: Graph
) -> None:
    """
    Compare et affiche les résultats de plusieurs algorithmes.
    
    Args:
        results: Dictionnaire {nom_algo: PathResult}
        graph: Le graphe utilisé
    """
    print(f"\n{'#'*60}")
    print(f"  COMPARAISON DES ALGORITHMES")
    print(f"{'#'*60}")
    print(f"Graphe : {graph.num_vertices()} sommets, {graph.num_edges_count()} arêtes\n")
    
    # Tableau comparatif
    print(f"{'Algorithme':<15} {'Coût':<10} {'Sommets':<10} {'% Expl.':<10} {'Temps (ms)':<12} {'Speedup':<10}")
    print(f"{'-'*70}")
    
    base_time = None
    
    for name, result in results.items():
        if result.success:
            time_ms = result.execution_time * 1000
            expl_pct = f"{result.visited_nodes / graph.num_vertices() * 100:.1f}%"
            
            if base_time is None:
                base_time = time_ms
                speedup = "1.00x (ref)"
            else:
                speedup = f"{base_time / time_ms:.2f}x" if time_ms > 0 else "N/A"
            
            print(f"{name:<15} {result.cost:<10.2f} {result.visited_nodes:<10} {expl_pct:<10} "
                  f"{time_ms:<12.2f} {speedup:<10}")
        else:
            print(f"{name:<15} {'N/A':<10} {result.visited_nodes:<10} {'N/A':<10} "
                  f"{result.execution_time * 1000:<12.2f} {'N/A':<10}")
    
    print(f"{'-'*70}\n")
    
    # Analyse
    if len(results) >= 2:
        algos = list(results.keys())
        
        # Vérifier que tous les algorithmes ont réussi
        all_success = all(results[algo].success for algo in algos)
        
        if all_success:
            print("📊 Analyse :")
            
            # Comparaison A* vs Dijkstra
            if 'astar' in results and 'dijkstra' in results:
                r_dijk = results['dijkstra']
                r_astar = results['astar']
                # Protection contre division par zéro
                if r_dijk.visited_nodes > 0:
                    reduction = (1 - r_astar.visited_nodes / r_dijk.visited_nodes) * 100
                else:
                    reduction = 0.0
                if r_dijk.execution_time > 0:
                    gain = (1 - r_astar.execution_time / r_dijk.execution_time) * 100
                else:
                    gain = 0.0
                print(f"  • A* vs Dijkstra :")
                print(f"    - Réduction de sommets visités : {reduction:.1f}%")
                print(f"    - Gain de temps : {gain:.1f}%")
            
            # Comparaison Bellman-Ford vs Dijkstra
            if 'bellman_ford' in results and 'dijkstra' in results:
                r_dijk = results['dijkstra']
                r_bf = results['bellman_ford']
                ratio = r_bf.execution_time / r_dijk.execution_time if r_dijk.execution_time > 0 else float('inf')
                print(f"  • Bellman-Ford vs Dijkstra :")
                print(f"    - Ratio de temps : {ratio:.1f}× plus lent")
            
            # Vérifier cohérence des coûts
            costs = [results[algo].cost for algo in algos if results[algo].success]
            if len(costs) >= 2:
                all_equal = all(abs(costs[0] - c) < 0.01 for c in costs)
                if all_equal:
                    print(f"  • Tous les algorithmes trouvent le même chemin optimal ✓")
                else:
                    print(f"  • ⚠️  Les coûts diffèrent légèrement (arrondi numérique)")
    
    print(f"{'#'*60}\n")


def calculate_speedup(
    time_baseline: float,
    time_optimized: float
) -> float:
    """
    Calcule le facteur d'accélération (speedup).
    
    Args:
        time_baseline: Temps de référence
        time_optimized: Temps optimisé
        
    Returns:
        Facteur d'accélération
    """
    if time_optimized == 0:
        return float('inf')
    return time_baseline / time_optimized


def effective_branching_factor(
    nodes_expanded: int,
    solution_depth: int
) -> float:
    """
    Calcule le facteur de branchement effectif b*.
    
    Formule : N = 1 + b* + (b*)^2 + ... + (b*)^d
    
    Args:
        nodes_expanded: Nombre de nœuds explorés
        solution_depth: Profondeur de la solution
        
    Returns:
        Facteur de branchement effectif
    """
    if solution_depth == 0:
        return 1.0
    
    # Approximation : N ≈ (b*^(d+1) - 1) / (b* - 1)
    # Résolution numérique simple
    b_star = 1.0
    for _ in range(100):  # Itérations
        numerator = b_star ** (solution_depth + 1) - 1
        denominator = b_star - 1
        
        if abs(denominator) < 1e-10:
            break
        
        estimated = numerator / denominator
        
        if abs(estimated - nodes_expanded) < 1:
            break
        
        # Ajustement
        if estimated < nodes_expanded:
            b_star += 0.01
        else:
            b_star -= 0.01
        
        if b_star <= 1.0:
            b_star = 1.01
    
    return b_star


def generate_report_summary(
    graph: Graph,
    results: Dict[str, PathResult]
) -> str:
    """
    Génère un résumé textuel des résultats.
    
    Args:
        graph: Le graphe
        results: Résultats des algorithmes
        
    Returns:
        Chaîne de caractères avec le résumé
    """
    report = []
    report.append("="*70)
    report.append(" RAPPORT DE SIMULATION - GPS INTELLIGENT")
    report.append("="*70)
    report.append("")
    report.append(f"Graphe analysé :")
    report.append(f"  • Sommets (n) : {graph.num_vertices()}")
    report.append(f"  • Arêtes (m)  : {graph.num_edges_count()}")
    report.append(f"  • Degré moyen : {graph.average_degree():.2f}")
    report.append(f"  • Connexe     : {'Oui' if graph.is_connected() else 'Non'}")
    report.append("")
    report.append("Résultats des algorithmes :")
    report.append("-"*70)
    
    for name, result in results.items():
        report.append(f"\n{name.upper()} :")
        if result.success:
            report.append(f"  ✓ Chemin trouvé")
            report.append(f"    - Coût               : {result.cost:.2f}")
            report.append(f"    - Longueur           : {len(result.path)} sommets")
            report.append(f"    - Sommets visités    : {result.visited_nodes}")
            report.append(f"    - Arêtes relaxées    : {result.relaxed_edges}")
            report.append(f"    - Temps              : {result.execution_time * 1000:.2f} ms")
            report.append(f"    - Exploration        : {result.visited_nodes / graph.num_vertices() * 100:.1f}% du graphe")
        else:
            report.append(f"  ✗ Aucun chemin trouvé")
    
    report.append("")
    report.append("="*70)
    
    return "\n".join(report)


def save_graph_to_file(
    graph: Graph,
    filename: str,
    format: str = "json"
) -> None:
    """
    Sauvegarde un graphe dans un fichier.
    
    Args:
        graph: Le graphe à sauvegarder
        filename: Nom du fichier
        format: Format ('json' ou 'edgelist')
    """
    if format == "json":
        data = {
            "vertices": [
                {"id": v.id, "x": v.x, "y": v.y, "label": v.label}
                for v in graph.vertices.values()
            ],
            "edges": [
                {"source": e.source, "target": e.target, "weight": e.weight}
                for e in graph.get_all_edges()
            ],
            "directed": graph.directed
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    elif format == "edgelist":
        with open(filename, 'w') as f:
            for edge in graph.get_all_edges():
                f.write(f"{edge.source} {edge.target} {edge.weight}\n")
    
    print(f"✓ Graphe sauvegardé : {filename}")

