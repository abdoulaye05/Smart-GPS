#!/usr/bin/env python3
"""
Application Web Interactive - GPS Intelligent
Version démo avec carte interactive Folium

Installation requise:
    pip install folium streamlit streamlit-folium osmnx

Lancement:
    streamlit run webapp_demo.py
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import time
import math
from src.graph import Graph
from src.algorithms import astar, dijkstra, bellman_ford
from src.generators import generate_random_urban_graph
from src.utils import print_path_result

# Import OSMnx pour les vraies données géographiques
try:
    import osmnx as ox
    OSMNX_AVAILABLE = True
except ImportError:
    OSMNX_AVAILABLE = False
    # Le warning sera affiché dans la sidebar si l'utilisateur essaie d'utiliser les vraies routes


def create_real_city_from_osm(place_name="11e Arrondissement, Paris, France", network_type="drive", simplify=True, max_nodes=5000):
    """
    Crée un graphe à partir des vraies données OpenStreetMap.
    
    Args:
        place_name: Nom du lieu (ex: "Paris, France", "Les Halles, Paris")
        network_type: Type de réseau ("drive", "walk", "bike", "all")
        simplify: Si True, simplifie le graphe (enlève les nœuds intermédiaires)
    
    Returns:
        Graph avec vraies coordonnées géographiques
    """
    if not OSMNX_AVAILABLE:
        return create_sample_city()
    
    try:
        # Télécharger le réseau routier depuis OpenStreetMap
        with st.spinner("📥 Téléchargement des données OpenStreetMap..."):
            G_osm = ox.graph_from_place(place_name, network_type=network_type, simplify=False)
        
        # Simplifier le graphe pour réduire le nombre de nœuds
        if simplify:
            with st.spinner("🔧 Simplification du graphe..."):
                G_osm = ox.simplify_graph(G_osm)
        
        # Convertir NetworkX vers notre format Graph
        graph = Graph(directed=False)
        graph.is_geographic = True
        
        # Créer un mapping OSM node_id -> notre vertex_id
        node_mapping = {}
        vertex_id = 0
        
        # Ajouter tous les sommets avec leurs vraies coordonnées
        with st.spinner("📍 Conversion des intersections..."):
            for node_id, data in G_osm.nodes(data=True):
                lat = data.get('y', 0)  # OSMnx utilise 'y' pour latitude
                lng = data.get('x', 0)  # OSMnx utilise 'x' pour longitude
                
                graph.add_vertex(vertex_id, lng, lat, label=f"OSM_{node_id}")
                node_mapping[node_id] = vertex_id
                vertex_id += 1
        
        # Ajouter toutes les arêtes avec leurs vraies longueurs
        with st.spinner("🛣️ Conversion des routes..."):
            edges_added = 0
            for u, v, data in G_osm.edges(data=True):
                if u in node_mapping and v in node_mapping:
                    # Utiliser la longueur réelle de l'arête (en mètres)
                    length_m = data.get('length', 0)
                    if length_m == 0:
                        # Si pas de longueur, calculer depuis les coordonnées
                        u_node = G_osm.nodes[u]
                        v_node = G_osm.nodes[v]
                        lat1, lng1 = u_node.get('y', 0), u_node.get('x', 0)
                        lat2, lng2 = v_node.get('y', 0), v_node.get('x', 0)
                        # Distance haversine approximative (en mètres)
                        R = 6371000  # Rayon de la Terre en mètres
                        dlat = math.radians(lat2 - lat1)
                        dlng = math.radians(lng2 - lng1)
                        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
                        length_m = 2 * R * math.asin(math.sqrt(a))
                    
                    # Convertir en kilomètres pour le poids
                    weight_km = length_m / 1000.0
                    
                    # Éviter les doublons (graphe non orienté)
                    if not graph.has_edge(node_mapping[u], node_mapping[v]):
                        graph.add_edge(
                            node_mapping[u], 
                            node_mapping[v], 
                            weight=weight_km
                        )
                        edges_added += 1
        
        # Ne pas afficher de message ici - sera géré dans main()
        return graph
    
    except Exception as e:
        # Logger l'erreur mais ne pas afficher de message (sera géré dans main())
        import traceback
        print(f"Erreur OSM: {str(e)}")
        traceback.print_exc()
        # Retourner le graphe généré en cas d'erreur
        return create_sample_city()


def create_sample_city():
    """Crée une ville d'exemple avec un graphe généré (pas de vraies coordonnées)."""
    graph = generate_random_urban_graph(
        num_vertices=100,
        avg_degree=4,
        width=0.02,  # En degrés (latitude/longitude)
        height=0.02
    )
    
    # Décaler pour centrer sur Paris (exemple)
    base_lat, base_lng = 48.85, 2.34
    for vertex in graph.vertices.values():
        vertex.x = base_lng + vertex.x
        vertex.y = base_lat + vertex.y
    
    return graph


def graph_to_folium_map(graph, center_lat=48.85, center_lng=2.34):
    """Convertit le graphe en carte Folium."""
    map = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=14,
        tiles='OpenStreetMap'
    )
    
    # Dessiner les arêtes (routes)
    for edge in graph.get_all_edges():
        v1 = graph.vertices[edge.source]
        v2 = graph.vertices[edge.target]
        
        folium.PolyLine(
            [[v1.y, v1.x], [v2.y, v2.x]],
            color='gray',
            weight=2,
            opacity=0.5
        ).add_to(map)
    
    # Dessiner les sommets (intersections)
    for vertex in graph.vertices.values():
        folium.CircleMarker(
            [vertex.y, vertex.x],
            radius=3,
            color='blue',
            fill=True,
            fillColor='lightblue',
            fillOpacity=0.6,
            popup=f"Intersection {vertex.id}"
        ).add_to(map)
    
    return map


def add_path_to_map(map, graph, path, color='red', transport_icon='<i class="fas fa-car"></i>'):
    """Ajoute un chemin sur la carte."""
    if not path or len(path) < 2:
        return
    
    # Ligne du chemin
    coords = [[graph.vertices[v].y, graph.vertices[v].x] for v in path]
    folium.PolyLine(
        coords,
        color=color,
        weight=5,
        opacity=0.8
    ).add_to(map)
    
    # Marqueur départ (vert) avec le bon moyen de transport
    start = graph.vertices[path[0]]
    folium.Marker(
        [start.y, start.x],
        popup=f"{transport_icon} Départ",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(map)
    
    # Marqueur arrivée (rouge)
    end = graph.vertices[path[-1]]
    folium.Marker(
        [end.y, end.x],
        popup="Arrivée",
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(map)
    
    return map



def create_exploration_map(graph, result, color='#3388ff'):
    """Crée une carte montrant la zone explorée."""
    # Calculer le centre (barycentre des nœuds explorés ou du graphe)
    if result.explored_nodes:
        # Centre sur les nœuds explorés
        explored_vertices = [graph.vertices[v_id] for v_id in result.explored_nodes if v_id in graph.vertices]
        if explored_vertices:
            avg_x = sum(v.x for v in explored_vertices) / len(explored_vertices)
            avg_y = sum(v.y for v in explored_vertices) / len(explored_vertices)
        else:
            avg_x, avg_y = 2.34, 48.85
    else:
        avg_x, avg_y = 2.34, 48.85
        
    m = folium.Map(location=[avg_y, avg_x], zoom_start=14, tiles='cartodbpositron')
    
    # Dessiner les nœuds explorés
    if result.explored_nodes:
        for v_id in result.explored_nodes:
            if v_id in graph.vertices:
                v = graph.vertices[v_id]
                folium.Circle(
                    location=[v.y, v.x],
                    radius=15,
                    color=color,
                    fill=True,
                    fill_opacity=0.4,
                    weight=0
                ).add_to(m)
            
    # Ajouter le chemin final
    if result.success:
        add_path_to_map(m, graph, result.path, color='black', transport_icon='')
        
    return m

@st.dialog("Comparaison des Performances", width="large")
def show_comparison_dialog(graph, source, target):
    """Affiche la comparaison dans une fenêtre modale."""
    st.markdown("""
        <div style='margin-bottom: 1rem; background-color: #e7f3ff; color: #000000; border-left: 4px solid #2196F3; padding: 0.75rem; border-radius: 0.25rem;'>
            <i class='fas fa-info-circle'></i> <strong>Comparaison en cours...</strong> Les 3 algorithmes sont calculés en temps réel.
        </div>
    """, unsafe_allow_html=True)
    
    # Calculer avec les 3 algorithmes
    with st.spinner("Calcul en cours..."):
        result_dijkstra = dijkstra(graph, source, target)
        result_astar = astar(graph, source, target)
        result_bellman = bellman_ford(graph, source, target)
    
    # Affichage côte à côte
    col_dijk, col_astar, col_bell = st.columns(3)
    
    map_height = 350  # Plus grand pour la popup
    
    with col_dijk:
        st.markdown("### <i class='fas fa-square'></i> Dijkstra", unsafe_allow_html=True)
        if result_dijkstra.success:
            st.metric("Temps", f"{result_dijkstra.execution_time*1000:.2f} ms")
            st.metric("Sommets explorés", result_dijkstra.visited_nodes)
            st.caption("Exploration uniforme (cercle)")
            
            # Carte exploration
            m_dijk = create_exploration_map(graph, result_dijkstra, color='#FF5733') # Rouge/Orange
            st_folium(m_dijk, width=None, height=map_height, key="map_dijk_popup")
        else:
            st.error("Échec")
    
    with col_astar:
        st.markdown("### <i class='fas fa-star'></i> A*", unsafe_allow_html=True)
        if result_astar.success:
            st.metric("Temps", f"{result_astar.execution_time*1000:.2f} ms")
            st.metric("Sommets explorés", result_astar.visited_nodes)
            st.caption("Exploration dirigée (faisceau)")
            
            # Indicateur de performance
            if result_astar.visited_nodes < result_dijkstra.visited_nodes:
                st.markdown(f"""
                    <div style='background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 0.25rem; padding: 0.5rem; margin-bottom: 0.5rem; color: #155724; font-size: 0.9em;'>
                        <i class='fas fa-bolt'></i> <strong>{((result_dijkstra.visited_nodes - result_astar.visited_nodes) / result_dijkstra.visited_nodes * 100):.0f}% moins de nœuds</strong>
                    </div>
                """, unsafe_allow_html=True)
            
            # Carte exploration
            m_astar = create_exploration_map(graph, result_astar, color='#3388ff') # Bleu
            st_folium(m_astar, width=None, height=map_height, key="map_astar_popup")

        else:
            st.error("Échec")
    
    with col_bell:
        st.markdown("### <i class='fas fa-shield-alt'></i> Bellman-Ford", unsafe_allow_html=True)
        if result_bellman.success:
            st.metric("Temps", f"{result_bellman.execution_time*1000:.2f} ms")
            st.metric("Sommets explorés", result_bellman.visited_nodes)
            st.caption("Exploration exhaustive")
            
            # Carte exploration
            m_bell = create_exploration_map(graph, result_bellman, color='#888888') # Gris
            st_folium(m_bell, width=None, height=map_height, key="map_bell_popup")

        else:
            st.error("Échec")
    
    # Vérification de cohérence
    st.markdown("---")
    if result_dijkstra.success and result_astar.success and result_bellman.success:
        if abs(result_dijkstra.cost - result_astar.cost) < 0.001 and abs(result_astar.cost - result_bellman.cost) < 0.001:
            st.success("✅ Tous les algorithmes trouvent le même chemin optimal !")
        else:
            st.warning("⚠️ Les algorithmes trouvent des chemins différents.")


def main():
    """Application principale."""
    
    # Configuration de la page
    st.set_page_config(
        page_title="GPS Intelligent",
        page_icon="🧭",
        layout="wide"
    )
    

    
    # Charger Font Awesome
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
        .icon-title {
            font-size: 2.5rem;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Titre avec icône
    st.markdown("""
        <div class="icon-title">
            <i class="fas fa-map-marked-alt"></i>
            <span>GPS Intelligent - Application Interactive</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("**Navigation optimale avec algorithmes de graphes**")
    
    # Sidebar
    st.sidebar.markdown("""
        <div class="section-header">
            <i class="fas fa-cog"></i>
            <h2 style="margin: 0;">Configuration</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Option pour choisir le type de graphe
    st.sidebar.markdown("---")
    st.sidebar.markdown("### <i class='fas fa-map'></i> Type de carte", unsafe_allow_html=True)
    
    # Afficher un avertissement si OSMnx n'est pas disponible
    if not OSMNX_AVAILABLE:
        st.sidebar.error("""
        ⚠️ **OSMnx non installé**
        
        Pour utiliser les vraies routes et distances :
        ```bash
        pip install osmnx>=1.8.0
        ```
        """)
    
    use_real_map = st.sidebar.checkbox(
        "Utiliser les vraies routes (OpenStreetMap)",
        value=False,
        disabled=not OSMNX_AVAILABLE,
        help="Active les vraies coordonnées géographiques et distances réelles. Plus lent au chargement." if OSMNX_AVAILABLE else "OSMnx doit être installé pour activer cette option."
    )
    
    # Initialiser le graphe
    graph_key = f"graph_{use_real_map}"
    is_real_graph_key = f"is_real_graph_{use_real_map}"
    loading_message_key = f"loading_msg_{use_real_map}"
    
    if graph_key not in st.session_state:
        if use_real_map and OSMNX_AVAILABLE:
            # Essayer de charger OSM (zone plus petite pour éviter les timeouts)
            # Utiliser une zone plus petite que tout Paris pour un chargement plus rapide
            try:
                graph = create_real_city_from_osm("11e Arrondissement, Paris, France", "drive", max_nodes=3000)
                st.session_state[graph_key] = graph
                # Vérifier si c'est vraiment un graphe OSM (plus de 500 sommets = probablement OSM)
                # Un graphe généré a 100 sommets
                is_real = graph.num_vertices() > 150  # Seuil pour distinguer OSM du graphe généré (100)
                st.session_state[is_real_graph_key] = is_real
                
                if is_real:
                    st.session_state[loading_message_key] = {
                        "type": "success",
                        "message": f"✅ Carte OSM chargée : {graph.num_vertices()} intersections, {graph.num_edges_count()} routes"
                    }
                else:
                    st.session_state[loading_message_key] = {
                        "type": "warning",
                        "message": "⚠️ Le chargement OSM a échoué. Utilisation d'un graphe généré."
                    }
            except Exception as e:
                # En cas d'erreur, utiliser le graphe généré
                st.session_state[graph_key] = create_sample_city()
                st.session_state[is_real_graph_key] = False
                st.session_state[loading_message_key] = {
                    "type": "error",
                    "message": f"❌ Erreur lors du chargement OSM : {str(e)[:100]}..."
                }
        else:
            with st.spinner("Chargement de la carte..."):
                st.session_state[graph_key] = create_sample_city()
                st.session_state[is_real_graph_key] = False
                st.session_state[loading_message_key] = None
    else:
        # Récupérer le flag existant
        if is_real_graph_key not in st.session_state:
            # Pour les anciens graphes, vérifier le nombre de sommets
            graph = st.session_state[graph_key]
            st.session_state[is_real_graph_key] = graph.num_vertices() > 150
    
    graph = st.session_state[graph_key]
    is_real_graph = st.session_state.get(is_real_graph_key, False)
    
    # Afficher UN SEUL message selon l'état du graphe
    if not is_real_graph and not use_real_map:
        # Graphe généré normal (utilisateur n'a pas coché OSM)
        st.sidebar.info("ℹ️ **Graphe généré** : Les distances affichées ne sont pas réalistes. Cochez 'Utiliser les vraies routes' pour des distances réelles.")
    elif not is_real_graph and use_real_map:
        # L'utilisateur a coché OSM mais le chargement a échoué
        # Afficher le message détaillé si disponible, sinon un message générique
        if loading_message_key in st.session_state and st.session_state[loading_message_key]:
            msg_data = st.session_state[loading_message_key]
            if msg_data["type"] == "error":
                st.sidebar.error(msg_data["message"])
            else:
                st.sidebar.warning("⚠️ **Le chargement OSM a échoué**. Utilisation d'un graphe généré. Les distances ne sont pas réalistes.")
        else:
            st.sidebar.warning("⚠️ **Le chargement OSM a échoué**. Utilisation d'un graphe généré. Les distances ne sont pas réalistes.")
    else:
        # Graphe OSM chargé avec succès
        if loading_message_key in st.session_state and st.session_state[loading_message_key]:
            msg_data = st.session_state[loading_message_key]
            if msg_data["type"] == "success":
                st.sidebar.success(msg_data["message"])
            else:
                st.sidebar.success("✅ **Vraies routes OSM** : Les distances affichées sont réelles.")
        else:
            st.sidebar.success("✅ **Vraies routes OSM** : Les distances affichées sont réelles.")
    
    # Options
    st.sidebar.subheader("Algorithme")
    algo_choice = st.sidebar.radio(
        "Choisir l'algorithme:",
        ["A* (Recommandé)", "Dijkstra", "Bellman-Ford"]
    )
    
    # Moyen de transport
    st.sidebar.markdown("---")
    st.sidebar.markdown("### <i class='fas fa-traffic-light'></i> Moyen de transport", unsafe_allow_html=True)
    transport_mode = st.sidebar.selectbox(
        "Choisir le moyen de transport:",
        ["Voiture", "Vélo", "À pied"],
        help="Change la vitesse et le temps de trajet"
    )
    
    # Définir les vitesses et temps incompressibles selon le moyen de transport
    if transport_mode == "Voiture":
        base_speed = 50  # km/h
        t0 = 15  # Temps incompressible (secondes)
        transport_icon = "<i class='fas fa-car'></i>"
    elif transport_mode == "Vélo":
        base_speed = 15  # km/h
        t0 = 8   # Temps incompressible (secondes)
        transport_icon = "<i class='fas fa-bicycle'></i>"
    else:  # À pied
        base_speed = 5   # km/h
        t0 = 5   # Temps incompressible (secondes)
        transport_icon = "<i class='fas fa-walking'></i>"
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Points de départ/arrivée")
    
    # Sélection des sommets
    vertices = list(graph.vertices.keys())
    
    col1, col2 = st.sidebar.columns([1, 4])
    with col1:
        st.markdown('<i class="fas fa-dice" style="font-size: 1.2rem; margin-top: 0.5rem;"></i>', unsafe_allow_html=True)
    with col2:
        # Bouton aléatoire avec icône
        st.markdown("""
            <style>
            .stButton button {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Aléatoire", help="Générer des points aléatoires", use_container_width=True):
            st.session_state.source = random.choice(vertices)
            st.session_state.target = random.choice([v for v in vertices if v != st.session_state.get('source')])
    
    source = st.sidebar.selectbox(
        "Départ",
        vertices,
        index=vertices.index(st.session_state.get('source', vertices[0]))
    )
    
    target = st.sidebar.selectbox(
        "Arrivée",
        vertices,
        index=vertices.index(st.session_state.get('target', vertices[-1]))
    )
    
    st.session_state.source = source
    st.session_state.target = target
    
    # Bouton calculer avec icône
    col_rocket, col_button = st.sidebar.columns([1, 4])
    with col_rocket:
        st.markdown('<i class="fas fa-rocket" style="font-size: 1.2rem; margin-top: 0.5rem;"></i>', unsafe_allow_html=True)
    with col_button:
        calculate = st.button("Calculer le trajet", type="primary", use_container_width=True)
    
    # Informations sur le graphe
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div class="section-header">
            <i class="fas fa-chart-bar"></i>
            <h3 style="margin: 0;">Statistiques du réseau</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_stat1, col_stat2 = st.sidebar.columns([1, 2])
    with col_stat1:
        st.markdown('<i class="fas fa-circle-notch" style="font-size: 1.5rem;"></i>', unsafe_allow_html=True)
    with col_stat2:
        st.metric("Intersections", graph.num_vertices())
    
    col_stat3, col_stat4 = st.sidebar.columns([1, 2])
    with col_stat3:
        st.markdown('<i class="fas fa-road" style="font-size: 1.5rem;"></i>', unsafe_allow_html=True)
    with col_stat4:
        st.metric("Routes", graph.num_edges_count())
    
    col_stat5, col_stat6 = st.sidebar.columns([1, 2])
    with col_stat5:
        st.markdown('<i class="fas fa-project-diagram" style="font-size: 1.5rem;"></i>', unsafe_allow_html=True)
    with col_stat6:
        st.metric("Degré moyen", f"{graph.average_degree():.1f}")
    
    # Carte principale
    col_map, col_results = st.columns([2, 1])
    
    with col_map:
        st.markdown("""
            <div class="section-header">
                <i class="fas fa-map" style="font-size: 1.8rem;"></i>
                <h2 style="margin: 0;">Carte Interactive</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Créer la carte
        map = graph_to_folium_map(graph)
        
        # Messages d'aide contextuels (UX améliorée)
        if source == target:
            st.markdown("""
                <div style='background-color: #fff3cd; color: #856404; border: 1px solid #ffc107; border-radius: 0.25rem; padding: 0.75rem; margin: 1rem 0;'>
                    <i class='fas fa-exclamation-triangle'></i> <strong>Départ et arrivée identiques !</strong> Choisissez deux points différents.
                </div>
            """, unsafe_allow_html=True)
        elif not calculate and 'result' not in st.session_state:
            st.markdown("""
                <div style='background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; border-radius: 0.25rem; padding: 0.75rem; margin: 1rem 0;'>
                    <i class='fas fa-hand-point-right'></i> <strong>Sélectionnez un départ et une arrivée, puis cliquez sur '<i class='fas fa-rocket'></i> Calculer le trajet'</strong>
                </div>
            """, unsafe_allow_html=True)
        
        # Calculer et afficher le chemin si demandé
        if calculate or 'result' in st.session_state:
            if source != target:
                # Barre de progression et messages
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.markdown("<i class='fas fa-search'></i> **Initialisation de l'algorithme...**", unsafe_allow_html=True)
                progress_bar.progress(20)
                
                # Choisir l'algorithme
                if algo_choice == "A* (Recommandé)":
                    status_text.markdown("<i class='fas fa-star'></i> **Calcul avec A* (heuristique guidée)...**", unsafe_allow_html=True)
                    progress_bar.progress(50)
                    result = astar(graph, source, target)
                elif algo_choice == "Dijkstra":
                    status_text.markdown("<i class='fas fa-square'></i> **Calcul avec Dijkstra (exploration complète)...**", unsafe_allow_html=True)
                    progress_bar.progress(50)
                    result = dijkstra(graph, source, target)
                else:  # Bellman-Ford
                    status_text.markdown("<i class='fas fa-shield-alt'></i> **Calcul avec Bellman-Ford (poids négatifs)...**", unsafe_allow_html=True)
                    progress_bar.progress(50)
                    result = bellman_ford(graph, source, target)
                
                progress_bar.progress(80)
                status_text.markdown("<i class='fas fa-chart-bar'></i> **Analyse des résultats...**", unsafe_allow_html=True)
                
                st.session_state.result = result
                
                if result.success:
                    progress_bar.progress(100)
                    status_text.markdown(f"<div style='color: green;'><i class='fas fa-check-circle'></i> <strong>Trajet trouvé !</strong> Distance : {result.cost:.2f} km</div>", unsafe_allow_html=True)
                    time.sleep(0.5)  # Afficher le message de succès
                    progress_bar.empty()
                    status_text.empty()
                else:
                    progress_bar.empty()
                    status_text.markdown("<div style='color: red;'><i class='fas fa-times-circle'></i> <strong>Aucun chemin trouvé</strong> entre ces deux points.</div>", unsafe_allow_html=True)
        
        # Afficher le chemin
        if 'result' in st.session_state and st.session_state.result.success:
            map = add_path_to_map(map, graph, st.session_state.result.path, transport_icon=transport_icon)
        
        # Afficher la carte
        st_folium(map, width=700, height=500)
    
    with col_results:
        st.markdown("""
            <div class="section-header">
                <i class="fas fa-chart-line" style="font-size: 1.8rem;"></i>
                <h2 style="margin: 0;">Résultats</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if 'result' in st.session_state and st.session_state.result.success:
            result = st.session_state.result
            
            # Afficher le moyen de transport utilisé
            st.markdown(f"### {transport_icon} Trajet en **{transport_mode}**", unsafe_allow_html=True)
            st.caption(f"Vitesse : {base_speed} km/h • Temps incompressible : {t0}s")
            st.markdown("---")
            
            # Métriques principales
            col_m1, col_m2 = st.columns([1, 4])
            with col_m1:
                st.markdown('<i class="fas fa-route" style="font-size: 2rem; color: #667eea;"></i>', unsafe_allow_html=True)
            with col_m2:
                st.metric("Distance", f"{result.cost:.4f} km")
            
            # ═══════════════════════════════════════════════════════════════
            # CALCUL DU TEMPS RÉALISTE (Modèle mathématique amélioré)
            # ═══════════════════════════════════════════════════════════════
            # 
            # Modèle : t = t₀ + d/v
            # 
            # Où :
            #   - t₀ = temps incompressible (démarrage, arrêt, feux)
            #   - d/v = temps de déplacement à vitesse constante
            #
            # Ce modèle est plus réaliste car :
            #   1. Il y a un temps minimum même pour distance → 0
            #   2. Le temps croît linéairement avec la distance
            #   3. Physiquement justifiable (phase statique + phase mobile)
            # ═══════════════════════════════════════════════════════════════
            
            distance_km = result.cost
            effective_speed = base_speed
            
            # Calcul du temps : t = t₀ + d/v
            time_variable = (distance_km / effective_speed) * 3600  # Temps en mouvement
            time_seconds_realistic = t0 + time_variable
            
            # Affichage adaptatif
            col_m3, col_m4 = st.columns([1, 4])
            with col_m3:
                st.markdown('<i class="fas fa-clock" style="font-size: 2rem; color: #667eea;"></i>', unsafe_allow_html=True)
            with col_m4:
                if time_seconds_realistic < 60:
                    st.metric(
                        "Temps estimé", 
                        f"{time_seconds_realistic:.0f} sec",
                        help=f"Modèle : t = {t0}s (fixe) + {time_variable:.1f}s (trajet) = {time_seconds_realistic:.1f}s"
                    )
                else:
                    time_minutes = time_seconds_realistic / 60
                    st.metric(
                        "Temps estimé", 
                        f"{time_minutes:.1f} min",
                        help=f"Modèle : t = {t0}s (fixe) + {time_variable:.1f}s (trajet) = {time_seconds_realistic:.1f}s"
                    )
            
            col_m5, col_m6 = st.columns([1, 4])
            with col_m5:
                st.markdown('<i class="fas fa-location-dot" style="font-size: 2rem; color: #667eea;"></i>', unsafe_allow_html=True)
            with col_m6:
                st.metric("Étapes", len(result.path))
            
            st.markdown("---")
            
            # ═══════════════════════════════════════════════════════════════
            # COMPARAISON CÔTE À CÔTE DES 3 ALGORITHMES (Optionnel avec bouton)
            # ═══════════════════════════════════════════════════════════════
            # Initialiser l'état de la comparaison
            if 'show_comparison' not in st.session_state:
                st.session_state.show_comparison = False
            
            # Bouton pour afficher/masquer la comparaison
            # Utiliser toute la largeur pour éviter que le texte soit coupé
            # Bouton pour afficher/masquer la comparaison (Popup)
            if st.button("Comparer les 3 Algorithmes (Popup)", use_container_width=True, type="primary"):
                show_comparison_dialog(graph, source, target)

            
            # (Ancien code de comparaison supprimé/remplacé par le dialog)

            
            st.markdown("---")
            
            # Statistiques détaillées de l'algorithme sélectionné
            st.markdown("""
                <div class="section-header">
                    <i class="fas fa-microchip" style="font-size: 1.5rem;"></i>
                    <h3 style="margin: 0;">Détails de l'algorithme sélectionné</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Sommets visités", result.visited_nodes)
            with col_b:
                st.metric("Arêtes explorées", result.relaxed_edges)
            
            st.metric("Temps de calcul", f"{result.execution_time * 1000:.2f} ms")
            
            # Efficacité
            efficiency = (result.visited_nodes / graph.num_vertices()) * 100
            st.progress(efficiency / 100)
            st.caption(f"Efficacité : {efficiency:.1f}% du réseau exploré")
            
            # Itinéraire
            st.markdown("---")
            st.markdown("### <i class='fas fa-compass'></i> Itinéraire", unsafe_allow_html=True)
            
            if len(result.path) <= 15:
                for i, vertex_id in enumerate(result.path):
                    if i == 0:
                        st.markdown(f"<i class='fas fa-circle' style='color: green;'></i> **Départ** : Intersection {vertex_id}", unsafe_allow_html=True)
                    elif i == len(result.path) - 1:
                        st.markdown(f"<i class='fas fa-circle' style='color: red;'></i> **Arrivée** : Intersection {vertex_id}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"   <i class='fas fa-arrow-down'></i> Intersection {vertex_id}", unsafe_allow_html=True)
            else:
                st.markdown(f"<i class='fas fa-circle' style='color: green;'></i> **Départ** : Intersection {result.path[0]}", unsafe_allow_html=True)
                st.markdown(f"   <i class='fas fa-ellipsis-v'></i> {len(result.path) - 2} étapes intermédiaires", unsafe_allow_html=True)
                st.markdown(f"<i class='fas fa-circle' style='color: red;'></i> **Arrivée** : Intersection {result.path[-1]}", unsafe_allow_html=True)
        

    
    # Section d'aide
    st.markdown("---")
    with st.expander("Comment utiliser cette application ?"):
        st.markdown("""
        <i class='fas fa-book' style='font-size: 1.2rem;'></i> **Mode d'emploi**
        
        1. **Sélectionnez** un point de départ et d'arrivée dans la barre latérale
        2. **Choisissez** l'algorithme (A* est recommandé car plus rapide)
        3. **Cliquez** sur "Calculer le trajet"
        4. **Visualisez** le chemin optimal en bleu sur la carte
        
        ### Légende
        
        - <i class='fas fa-circle' style='color: green;'></i> **Point vert** : Départ
        - <i class='fas fa-circle' style='color: red;'></i> **Point rouge** : Arrivée
        - <i class='fas fa-circle' style='color: blue;'></i> **Ligne bleue** : Chemin optimal calculé
        - <i class='fas fa-circle' style='color: gray;'></i> **Points gris** : Intersections du réseau
        
        ### Algorithmes
        
        - **A*** <i class='fas fa-star'></i> : Le plus rapide, utilise une heuristique pour se diriger vers la cible (Recommandé)
        - **Dijkstra** <i class='fas fa-square'></i> : Explore dans toutes les directions, garanti optimal
        - **Bellman-Ford** <i class='fas fa-shield-alt'></i> : Supporte les poids négatifs, plus lent (O(n·m))
        
        Les trois garantissent de trouver le plus court chemin !
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Projet BUT Informatique S5** | Diallo Abdoulaye, Semih Taskin, Muller Arthur")


if __name__ == "__main__":
    main()

