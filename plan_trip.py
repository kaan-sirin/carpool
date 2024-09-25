import click
import networkx as nx
import json
import os

def find_trip_path(G, area_from, area_to):
    area_from, area_to = int(area_from), int(area_to)
    if area_from not in G or area_to not in G:
        print(f"Area {area_from} or {area_to} not found in graph")
        return None
    try:
        path = nx.shortest_path(G, source=area_from, target=area_to, weight='weight')
        return path
    except nx.NetworkXNoPath:
        print(f"No path found between Area {area_from} and Area {area_to}")
        return None


    
@click.command()
@click.option('--graph-path', type=click.Path(exists=True), required=True, help='Path to the graph gpickle file.')
@click.option('--area-id-from', help='Limit the number of nodes to visualize.')
@click.option('--area-id-to', help='Limit the number of nodes to visualize.')
@click.option('--output-file', type=str, default="trip_path.json", help='Name of the output JSON file.')
def main(graph_path, area_id_from, area_id_to, output_file):
    click.echo(f"Loading graph from {graph_path}...")
    G = nx.read_gpickle(graph_path)
    path = find_trip_path(G, area_id_from, area_id_to)
    click.echo(f"The path from {area_id_from} to {area_id_to} is: {path}")
    output_path = os.path.join(os.getcwd(), output_file)
    with open(output_path, 'w') as json_file:
        json.dump(path, json_file, indent=4)
    click.echo(f"Path saved to {output_path}")
    

    
if __name__ == '__main__':
    main()
