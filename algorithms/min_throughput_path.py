from typing import Tuple, List

import networkx as nx

from algorithms.available_subgraph import available_subgraph
from algorithms.utils import filter_null_edges, path_with_edge


def min_throughput_path(G: nx.Graph, s: int, t: int, attr_name="throughput") -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with minimal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """

    if not nx.has_path(G, s, t):
        raise Exception("There is not path between s and t")
    if s == t:
        raise Exception("Source and target are the same node")

    G_a, _, _ = available_subgraph(G, s, t)
    G_a = nx.Graph(G_a)

    edges = G_a.edges()
    throughputs = nx.get_edge_attributes(G_a, attr_name)

    min_edge = None
    min_throughput = float('inf')
    for e in edges:
        if throughputs[e] < min_throughput:
            min_edge = e
            min_throughput = throughputs[e]

    G_a.remove_edge(*min_edge)
    path = path_with_edge(G_a, s, t, min_edge)

    return path, min_throughput
