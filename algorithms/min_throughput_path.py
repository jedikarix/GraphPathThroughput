from typing import Tuple, List

import networkx as nx

from algorithms.available_subgraph import available_subgraph
from algorithms.utils import filter_null_edges


def min_throughput_path(G: nx.Graph, s: int, t: int, remove_null:bool = True, attr_name="throughput") -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with minimal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """

    if remove_null:
        G = filter_null_edges(G)

    if not nx.has_path(G, s, t):
        raise Exception("There is not path between s and t")

    G_a = available_subgraph(G, s, t)

    edges = G_a.edges()
    throughputs = nx.get_edge_attributes(G_a, attr_name)
    print(throughputs)
    min_edge = None
    min_throughput = float('inf')
    for e in edges:
        if throughputs[e] < min_throughput:
            min_edge = e
            min_throughput = throughputs[e]

    path_a = nx.shortest_path(G, s, min_edge[0])
    path_b = nx.shortest_path(G, min_edge[1], t)

    return path_a + path_b, min_throughput
