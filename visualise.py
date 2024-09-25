import click
import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(G, limit=20):
    plt.figure(figsize=(12, 10))

    # show only a limited number of nodes
    limited_nodes = list(G.nodes)[:limit]
    limited_graph = G.subgraph(limited_nodes)

    pos = {node: (limited_graph.nodes[node]['lon'], limited_graph.nodes[node]['lat']) for node in limited_graph.nodes()}

    # display edges with distances
    nx.draw(limited_graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_weight="bold", edge_color='gray', width=2)

    edge_labels = nx.get_edge_attributes(limited_graph, 'weight')
    edge_labels_rounded = {k: f"{v:.2f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(limited_graph, pos, edge_labels=edge_labels_rounded)

    plt.title(f"Graph Visualization of First {limit} Areas with Edges and Distances")
    plt.show()

@click.command()
@click.option('--graph-path', type=click.Path(exists=True), required=True, help='Path to the graph gpickle file.')
@click.option('--limit', default=20, help='Limit the number of nodes to visualize.')
def main(graph_path, limit):
    click.echo(f"Loading graph from {graph_path}...")
    G = nx.read_gpickle(graph_path)

    click.echo(f"Visualizing the graph with the first {limit} nodes...")
    visualize_graph(G, limit)


if __name__ == '__main__':
    main()


