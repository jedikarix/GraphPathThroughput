import networkx as nx
import random

from typing import List, Tuple


def generate_graph(num_of_ver: int, num_of_edg: int,
                   min_weight: int = 1, max_weight: int = 10) -> nx.Graph:
    """
    Generate graph
    :param num_of_ver: number of vertices
    :param num_of_edg: numver of edges
    :param min_weight: min weight of edge
    :param max_weight: max weight of edge
    :return: new created graph
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(1, num_of_ver + 1))

    all_edges = generate_all_edges(num_of_ver)
    graph_edges = random.sample(all_edges, num_of_edg)

    weight_edges = list()
    for ge in graph_edges:
        weight_edges.append((ge[0], ge[1], random.randint(min_weight, max_weight)))

    graph.add_weighted_edges_from(weight_edges)
    return graph


def save_graph(graph: nx.Graph, filename : str) -> None:
    """
    Save graph into file using format readable by pipeline.load_graphs_from_file()
    :param graph: graph to save
    :param filename: name of file
    :return: None
    """
    with open(filename, 'w+') as file:
        for (u, v, wt) in graph.edges.data('weight'):
            if wt:
                file.write(str(u) + ' ' + str(v) + ' {\'weight\' : ' + str(wt) + '}\n')
    return


def generate_all_edges(num_of_ver : int) -> List[Tuple[int, int]]:
    """
    Generate all possible edges for a graph with very number of vertices
    :param num_of_ver: number of vertices
    :return: list of possible edges
    """
    edges = list()
    for a in range(1, num_of_ver + 1):
        for b in range(a + 1, num_of_ver + 1):
            edges.append((a, b))
    return edges