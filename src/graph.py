"""
Module de gestion des graphes pour la modélisation de réseaux urbains.

Ce module définit les structures de données pour représenter un graphe pondéré :
- Vertex : Représente un sommet (intersection)
- Edge : Représente une arête (route)
- Graph : Structure complète du graphe avec ses opérations
"""

from typing import Dict, List, Tuple, Optional, Set
import math


class Vertex:
    """
    Classe représentant un sommet du graphe (intersection).
    
    Attributs:
        id (int): Identifiant unique du sommet
        x (float): Coordonnée x (longitude)
        y (float): Coordonnée y (latitude)
        label (str): Nom optionnel du sommet
    """
    
    def __init__(self, id: int, x: float = 0.0, y: float = 0.0, label: str = ""):
        self.id = id
        self.x = x
        self.y = y
        self.label = label or f"V{id}"
    
    def distance_to(self, other: 'Vertex') -> float:
        """
        Calcule la distance euclidienne vers un autre sommet.
        
        Args:
            other: Autre sommet
            
        Returns:
            Distance euclidienne (en unités du plan)
        """
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Vertex({self.id}, pos=({self.x:.2f}, {self.y:.2f}))"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Vertex) and self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)


class Edge:
    """
    Classe représentant une arête du graphe (route).
    
    Attributs:
        source (int): ID du sommet source
        target (int): ID du sommet cible
        weight (float): Poids de l'arête (distance, temps, etc.)
        road_type (str): Type de route ('highway', 'main', 'residential')
        speed_limit (float): Vitesse limite (km/h)
    """
    
    def __init__(
        self, 
        source: int, 
        target: int, 
        weight: float,
        road_type: str = "main",
        speed_limit: float = 50.0
    ):
        self.source = source
        self.target = target
        self.weight = weight
        self.road_type = road_type
        self.speed_limit = speed_limit
    
    def __repr__(self) -> str:
        return f"Edge({self.source} -> {self.target}, w={self.weight:.2f})"


class Graph:
    """
    Classe représentant un graphe orienté pondéré.
    
    Modélisation : G = (V, E, w)
    - V : ensemble des sommets (Vertex)
    - E : ensemble des arêtes (Edge)
    - w : fonction de pondération (weight)
    
    Implémentation : Liste d'adjacence pour efficacité O(n + m)
    """
    
    def __init__(self, directed: bool = True):
        """
        Initialise un graphe vide.
        
        Args:
            directed: Si True, graphe orienté ; si False, graphe non-orienté
        """
        self.vertices: Dict[int, Vertex] = {}
        self.adjacency_list: Dict[int, List[Tuple[int, float, Edge]]] = {}
        self.directed = directed
        self.num_edges = 0
    
    def add_vertex(self, vertex_id: int, x: float = 0.0, y: float = 0.0, label: str = "") -> Vertex:
        """
        Ajoute un sommet au graphe.
        
        Args:
            vertex_id: Identifiant unique
            x: Coordonnée x
            y: Coordonnée y
            label: Label optionnel
            
        Returns:
            Le sommet créé
        """
        if vertex_id not in self.vertices:
            vertex = Vertex(vertex_id, x, y, label)
            self.vertices[vertex_id] = vertex
            self.adjacency_list[vertex_id] = []
            return vertex
        return self.vertices[vertex_id]
    
    def add_edge(
        self, 
        source: int, 
        target: int, 
        weight: float = None,
        road_type: str = "main",
        speed_limit: float = 50.0
    ) -> None:
        """
        Ajoute une arête au graphe.
        
        Args:
            source: ID du sommet source
            target: ID du sommet cible
            weight: Poids (si None, calculé par distance euclidienne)
            road_type: Type de route
            speed_limit: Vitesse limite
            
        Note:
            Si le graphe est non-orienté, ajoute aussi l'arête inverse.
        """
        # Créer les sommets s'ils n'existent pas
        if source not in self.vertices:
            self.add_vertex(source)
        if target not in self.vertices:
            self.add_vertex(target)
        
        # Calculer le poids si non spécifié (distance euclidienne)
        if weight is None:
            v_source = self.vertices[source]
            v_target = self.vertices[target]
            weight = v_source.distance_to(v_target)
        
        # Créer l'arête
        edge = Edge(source, target, weight, road_type, speed_limit)
        self.adjacency_list[source].append((target, weight, edge))
        self.num_edges += 1
        
        # Si non-orienté, ajouter l'arête inverse
        if not self.directed:
            edge_reverse = Edge(target, source, weight, road_type, speed_limit)
            self.adjacency_list[target].append((source, weight, edge_reverse))
    
    def get_neighbors(self, vertex_id: int) -> List[Tuple[int, float]]:
        """
        Retourne les voisins d'un sommet avec leurs poids.
        
        Args:
            vertex_id: ID du sommet
            
        Returns:
            Liste de tuples (voisin_id, poids)
        """
        return [(neighbor, weight) for neighbor, weight, _ in self.adjacency_list.get(vertex_id, [])]
    
    def get_edge(self, source: int, target: int) -> Optional[Edge]:
        """
        Récupère l'arête entre deux sommets.
        
        Args:
            source: ID du sommet source
            target: ID du sommet cible
            
        Returns:
            L'arête si elle existe, None sinon
        """
        for neighbor, _, edge in self.adjacency_list.get(source, []):
            if neighbor == target:
                return edge
        return None
    
    def get_weight(self, source: int, target: int) -> Optional[float]:
        """
        Récupère le poids de l'arête entre deux sommets.
        
        Args:
            source: ID du sommet source
            target: ID du sommet cible
            
        Returns:
            Le poids si l'arête existe, None sinon
        """
        edge = self.get_edge(source, target)
        return edge.weight if edge else None
    
    def has_vertex(self, vertex_id: int) -> bool:
        """Vérifie si un sommet existe."""
        return vertex_id in self.vertices
    
    def has_edge(self, source: int, target: int) -> bool:
        """Vérifie si une arête existe."""
        return self.get_edge(source, target) is not None
    
    def get_all_vertices(self) -> List[Vertex]:
        """Retourne la liste de tous les sommets."""
        return list(self.vertices.values())
    
    def get_all_edges(self) -> List[Edge]:
        """Retourne la liste de toutes les arêtes."""
        edges = []
        for vertex_id in self.adjacency_list:
            for _, _, edge in self.adjacency_list[vertex_id]:
                edges.append(edge)
        return edges
    
    def num_vertices(self) -> int:
        """Retourne le nombre de sommets."""
        return len(self.vertices)
    
    def num_edges_count(self) -> int:
        """Retourne le nombre d'arêtes."""
        return self.num_edges
    
    def degree(self, vertex_id: int) -> int:
        """
        Retourne le degré d'un sommet (nombre de voisins).
        
        Args:
            vertex_id: ID du sommet
            
        Returns:
            Degré du sommet
        """
        return len(self.adjacency_list.get(vertex_id, []))
    
    def average_degree(self) -> float:
        """Retourne le degré moyen du graphe."""
        if self.num_vertices() == 0:
            return 0.0
        total_degree = sum(self.degree(v) for v in self.vertices)
        return total_degree / self.num_vertices()
    
    def is_connected(self) -> bool:
        """
        Vérifie si le graphe est connexe (parcours BFS).
        
        Returns:
            True si connexe, False sinon
        """
        if not self.vertices:
            return True
        
        start = next(iter(self.vertices))
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            current = queue.pop(0)
            for neighbor, _ in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == self.num_vertices()
    
    def __repr__(self) -> str:
        return (f"Graph(vertices={self.num_vertices()}, "
                f"edges={self.num_edges_count()}, "
                f"directed={self.directed})")
    
    def summary(self) -> str:
        """
        Retourne un résumé détaillé du graphe.
        
        Returns:
            Chaîne de caractères avec statistiques
        """
        return f"""
Graphe : {'Orienté' if self.directed else 'Non-orienté'}
----------------------------------------
Nombre de sommets (n) : {self.num_vertices()}
Nombre d'arêtes (m)   : {self.num_edges_count()}
Degré moyen           : {self.average_degree():.2f}
Densité               : {2 * self.num_edges_count() / (self.num_vertices() * (self.num_vertices() - 1)):.4f}
Connexe               : {'Oui' if self.is_connected() else 'Non'}
        """.strip()

