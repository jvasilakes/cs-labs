import string
import argparse
from collections import defaultdict

"""
Top-down coloring algorithm.
1. Assume an ordered list of colors, encoded as uppercase ASCII characters.
2. Assume a graph with integer node IDs.
3. Rank nodes of the graph by their number of neighbors, in descending order.
    a. Ties give priority to lower node ID.
4. For each node
    a. Assign the node the first color in the list of colors that is not
       used by the node's neighbors
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str,
                        help="Path to file containing graph definition")
    parser.add_argument("outfile", type=str,
                        help="Where to write the graph coloring.")
    return parser.parse_args()


def main(infile, outfile):
    """
    Read the graph from infile, color it, and write it to outfile.

    :param str infile: The graph data file.
    :param str outfile: Where to save the colored graph.
    """
    graph = read_graph(infile)
    colors = list(string.ascii_uppercase)
    colored_graph = color_graph(graph, colors)
    with open(outfile, 'w') as outF:
        for (node, color) in sorted(colored_graph.items()):
            outF.write(f"{node}{color}\n")


def read_graph(fpath):
    """
    Read the graph data in fpath into a dict

    :param str fpath: The path to the graph data file.
    :returns: The graph where each key is a node and
              each value is a list of its neighbors.
    :rtype: dict
    """
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
    Color the graph using the specified colors.

    :param dict graph: A dictionary of nodes to neighbors
    :param list colors: A list of colors
    :returns: Dictionary of node: color assignments
    :rtype: dict
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
