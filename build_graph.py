import click
import pandas as pd
import math
import networkx as nx


def load_areas_csv(areas_path):
    areas_df = pd.read_csv(areas_path)
    return areas_df
    

def haversine_distance(lat1, lon1, lat2, lon2):
    # radius of earth
    R = 6371.0  
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # haversine formlua
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def longest_shortest_distance(G):
    max_shortest = 0

    for node in G.nodes():
        # Find the shortest distance to any neighbor
        if G.degree[node] > 0:  # Only consider nodes with neighbors
            shortest_dist = min([G.edges[node, neighbor]['weight'] for neighbor in G.neighbors(node)])
            max_shortest = max(max_shortest, shortest_dist)

    return max_shortest

def build_graph(areas_df):
    G = nx.Graph()

    # add areas as nodes
    for _, area in areas_df.iterrows():
        G.add_node(area["Id"], municipality=area["Municipality"], place=area["Place"], 
                   lat=area["Latitude"], lon=area["Longitude"])

    for i, area1 in areas_df.iterrows():
        for j, area2 in areas_df.iterrows():
            if i < j:
                lat1, lon1 = area1["Latitude"], area1["Longitude"]
                lat2, lon2 = area2["Latitude"], area2["Longitude"]
                dist = haversine_distance(lat1, lon1, lat2, lon2)

                # If the distance is below a threshold, connect the areas
                if dist < 20:
                    G.add_edge(area1["Id"], area2["Id"], weight=dist)

    return G

@click.command()
@click.option('--areas-csv', type=click.Path(exists=True), required=True, help='Path to the areas CSV file.')
@click.option('--output-path', type=click.Path(), required=True, help='Path to save the output graph file.')
def main(areas_csv, output_path):
    click.echo(f"Loading areas from {areas_csv}...")
    areas_df = load_areas_csv(areas_csv)

    click.echo("Building graph...")
    G = build_graph(areas_df)
    min_max = longest_shortest_distance(G)
    click.echo(f"Longest shortest distance: {min_max}")

    click.echo(f"Saving graph to {output_path}...")
    nx.write_gpickle(G, output_path)
    click.echo("Graph saved successfully.")


if __name__ == '__main__':
    main()





