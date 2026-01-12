"""
Module de génération de graphes urbains.

Ce module fournit des fonctions pour créer différents types de graphes
représentatifs de réseaux urbains :
- Grilles régulières (Manhattan-like)
- Graphes aléatoires planaires
- Graphes réalistes avec clusters
"""

import random
import math
from typing import List, Tuple
from .graph import Graph


def generate_grid_graph(
    rows: int,
    cols: int,
    spacing: float = 1.0,
    add_diagonals: bool = False,
    noise: float = 0.0
) -> Graph:
    """
    Génère un graphe en grille régulière (type Manhattan).
    
    Structure :
        - Sommets organisés en grille rows × cols
        - Connexions horizontales et verticales
        - Option : connexions diagonales
        - Option : bruit sur les positions
    
    Args:
        rows: Nombre de lignes
        cols: Nombre de colonnes
        spacing: Espacement entre sommets adjacents
        add_diagonals: Si True, ajoute les arêtes diagonales
        noise: Facteur de bruit (0 = régulier, 1 = aléatoire)
        
    Returns:
        Graph avec structure en grille
        
    Example:
        >>> g = generate_grid_graph(10, 10, spacing=100)
        >>> print(g.summary())
    """
    graph = Graph(directed=False)
    
    # Créer les sommets avec positions
    vertex_map = {}  # (row, col) -> vertex_id
    vertex_id = 0
    
    for row in range(rows):
        for col in range(cols):
            # Position de base
            x = col * spacing
            y = row * spacing
            
            # Ajouter du bruit aléatoire si demandé
            if noise > 0:
                x += random.uniform(-noise * spacing / 2, noise * spacing / 2)
                y += random.uniform(-noise * spacing / 2, noise * spacing / 2)
            
            vertex = graph.add_vertex(vertex_id, x, y, label=f"({row},{col})")
            vertex_map[(row, col)] = vertex_id
            vertex_id += 1
    
    # Créer les arêtes
    for row in range(rows):
        for col in range(cols):
            current_id = vertex_map[(row, col)]
            
            # Arête vers la droite
            if col < cols - 1:
                right_id = vertex_map[(row, col + 1)]
                graph.add_edge(current_id, right_id)
            
            # Arête vers le bas
            if row < rows - 1:
                down_id = vertex_map[(row + 1, col)]
                graph.add_edge(current_id, down_id)
            
            # Arêtes diagonales (optionnel)
            if add_diagonals:
                # Diagonale bas-droite
                if row < rows - 1 and col < cols - 1:
                    diag_rd = vertex_map[(row + 1, col + 1)]
                    graph.add_edge(current_id, diag_rd)
                
                # Diagonale bas-gauche
                if row < rows - 1 and col > 0:
                    diag_ld = vertex_map[(row + 1, col - 1)]
                    graph.add_edge(current_id, diag_ld)
    
    return graph


def generate_random_urban_graph(
    num_vertices: int,
    avg_degree: float = 4.0,
    width: float = 1000.0,
    height: float = 1000.0,
    min_distance: float = 50.0,
    connect_nearest: bool = True
) -> Graph:
    """
    Génère un graphe urbain aléatoire planaire.
    
    Algorithme :
        1. Placer num_vertices sommets aléatoirement (avec distance minimale)
        2. Connecter chaque sommet à ses k plus proches voisins
        3. Assurer la connexité du graphe
        
    Args:
        num_vertices: Nombre de sommets
        avg_degree: Degré moyen souhaité
        width: Largeur de la zone (en unités)
        height: Hauteur de la zone
        min_distance: Distance minimale entre sommets
        connect_nearest: Si True, connecte aux plus proches voisins
        
    Returns:
        Graph avec structure réaliste
    """
    graph = Graph(directed=False)
    
    # Générer positions avec distance minimale
    positions = []
    attempts = 0
    max_attempts = num_vertices * 100
    
    while len(positions) < num_vertices and attempts < max_attempts:
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        
        # Vérifier distance minimale
        valid = True
        for px, py in positions:
            dist = math.sqrt((x - px)**2 + (y - py)**2)
            if dist < min_distance:
                valid = False
                break
        
        if valid:
            positions.append((x, y))
        
        attempts += 1
    
    # Si pas assez de positions trouvées, relâcher la contrainte
    while len(positions) < num_vertices:
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        positions.append((x, y))
    
    # Créer les sommets
    for i, (x, y) in enumerate(positions):
        graph.add_vertex(i, x, y, label=f"V{i}")
    
    # Stratégie de connexion
    if connect_nearest:
        # Connecter chaque sommet à ses k plus proches voisins
        k = max(2, int(avg_degree))
        
        for i in range(num_vertices):
            # Calculer distances à tous les autres sommets
            distances = []
            for j in range(num_vertices):
                if i != j:
                    dist = math.sqrt(
                        (positions[i][0] - positions[j][0])**2 +
                        (positions[i][1] - positions[j][1])**2
                    )
                    distances.append((dist, j))
            
            # Trier par distance et connecter aux k plus proches
            distances.sort()
            for _, neighbor in distances[:k]:
                if not graph.has_edge(i, neighbor):
                    graph.add_edge(i, neighbor)
    else:
        # Connexion aléatoire avec probabilité
        target_edges = int(num_vertices * avg_degree / 2)
        edges_added = 0
        
        while edges_added < target_edges:
            i = random.randint(0, num_vertices - 1)
            j = random.randint(0, num_vertices - 1)
            
            if i != j and not graph.has_edge(i, j):
                graph.add_edge(i, j)
                edges_added += 1
    
    # Assurer la connexité (ajouter des arêtes si nécessaire)
    if not graph.is_connected():
        _ensure_connectivity(graph)
    
    return graph


def generate_clustered_urban_graph(
    num_clusters: int,
    vertices_per_cluster: int,
    cluster_radius: float = 200.0,
    world_size: float = 2000.0,
    inter_cluster_connections: int = 3
) -> Graph:
    """
    Génère un graphe avec structure en clusters (quartiers).
    
    Simule une ville avec plusieurs quartiers densément connectés
    et quelques routes principales entre quartiers.
    
    Args:
        num_clusters: Nombre de clusters (quartiers)
        vertices_per_cluster: Sommets par cluster
        cluster_radius: Rayon de chaque cluster
        world_size: Taille de la zone totale
        inter_cluster_connections: Nombre de connexions entre clusters
        
    Returns:
        Graph avec structure clustérisée
    """
    graph = Graph(directed=False)
    
    # Positionner les centres de clusters
    cluster_centers = []
    for _ in range(num_clusters):
        cx = random.uniform(cluster_radius, world_size - cluster_radius)
        cy = random.uniform(cluster_radius, world_size - cluster_radius)
        cluster_centers.append((cx, cy))
    
    # Générer sommets dans chaque cluster
    vertex_id = 0
    cluster_vertices = []  # Liste des sommets par cluster
    
    for cluster_idx, (cx, cy) in enumerate(cluster_centers):
        vertices_in_cluster = []
        
        for _ in range(vertices_per_cluster):
            # Position autour du centre (distribution gaussienne)
            angle = random.uniform(0, 2 * math.pi)
            radius = random.gauss(cluster_radius / 2, cluster_radius / 4)
            radius = max(0, min(radius, cluster_radius))
            
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            graph.add_vertex(vertex_id, x, y, label=f"C{cluster_idx}_V{vertex_id}")
            vertices_in_cluster.append(vertex_id)
            vertex_id += 1
        
        cluster_vertices.append(vertices_in_cluster)
    
    # Connecter sommets à l'intérieur de chaque cluster
    for vertices in cluster_vertices:
        for i, v1 in enumerate(vertices):
            # Connecter aux 3-4 plus proches voisins dans le cluster
            neighbors = []
            for v2 in vertices:
                if v1 != v2:
                    dist = graph.vertices[v1].distance_to(graph.vertices[v2])
                    neighbors.append((dist, v2))
            
            neighbors.sort()
            k = min(4, len(neighbors))
            for _, v2 in neighbors[:k]:
                if not graph.has_edge(v1, v2):
                    graph.add_edge(v1, v2)
    
    # Connecter les clusters entre eux (routes principales)
    for _ in range(inter_cluster_connections * num_clusters):
        c1 = random.randint(0, num_clusters - 1)
        c2 = random.randint(0, num_clusters - 1)
        
        if c1 != c2:
            # Choisir un sommet aléatoire de chaque cluster
            v1 = random.choice(cluster_vertices[c1])
            v2 = random.choice(cluster_vertices[c2])
            
            if not graph.has_edge(v1, v2):
                # Arête "autoroute" entre clusters (poids peut être modifié)
                graph.add_edge(v1, v2)
    
    # Assurer connexité
    if not graph.is_connected():
        _ensure_connectivity(graph)
    
    return graph


def add_traffic_congestion(
    graph: Graph,
    congestion_factor: float = 2.0,
    affected_ratio: float = 0.3
) -> None:
    """
    Ajoute de la congestion (trafic) à certaines arêtes du graphe.
    
    Modifie les poids des arêtes pour simuler du trafic dense.
    
    Args:
        graph: Le graphe à modifier (modification in-place)
        congestion_factor: Facteur multiplicatif du poids (> 1)
        affected_ratio: Proportion d'arêtes affectées (0 à 1)
    """
    all_edges = graph.get_all_edges()
    num_affected = int(len(all_edges) * affected_ratio)
    
    # Sélectionner aléatoirement des arêtes
    affected_edges = random.sample(all_edges, num_affected)
    
    for edge in affected_edges:
        edge.weight *= congestion_factor


def _ensure_connectivity(graph: Graph) -> None:
    """
    Assure qu'un graphe est connexe en ajoutant des arêtes si nécessaire.
    
    Utilise un parcours BFS pour identifier les composantes connexes,
    puis connecte les composantes entre elles.
    
    Args:
        graph: Le graphe à rendre connexe (modification in-place)
    """
    if graph.num_vertices() == 0:
        return
    
    # Identifier les composantes connexes
    visited = set()
    components = []
    
    for start in graph.vertices:
        if start not in visited:
            component = set()
            queue = [start]
            component.add(start)
            visited.add(start)
            
            while queue:
                current = queue.pop(0)
                for neighbor, _ in graph.get_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        component.add(neighbor)
                        queue.append(neighbor)
            
            components.append(list(component))
    
    # Connecter les composantes
    for i in range(len(components) - 1):
        # Trouver les deux sommets les plus proches entre composantes i et i+1
        min_dist = float('inf')
        best_pair = None
        
        for v1 in components[i]:
            for v2 in components[i + 1]:
                dist = graph.vertices[v1].distance_to(graph.vertices[v2])
                if dist < min_dist:
                    min_dist = dist
                    best_pair = (v1, v2)
        
        # Ajouter l'arête
        if best_pair:
            graph.add_edge(best_pair[0], best_pair[1])


def generate_realistic_city(
    size: str = "medium"
) -> Graph:
    """
    Génère un graphe urbain réaliste en fonction d'une taille prédéfinie.
    
    Args:
        size: Taille de la ville ("small", "medium", "large")
        
    Returns:
        Graph représentant une ville
    """
    sizes = {
        "small": {
            "num_clusters": 3,
            "vertices_per_cluster": 20,
            "cluster_radius": 150,
            "world_size": 1000
        },
        "medium": {
            "num_clusters": 5,
            "vertices_per_cluster": 40,
            "cluster_radius": 200,
            "world_size": 2000
        },
        "large": {
            "num_clusters": 10,
            "vertices_per_cluster": 100,
            "cluster_radius": 250,
            "world_size": 5000
        }
    }
    
    params = sizes.get(size, sizes["medium"])
    
    return generate_clustered_urban_graph(
        num_clusters=params["num_clusters"],
        vertices_per_cluster=params["vertices_per_cluster"],
        cluster_radius=params["cluster_radius"],
        world_size=params["world_size"]
    )


