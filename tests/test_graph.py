"""
Tests unitaires pour le module graph.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.graph import Graph, Vertex, Edge


class TestVertex:
    """Tests pour la classe Vertex."""
    
    def test_creation(self):
        """Test de création d'un sommet."""
        v = Vertex(0, 10.0, 20.0, "A")
        assert v.id == 0
        assert v.x == 10.0
        assert v.y == 20.0
        assert v.label == "A"
    
    def test_distance(self):
        """Test de calcul de distance euclidienne."""
        v1 = Vertex(0, 0.0, 0.0)
        v2 = Vertex(1, 3.0, 4.0)
        
        dist = v1.distance_to(v2)
        assert abs(dist - 5.0) < 1e-6  # 3-4-5 triangle
    
    def test_equality(self):
        """Test d'égalité de sommets."""
        v1 = Vertex(0, 0.0, 0.0)
        v2 = Vertex(0, 10.0, 10.0)
        v3 = Vertex(1, 0.0, 0.0)
        
        assert v1 == v2  # Même ID
        assert v1 != v3  # IDs différents


class TestGraph:
    """Tests pour la classe Graph."""
    
    def test_empty_graph(self):
        """Test de création d'un graphe vide."""
        g = Graph()
        assert g.num_vertices() == 0
        assert g.num_edges_count() == 0
    
    def test_add_vertex(self):
        """Test d'ajout de sommets."""
        g = Graph()
        v1 = g.add_vertex(0, 0.0, 0.0)
        v2 = g.add_vertex(1, 10.0, 10.0)
        
        assert g.num_vertices() == 2
        assert g.has_vertex(0)
        assert g.has_vertex(1)
        assert not g.has_vertex(2)
    
    def test_add_edge(self):
        """Test d'ajout d'arêtes."""
        g = Graph()
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 3.0, 4.0)
        g.add_edge(0, 1, weight=5.0)
        
        assert g.has_edge(0, 1)
        assert g.get_weight(0, 1) == 5.0
    
    def test_add_edge_auto_weight(self):
        """Test d'ajout d'arête avec poids automatique."""
        g = Graph()
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 3.0, 4.0)
        g.add_edge(0, 1)  # Poids calculé automatiquement
        
        weight = g.get_weight(0, 1)
        assert abs(weight - 5.0) < 1e-6
    
    def test_undirected_graph(self):
        """Test de graphe non-orienté."""
        g = Graph(directed=False)
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_edge(0, 1, weight=10.0)
        
        # Les deux directions doivent exister
        assert g.has_edge(0, 1)
        assert g.has_edge(1, 0)
    
    def test_directed_graph(self):
        """Test de graphe orienté."""
        g = Graph(directed=True)
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_edge(0, 1, weight=10.0)
        
        # Seulement une direction
        assert g.has_edge(0, 1)
        assert not g.has_edge(1, 0)
    
    def test_neighbors(self):
        """Test de récupération des voisins."""
        g = Graph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_edge(0, 1, weight=5.0)
        g.add_edge(0, 2, weight=10.0)
        
        neighbors = g.get_neighbors(0)
        assert len(neighbors) == 2
        assert (1, 5.0) in neighbors
        assert (2, 10.0) in neighbors
    
    def test_degree(self):
        """Test de calcul du degré."""
        g = Graph(directed=False)
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        
        assert g.degree(0) == 2
        assert g.degree(1) == 1
        assert g.degree(2) == 1
    
    def test_is_connected(self):
        """Test de vérification de connexité."""
        # Graphe connexe
        g1 = Graph(directed=False)
        g1.add_vertex(0)
        g1.add_vertex(1)
        g1.add_vertex(2)
        g1.add_edge(0, 1)
        g1.add_edge(1, 2)
        assert g1.is_connected()
        
        # Graphe non-connexe
        g2 = Graph(directed=False)
        g2.add_vertex(0)
        g2.add_vertex(1)
        g2.add_vertex(2)
        g2.add_edge(0, 1)
        # 2 est isolé
        assert not g2.is_connected()


class TestGraphScenarios:
    """Tests de scénarios réalistes."""
    
    def test_triangle(self):
        """Test sur un graphe triangle."""
        g = Graph(directed=False)
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 1.0, 0.0)
        g.add_vertex(2, 0.5, 0.866)  # Triangle équilatéral approximatif
        
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        
        assert g.num_vertices() == 3
        assert g.num_edges_count() == 3
        assert g.is_connected()
        assert g.average_degree() == 2.0
    
    def test_path_graph(self):
        """Test sur un graphe en chemin."""
        g = Graph(directed=False)
        n = 5
        
        for i in range(n):
            g.add_vertex(i, float(i), 0.0)
        
        for i in range(n - 1):
            g.add_edge(i, i + 1)
        
        assert g.num_vertices() == n
        assert g.num_edges_count() == n - 1
        assert g.is_connected()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


