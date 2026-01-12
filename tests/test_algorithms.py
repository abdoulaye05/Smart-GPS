"""
Tests unitaires pour le module algorithms.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.graph import Graph
from src.algorithms import dijkstra, astar, PathResult


class TestDijkstra:
    """Tests pour l'algorithme de Dijkstra."""
    
    def test_simple_path(self):
        """Test sur un chemin simple."""
        g = Graph(directed=False)
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 1.0, 0.0)
        g.add_vertex(2, 2.0, 0.0)
        g.add_edge(0, 1, weight=1.0)
        g.add_edge(1, 2, weight=1.0)
        
        result = dijkstra(g, 0, 2)
        
        assert result.success
        assert result.path == [0, 1, 2]
        assert result.cost == 2.0
    
    def test_source_equals_target(self):
        """Test quand source = cible."""
        g = Graph()
        g.add_vertex(0)
        
        result = dijkstra(g, 0, 0)
        
        assert result.success
        assert result.path == [0]
        assert result.cost == 0.0
    
    def test_triangle_shortest(self):
        """Test sur un triangle : vérifier le plus court chemin."""
        g = Graph(directed=False)
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 4.0, 0.0)
        g.add_vertex(2, 2.0, 1.0)
        
        g.add_edge(0, 1, weight=10.0)  # Long
        g.add_edge(0, 2, weight=3.0)   # Court
        g.add_edge(2, 1, weight=3.0)   # Court
        
        result = dijkstra(g, 0, 1)
        
        assert result.success
        assert result.path == [0, 2, 1]
        assert result.cost == 6.0
    
    def test_no_path(self):
        """Test quand aucun chemin n'existe."""
        g = Graph(directed=True)
        g.add_vertex(0)
        g.add_vertex(1)
        # Pas d'arête
        
        result = dijkstra(g, 0, 1)
        
        assert not result.success
    
    def test_grid_path(self):
        """Test sur une grille 3×3."""
        g = Graph(directed=False)
        
        # Créer grille 3×3
        for i in range(9):
            row, col = i // 3, i % 3
            g.add_vertex(i, float(col), float(row))
        
        # Connexions horizontales et verticales
        for i in range(9):
            row, col = i // 3, i % 3
            if col < 2:  # Droite
                g.add_edge(i, i + 1, weight=1.0)
            if row < 2:  # Bas
                g.add_edge(i, i + 3, weight=1.0)
        
        result = dijkstra(g, 0, 8)  # Coin haut-gauche → coin bas-droit
        
        assert result.success
        assert result.cost == 4.0  # Distance de Manhattan
        assert len(result.path) == 5


class TestAstar:
    """Tests pour l'algorithme A*."""
    
    def test_simple_path(self):
        """Test sur un chemin simple."""
        g = Graph(directed=False)
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 1.0, 0.0)
        g.add_vertex(2, 2.0, 0.0)
        g.add_edge(0, 1, weight=1.0)
        g.add_edge(1, 2, weight=1.0)
        
        result = astar(g, 0, 2)
        
        assert result.success
        assert result.path == [0, 1, 2]
        assert result.cost == 2.0
    
    def test_optimality(self):
        """Test que A* trouve le même chemin que Dijkstra."""
        g = Graph(directed=False)
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 4.0, 0.0)
        g.add_vertex(2, 2.0, 1.0)
        
        g.add_edge(0, 1, weight=10.0)
        g.add_edge(0, 2, weight=3.0)
        g.add_edge(2, 1, weight=3.0)
        
        result_dijkstra = dijkstra(g, 0, 1)
        result_astar = astar(g, 0, 1)
        
        assert result_dijkstra.success and result_astar.success
        assert abs(result_dijkstra.cost - result_astar.cost) < 1e-6
    
    def test_heuristic_efficiency(self):
        """Test que A* visite moins de nœuds que Dijkstra."""
        g = Graph(directed=False)
        
        # Grille 10×10
        for i in range(100):
            row, col = i // 10, i % 10
            g.add_vertex(i, float(col), float(row))
        
        for i in range(100):
            row, col = i // 10, i % 10
            if col < 9:
                g.add_edge(i, i + 1)
            if row < 9:
                g.add_edge(i, i + 10)
        
        result_dijkstra = dijkstra(g, 0, 99)
        result_astar = astar(g, 0, 99)
        
        assert result_astar.success
        # A* devrait visiter au plus autant de nœuds que Dijkstra
        assert result_astar.visited_nodes <= result_dijkstra.visited_nodes
    
    def test_source_equals_target(self):
        """Test quand source = cible."""
        g = Graph()
        g.add_vertex(0, 0.0, 0.0)
        
        result = astar(g, 0, 0)
        
        assert result.success
        assert result.path == [0]
        assert result.cost == 0.0


class TestComparison:
    """Tests de comparaison entre algorithmes."""
    
    def test_same_cost(self):
        """Vérifier que les deux algorithmes trouvent le même coût."""
        g = Graph(directed=False)
        
        # Graphe aléatoire simple
        g.add_vertex(0, 0.0, 0.0)
        g.add_vertex(1, 1.0, 1.0)
        g.add_vertex(2, 2.0, 0.0)
        g.add_vertex(3, 3.0, 1.0)
        
        g.add_edge(0, 1, weight=2.0)
        g.add_edge(1, 2, weight=2.0)
        g.add_edge(2, 3, weight=2.0)
        g.add_edge(0, 2, weight=5.0)  # Chemin alternatif plus long
        
        result_dijkstra = dijkstra(g, 0, 3)
        result_astar = astar(g, 0, 3)
        
        assert result_dijkstra.success and result_astar.success
        assert abs(result_dijkstra.cost - result_astar.cost) < 1e-6
    
    def test_performance_difference(self):
        """Vérifier que A* est généralement plus rapide."""
        g = Graph(directed=False)
        
        # Grande grille
        size = 20
        for i in range(size * size):
            row, col = i // size, i % size
            g.add_vertex(i, float(col), float(row))
        
        for i in range(size * size):
            row, col = i // size, i % size
            if col < size - 1:
                g.add_edge(i, i + 1)
            if row < size - 1:
                g.add_edge(i, i + size)
        
        result_dijkstra = dijkstra(g, 0, size * size - 1)
        result_astar = astar(g, 0, size * size - 1)
        
        # A* devrait être plus rapide (en général)
        # Note : sur petits graphes, la différence peut être négligeable
        assert result_astar.success
        assert result_astar.visited_nodes <= result_dijkstra.visited_nodes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

