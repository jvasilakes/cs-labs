import string
import argparse
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="Path to file containing graph definition")
    parser.add_argument("outfile", type=str,
                        help="Where to write the graph coloring.")
    return parser.parse_args()


def main(infile, outfile):
    graph = read_graph(infile)
    colors = list(string.ascii_uppercase)
    colored_graph = color_graph(graph, colors)
    with open(outfile, 'w') as outF:
        for (node, color) in sorted(colored_graph.items()):
            outF.write(f"{node}{color}\n")


def read_graph(fpath):
    graph = dict()
    max_node_id = 0
    for line in open(fpath, 'r'):
        nodes = [int(n) for n in line.split()]
        parent = nodes[0]
        neighbors = nodes[1:]
        graph[parent] = neighbors
        max_node_id = max(nodes)
    assert max_node_id == len(graph)
    return graph


def color_graph(graph, colors):
    """
    :param dict graph: A dictionary of nodes to neighbors
    :param list colors: A list of colors
    """
    # First, rank nodes of the graph in descending order
    # according to the number of neighbors.
    sorted_nodes = sorted(graph.keys(), key=lambda x: len(graph[x]),
                          reverse=True)

    # Then, assign to each node the first color that is not used
    # by any of its neighbors
    color_assignments = defaultdict(str)
    for node in sorted_nodes:
        neighbors = graph[node]
        neighbor_colors = [color_assignments[n] for n in neighbors]
        # color = the first color that is not in the neighboring colors
        for color in colors:
            if color not in neighbor_colors:
                break
        color_assignments[node] = color
    return color_assignments


if __name__ == "__main__":
    args = parse_args()
    main(args.infile, args.outfile)
