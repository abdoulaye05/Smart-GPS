"""
Module d'algorithmes de plus court chemin.

Implémente :
- Dijkstra : Algorithme classique du plus court chemin
- A* : Algorithme heuristique guidé par distance euclidienne

Complexité :
- Dijkstra : O((n + m) log n) avec tas binaire
- A* : O((n + m) log n) pire cas, souvent meilleur en pratique
"""

from typing import Dict, List, Tuple, Optional, Callable
import heapq
import math
import time
from .graph import Graph



class PathResult:
    """
    Classe encapsulant les résultats d'un algorithme de plus court chemin.
    
    Attributs:
        path: Liste des IDs de sommets formant le chemin
        cost: Coût total du chemin
        visited_nodes: Nombre de sommets visités
        explored_nodes: Ensemble des IDs de sommets explorés (pour visualisation)
        relaxed_edges: Nombre d'arêtes relaxées
        execution_time: Temps d'exécution (secondes)
        success: True si un chemin a été trouvé
    """
    
    def __init__(
        self,
        path: List[int] = None,
        cost: float = float('inf'),
        visited_nodes: int = 0,
        explored_nodes: Set[int] = None,
        relaxed_edges: int = 0,
        execution_time: float = 0.0,
        success: bool = False
    ):
        self.path = path or []
        self.cost = cost
        self.visited_nodes = visited_nodes
        self.explored_nodes = explored_nodes or set()
        self.relaxed_edges = relaxed_edges
        self.execution_time = execution_time
        self.success = execution_time >= 0 and success  # Petit fix pour garder success
    
    def __repr__(self) -> str:
        if self.success:
            return (f"PathResult(cost={self.cost:.2f}, "
                   f"length={len(self.path)}, "
                   f"visited={self.visited_nodes}, "
                   f"time={self.execution_time*1000:.2f}ms)")
        return "PathResult(no path found)"


def dijkstra(
    graph: Graph,
    source: int,
    target: int = None,
    return_stats: bool = True
) -> PathResult:
    """
    Algorithme de Dijkstra pour le plus court chemin.
    """
    start_time = time.perf_counter()
    
    # Vérifications
    if not graph.has_vertex(source):
        raise ValueError(f"Sommet source {source} n'existe pas")
    if target is not None and not graph.has_vertex(target):
        raise ValueError(f"Sommet cible {target} n'existe pas")
    
    # Cas trivial : source = cible
    if source == target:
        return PathResult(
            path=[source],
            cost=0.0,
            visited_nodes=1,
            explored_nodes={source},
            execution_time=time.perf_counter() - start_time,
            success=True
        )
    
    # Initialisation
    distances: Dict[int, float] = {v: float('inf') for v in graph.vertices}
    distances[source] = 0.0
    parents: Dict[int, Optional[int]] = {v: None for v in graph.vertices}
    
    # File de priorité : (distance, vertex_id)
    priority_queue = [(0.0, source)]
    visited: set = set()
    
    # Statistiques
    visited_count = 0
    relaxed_count = 0
    
    # Boucle principale
    while priority_queue:
        current_dist, current = heapq.heappop(priority_queue)
        
        # Si déjà visité, ignorer (duplicata dans la file)
        if current in visited:
            continue
        
        visited.add(current)
        visited_count += 1
        
        # Arrêt anticipé si cible atteinte
        if target is not None and current == target:
            break
        
        # Si distance obsolète, ignorer
        if current_dist > distances[current]:
            continue
        
        # Relaxation des arêtes
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            
            new_distance = distances[current] + weight
            relaxed_count += 1
            
            # Mise à jour si amélioration
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parents[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))
    
    execution_time = time.perf_counter() - start_time
    
    # Reconstruction du chemin si cible spécifiée
    if target is not None:
        if distances[target] == float('inf'):
            # Pas de chemin trouvé
            return PathResult(
                visited_nodes=visited_count,
                explored_nodes=visited,
                relaxed_edges=relaxed_count,
                execution_time=execution_time,
                success=False
            )
        
        # Reconstruction
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        
        return PathResult(
            path=path,
            cost=distances[target],
            visited_nodes=visited_count,
            explored_nodes=visited,
            relaxed_edges=relaxed_count,
            execution_time=execution_time,
            success=True
        )
    
    # Retour de toutes les distances (mode "single-source")
    return PathResult(
        visited_nodes=visited_count,
        explored_nodes=visited,
        relaxed_edges=relaxed_count,
        execution_time=execution_time,
        success=True
    )


def astar(
    graph: Graph,
    source: int,
    target: int,
    heuristic: Callable[[int, int, Graph], float] = None,
    return_stats: bool = True
) -> PathResult:
    """
    Algorithme A* (A-étoile) pour le plus court chemin.
    """
    start_time = time.perf_counter()
    
    # Vérifications
    if not graph.has_vertex(source):
        raise ValueError(f"Sommet source {source} n'existe pas")
    if not graph.has_vertex(target):
        raise ValueError(f"Sommet cible {target} n'existe pas")
    
    # Cas trivial
    if source == target:
        return PathResult(
            path=[source],
            cost=0.0,
            visited_nodes=1,
            explored_nodes={source},
            execution_time=time.perf_counter() - start_time,
            success=True
        )
    
    # Heuristique par défaut : adaptative
    if heuristic is None:
        def default_heuristic(v_id: int, t_id: int, g: Graph) -> float:
            """Heuristique adaptative (Euclidienne ou Haversine)."""
            v = g.vertices[v_id]
            t = g.vertices[t_id]
            metric = 'haversine' if getattr(g, 'is_geographic', False) else 'euclidean'
            return v.distance_to(t, metric=metric)
        heuristic = default_heuristic
    
    # Initialisation
    g_scores: Dict[int, float] = {v: float('inf') for v in graph.vertices}
    g_scores[source] = 0.0
    
    # f(v) = g(v) + h(v)
    h_source = heuristic(source, target, graph)
    f_scores: Dict[int, float] = {v: float('inf') for v in graph.vertices}
    f_scores[source] = h_source
    
    parents: Dict[int, Optional[int]] = {v: None for v in graph.vertices}
    
    # File de priorité OPEN : (f_score, vertex_id)
    open_set = [(f_scores[source], source)]
    open_set_members = {source}  # Pour vérification rapide
    
    # Ensemble CLOSED : sommets déjà explorés
    closed_set = set()
    
    # Statistiques
    visited_count = 0
    relaxed_count = 0
    
    # Boucle principale
    while open_set:
        # Extraire le sommet de f-score minimal
        current_f, current = heapq.heappop(open_set)
        open_set_members.discard(current)
        
        # Si déjà exploré, ignorer
        if current in closed_set:
            continue
        
        # Marquer comme visité
        closed_set.add(current)
        visited_count += 1
        
        # But atteint !
        if current == target:
            break
        
        # Si f-score obsolète, ignorer
        if current_f > f_scores[current]:
            continue
        
        # Explorer les voisins
        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            # Calculer g_score tentative
            tentative_g = g_scores[current] + weight
            relaxed_count += 1
            
            # Si amélioration
            if tentative_g < g_scores[neighbor]:
                # Mettre à jour le chemin
                parents[neighbor] = current
                g_scores[neighbor] = tentative_g
                
                # Calculer f_score
                h_neighbor = heuristic(neighbor, target, graph)
                f_scores[neighbor] = tentative_g + h_neighbor
                
                # Ajouter à OPEN (même si déjà présent, avec nouvelle priorité)
                heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                open_set_members.add(neighbor)
    
    execution_time = time.perf_counter() - start_time
    
    # Vérifier si un chemin a été trouvé
    if g_scores[target] == float('inf'):
        return PathResult(
            visited_nodes=visited_count,
            explored_nodes=closed_set,
            relaxed_edges=relaxed_count,
            execution_time=execution_time,
            success=False
        )
    
    # Reconstruction du chemin
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    
    return PathResult(
        path=path,
        cost=g_scores[target],
        visited_nodes=visited_count,
        explored_nodes=closed_set,
        relaxed_edges=relaxed_count,
        execution_time=execution_time,
        success=True
    )


def compare_algorithms(
    graph: Graph,
    source: int,
    target: int
) -> Dict[str, PathResult]:
    """
    Compare Dijkstra, A* et Bellman-Ford sur le même graphe.
    """
    results = {}
    
    # Dijkstra
    results['dijkstra'] = dijkstra(graph, source, target)
    
    # A*
    results['astar'] = astar(graph, source, target)
    
    # Bellman-Ford
    results['bellman_ford'] = bellman_ford(graph, source, target)
    
    return results


def bellman_ford(
    graph: Graph,
    source: int,
    target: int = None
) -> PathResult:
    """
    Algorithme de Bellman-Ford (bonus).
    """
    start_time = time.perf_counter()
    
    # Initialisation
    distances = {v: float('inf') for v in graph.vertices}
    distances[source] = 0.0
    parents = {v: None for v in graph.vertices}
    
    # Statistiques
    relaxed_count = 0
    visited_vertices = set([source])  # Source toujours visitée
    
    # Relaxation (n-1 fois)
    n = graph.num_vertices()
    for _ in range(n - 1):
        for edge in graph.get_all_edges():
            u, v, w = edge.source, edge.target, edge.weight
            relaxed_count += 1
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                parents[v] = u
                visited_vertices.add(v)
    
    # Détection de cycle négatif
    for edge in graph.get_all_edges():
        u, v, w = edge.source, edge.target, edge.weight
        if distances[u] + w < distances[v]:
            raise ValueError("Le graphe contient un cycle de poids négatif")
    
    execution_time = time.perf_counter() - start_time
    
    # Reconstruction si target spécifié
    if target is not None:
        if distances[target] == float('inf'):
            return PathResult(
                visited_nodes=len(visited_vertices),
                explored_nodes=visited_vertices,
                relaxed_edges=relaxed_count,
                execution_time=execution_time,
                success=False
            )
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        
        return PathResult(
            path=path,
            cost=distances[target],
            visited_nodes=len(visited_vertices),
            explored_nodes=visited_vertices,
            relaxed_edges=relaxed_count,
            execution_time=execution_time,
            success=True
        )
    
    return PathResult(
        visited_nodes=len(visited_vertices),
        explored_nodes=visited_vertices,
        relaxed_edges=relaxed_count,
        execution_time=execution_time,
        success=True
    )


