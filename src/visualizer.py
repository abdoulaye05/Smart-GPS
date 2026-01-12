"""
Module de visualisation de graphes et de chemins.

Fournit des fonctions pour visualiser :
- Les graphes urbains
- Les chemins optimaux trouvés
- Les comparaisons entre algorithmes
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Optional, Dict
from .graph import Graph
from .algorithms import PathResult


def plot_graph(
    graph: Graph,
    figsize: tuple = (12, 10),
    node_size: int = 50,
    node_color: str = 'lightblue',
    edge_color: str = 'gray',
    edge_width: float = 0.5,
    show_labels: bool = False,
    title: str = "Graphe Urbain",
    save_path: Optional[str] = None
) -> None:
    """
    Visualise un graphe avec ses sommets et arêtes.
    
    Args:
        graph: Le graphe à visualiser
        figsize: Taille de la figure
        node_size: Taille des sommets
        node_color: Couleur des sommets
        edge_color: Couleur des arêtes
        edge_width: Épaisseur des arêtes
        show_labels: Afficher les labels des sommets
        title: Titre du graphique
        save_path: Chemin pour sauvegarder (si None, affiche)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Dessiner les arêtes
    for edge in graph.get_all_edges():
        v1 = graph.vertices[edge.source]
        v2 = graph.vertices[edge.target]
        
        ax.plot(
            [v1.x, v2.x],
            [v1.y, v2.y],
            color=edge_color,
            linewidth=edge_width,
            zorder=1,
            alpha=0.6
        )
    
    # Dessiner les sommets
    x_coords = [v.x for v in graph.vertices.values()]
    y_coords = [v.y for v in graph.vertices.values()]
    
    ax.scatter(
        x_coords,
        y_coords,
        s=node_size,
        c=node_color,
        edgecolors='black',
        linewidths=0.5,
        zorder=2,
        alpha=0.8
    )
    
    # Ajouter les labels si demandé
    if show_labels:
        for v in graph.vertices.values():
            ax.annotate(
                v.label,
                (v.x, v.y),
                fontsize=6,
                ha='center',
                va='bottom'
            )
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('X (longitude)', fontsize=12)
    ax.set_ylabel('Y (latitude)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_path(
    graph: Graph,
    path: List[int],
    path_color: str = 'red',
    path_width: float = 3.0,
    highlight_nodes: bool = True,
    title: str = "Plus Court Chemin",
    figsize: tuple = (12, 10),
    save_path: Optional[str] = None
) -> None:
    """
    Visualise un chemin sur le graphe.
    
    Args:
        graph: Le graphe
        path: Liste d'IDs de sommets formant le chemin
        path_color: Couleur du chemin
        path_width: Épaisseur du chemin
        highlight_nodes: Mettre en évidence les nœuds du chemin
        title: Titre du graphique
        figsize: Taille de la figure
        save_path: Chemin pour sauvegarder
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Dessiner toutes les arêtes (en gris clair)
    for edge in graph.get_all_edges():
        v1 = graph.vertices[edge.source]
        v2 = graph.vertices[edge.target]
        
        ax.plot(
            [v1.x, v2.x],
            [v1.y, v2.y],
            color='lightgray',
            linewidth=0.5,
            zorder=1,
            alpha=0.5
        )
    
    # Dessiner tous les sommets (petits, gris)
    x_coords = [v.x for v in graph.vertices.values()]
    y_coords = [v.y for v in graph.vertices.values()]
    
    ax.scatter(
        x_coords,
        y_coords,
        s=30,
        c='lightgray',
        edgecolors='gray',
        linewidths=0.3,
        zorder=2,
        alpha=0.6
    )
    
    # Dessiner le chemin
    if path and len(path) > 1:
        path_x = [graph.vertices[v_id].x for v_id in path]
        path_y = [graph.vertices[v_id].y for v_id in path]
        
        ax.plot(
            path_x,
            path_y,
            color=path_color,
            linewidth=path_width,
            zorder=3,
            label=f'Chemin (longueur: {len(path)} sommets)',
            marker='o',
            markersize=8,
            markerfacecolor=path_color,
            markeredgecolor='darkred',
            markeredgewidth=1.5
        )
        
        # Marquer le départ (vert)
        start = graph.vertices[path[0]]
        ax.scatter(
            [start.x],
            [start.y],
            s=200,
            c='green',
            marker='o',
            edgecolors='darkgreen',
            linewidths=2,
            zorder=5,
            label='Départ'
        )
        
        # Marquer l'arrivée (bleu)
        end = graph.vertices[path[-1]]
        ax.scatter(
            [end.x],
            [end.y],
            s=200,
            c='blue',
            marker='s',
            edgecolors='darkblue',
            linewidths=2,
            zorder=5,
            label='Arrivée'
        )
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('X (longitude)', fontsize=12)
    ax.set_ylabel('Y (latitude)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_comparison(
    results: Dict[str, PathResult],
    graph: Graph,
    title: str = "Comparaison des Algorithmes",
    figsize: tuple = (16, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Compare visuellement les résultats de plusieurs algorithmes.
    
    Args:
        results: Dictionnaire {nom_algo: PathResult}
        graph: Le graphe
        title: Titre du graphique
        figsize: Taille de la figure
        save_path: Chemin pour sauvegarder
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # Couleurs pour chaque algorithme
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    # 1. Comparaison des coûts
    ax1 = axes[0]
    algo_names = list(results.keys())
    costs = [results[name].cost if results[name].success else 0 for name in algo_names]
    
    bars = ax1.bar(algo_names, costs, color=colors[:len(algo_names)], alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Coût du chemin', fontsize=12)
    ax1.set_title('Coût Total', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for bar, cost in zip(bars, costs):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{cost:.1f}',
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    # 2. Comparaison des sommets visités
    ax2 = axes[1]
    visited = [results[name].visited_nodes for name in algo_names]
    
    bars = ax2.bar(algo_names, visited, color=colors[:len(algo_names)], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Nombre de sommets', fontsize=12)
    ax2.set_title('Sommets Visités', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, v in zip(bars, visited):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{v}',
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    # 3. Comparaison des temps d'exécution
    ax3 = axes[2]
    times_ms = [results[name].execution_time * 1000 for name in algo_names]
    
    bars = ax3.bar(algo_names, times_ms, color=colors[:len(algo_names)], alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Temps (ms)', fontsize=12)
    ax3.set_title('Temps d\'Exécution', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, t in zip(bars, times_ms):
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{t:.2f}',
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_performance_scaling(
    sizes: List[int],
    dijkstra_times: List[float],
    astar_times: List[float],
    title: str = "Analyse de Performance",
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Graphique montrant l'évolution du temps en fonction de la taille du graphe.
    
    Args:
        sizes: Liste des tailles de graphes (nombre de sommets)
        dijkstra_times: Temps d'exécution de Dijkstra (ms)
        astar_times: Temps d'exécution de A* (ms)
        title: Titre du graphique
        figsize: Taille de la figure
        save_path: Chemin pour sauvegarder
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(
        sizes,
        dijkstra_times,
        marker='o',
        linewidth=2,
        markersize=8,
        label='Dijkstra',
        color='#FF6B6B'
    )
    
    ax.plot(
        sizes,
        astar_times,
        marker='s',
        linewidth=2,
        markersize=8,
        label='A*',
        color='#4ECDC4'
    )
    
    ax.set_xlabel('Nombre de sommets (n)', fontsize=12)
    ax.set_ylabel('Temps d\'exécution (ms)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Échelle logarithmique si nécessaire
    if max(sizes) / min(sizes) > 100:
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_heatmap_distances(
    graph: Graph,
    source: int,
    distances: Dict[int, float],
    title: str = "Carte des Distances",
    figsize: tuple = (12, 10),
    save_path: Optional[str] = None
) -> None:
    """
    Visualise les distances depuis un sommet source avec une carte de chaleur.
    
    Args:
        graph: Le graphe
        source: Sommet source
        distances: Dictionnaire {vertex_id: distance}
        title: Titre du graphique
        figsize: Taille de la figure
        save_path: Chemin pour sauvegarder
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Préparer les données
    x_coords = []
    y_coords = []
    colors_vals = []
    
    for v_id, vertex in graph.vertices.items():
        x_coords.append(vertex.x)
        y_coords.append(vertex.y)
        dist = distances.get(v_id, float('inf'))
        colors_vals.append(dist if dist != float('inf') else max(distances.values()))
    
    # Dessiner les arêtes
    for edge in graph.get_all_edges():
        v1 = graph.vertices[edge.source]
        v2 = graph.vertices[edge.target]
        ax.plot(
            [v1.x, v2.x],
            [v1.y, v2.y],
            color='lightgray',
            linewidth=0.5,
            zorder=1,
            alpha=0.3
        )
    
    # Scatter plot avec couleurs
    scatter = ax.scatter(
        x_coords,
        y_coords,
        c=colors_vals,
        s=100,
        cmap='YlOrRd',
        edgecolors='black',
        linewidths=0.5,
        zorder=2
    )
    
    # Marquer la source
    source_vertex = graph.vertices[source]
    ax.scatter(
        [source_vertex.x],
        [source_vertex.y],
        s=300,
        c='blue',
        marker='*',
        edgecolors='darkblue',
        linewidths=2,
        zorder=3,
        label='Source'
    )
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Distance depuis la source', fontsize=12)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('X (longitude)', fontsize=12)
    ax.set_ylabel('Y (latitude)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    else:
        plt.show()
    
    plt.close()


