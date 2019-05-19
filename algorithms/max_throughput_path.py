from typing import Tuple, List

import networkx as nx

from algorithms.available_subgraph import available_subgraph
from algorithms.utils import filter_null_edges, path_with_edge


def max_throughput_path(G: nx.Graph, s: int, t: int, remove_null:bool = True, attr_name="throughput") -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with maximal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """

    if remove_null:
        G = filter_null_edges(G)

    if not nx.has_path(G, s, t):
        raise Exception("There is not path between s and t")

    G_a = nx.Graph(available_subgraph(G, s, t))

    throughput = nx.get_edge_attributes(G_a, attr_name)
    edges = sorted(G_a.edges(), key=lambda e: throughput[e])

    min_edge = None
    min_throughput = 0

    for e in edges:
        G_a.remove_edge(e[0], e[1])
        if not nx.has_path(G_a, s, t):
            min_edge = e
            min_throughput = throughput[e]
            break

    path = path_with_edge(G_a, s, t, min_edge)

    return path, min_throughput
