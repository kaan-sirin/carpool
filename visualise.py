import matplotlib.pyplot as plt
import pandas as pd
import math
import networkx as nx

# Function to load CSV files
def load_csv_files(areas_path, travels_path, districts_path):
    areas_df = pd.read_csv(areas_path)
    travels_df = pd.read_csv(travels_path)
    districts_df = pd.read_csv(districts_path)
    return areas_df, travels_df, districts_df

# Haversine formula to calculate distance between two geographical coordinates
def haversine(lat1, lon1, lat2, lon2):
    dlat = (lat2 - lat1)
    dlon = (lon2 - lon1)
    distance = math.sqrt(dlat**2 + dlon**2)*100
    return distance

# Step 1: Create a graph with areas as nodes and calculate distances as edges
def build_graph(areas_df):
    G = nx.Graph()

    # Adding areas as nodes
    for _, area in areas_df.iterrows():
        G.add_node(area["Id"], municipality=area["Municipality"], place=area["Place"], 
                   lat=area["Latitude"], lon=area["Longitude"])

    # Adding edges between areas based on proximity (optional based on data)
    for i, area1 in areas_df.iterrows():
        for j, area2 in areas_df.iterrows():
            if i < j:
                lat1, lon1 = area1["Latitude"], area1["Longitude"]
                lat2, lon2 = area2["Latitude"], area2["Longitude"]
                distance = haversine(lat1, lon1, lat2, lon2)

                # If the distance is below a threshold, connect the areas
                if distance < 5000000000000000:  # Adjust this threshold based on real-world data
                    G.add_edge(area1["Id"], area2["Id"], weight=distance)

    return G

# Function to visualize the graph
def visualize_graph(G):
    plt.figure(figsize=(10, 8))
    
    # Get positions using latitude and longitude
    pos = {node: (G.nodes[node]['lon'], G.nodes[node]['lat']) for node in G.nodes()}
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_weight="bold")
    
    # Draw edge labels (distance)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Graph Visualization of Areas")
    plt.show()
    
    
# Function to visualize the graph using first 20 entries and display edges with distances
def visualize_graph_with_edges(G, limit=20):
    plt.figure(figsize=(12, 10))
    
    # Limit the graph to the first 'limit' number of nodes
    limited_nodes = list(G.nodes)[:limit]
    limited_graph = G.subgraph(limited_nodes)
    
    # Get positions using latitude and longitude
    pos = {node: (limited_graph.nodes[node]['lon'], limited_graph.nodes[node]['lat']) for node in limited_graph.nodes()}
    
    # Draw the graph with limited nodes and display edges with distances
    nx.draw(limited_graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_weight="bold", edge_color='gray')
    
    # Draw edges with weight labels (distances)
    edge_labels = nx.get_edge_attributes(limited_graph, 'weight')
    nx.draw_networkx_edge_labels(limited_graph, pos, edge_labels=edge_labels)
    
    plt.title(f"Graph Visualization of First {limit} Areas with Edges and Distances")
    plt.show()

# Example for loading data and building the graph
areas_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/areas.csv"
travels_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/travels.csv"
districts_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/districts.csv"

# Load CSV data
areas_df, travels_df, districts_df = load_csv_files(areas_path, travels_path, districts_path)

# Build the graph using areas
G = build_graph(areas_df)

# Visualize the graph
# visualize_graph(G)

visualize_graph_with_edges(G, limit=20)

