import pandas as pd
import math
import networkx as nx

def load_csv_files(areas_path, travels_path, districts_path):
    areas_df = pd.read_csv(areas_path)
    travels_df = pd.read_csv(travels_path)
    districts_df = pd.read_csv(districts_path)
    return areas_df, travels_df, districts_df

def distance(lat1, lon1, lat2, lon2):
    dlat = (lat2 - lat1)
    dlon = (lon2 - lon1)
    dist = math.sqrt(dlat**2 + dlon**2)*100
    return dist

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
                dist = distance(lat1, lon1, lat2, lon2)

                # If the distance is below a threshold, connect the areas
                if dist < 8:
                    G.add_edge(area1["Id"], area2["Id"], weight=dist)

    return G

def find_trip_path(G, area_from, area_to):
    if area_from not in G or area_to not in G:
        print(f"Area {area_from} or {area_to} not found in graph")
        return None
    try:
        path = nx.shortest_path(G, source=area_from, target=area_to, weight='weight')
        return path
    except nx.NetworkXNoPath:
        print(f"No path found between Area {area_from} and Area {area_to}")
        return None

def check_destinations_in_order(trip, fromAreaId, toAreaId):
    try:
        index_1 = trip.index(fromAreaId)
        index_2 = trip.index(toAreaId)
        return index_1 < index_2
    except ValueError:
        return False

areas_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/areas.csv"
travels_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/travels.csv"
districts_path = "/Users/kaansirin/Desktop/ETSN05/dataleverans/districts.csv"

areas_df, travels_df, districts_df = load_csv_files(areas_path, travels_path, districts_path)
travels_df = travels_df.dropna(subset=['AreaIdFrom', 'AreaIdTo'])

G = build_graph(areas_df)

first_trip = travels_df.iloc[0]  
trip_path = find_trip_path(G, int(first_trip['AreaIdFrom']), int(first_trip['AreaIdTo']))

result = check_destinations_in_order(trip_path, 65, 59)
print(trip_path)
print(result)
