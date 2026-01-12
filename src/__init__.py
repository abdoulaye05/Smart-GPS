"""
Projet : Optimisation de Trajets Urbains - GPS Intelligent
BUT Informatique - Semestre 5

Ce package contient l'implémentation des algorithmes de plus court chemin
et des outils de visualisation pour la modélisation de réseaux urbains.
"""

__version__ = "1.0.0"
__author__ = "Équipe ProjetS5"

from .graph import Graph, Vertex, Edge
from .algorithms import dijkstra, astar
from .generators import generate_grid_graph, generate_random_urban_graph
from .visualizer import plot_graph, plot_path, plot_comparison

__all__ = [
    "Graph",
    "Vertex",
    "Edge",
    "dijkstra",
    "astar",
    "generate_grid_graph",
    "generate_random_urban_graph",
    "plot_graph",
    "plot_path",
    "plot_comparison",
]


