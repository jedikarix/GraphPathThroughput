from typing import Tuple, List

import networkx as nx

from algorithms.available_subgraph import available_subgraph


def max_throughput_path(G: nx.Graph, s: int, t: int) -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with maximal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """
    G_a = nx.Graph(available_subgraph(G, s, t))

    throughput = nx.get_edge_attributes(G_a, 'throughput')
    edges = sorted(G_a.edges(), key=lambda e: throughput[e])

    min_edge = None
    min_throughput = 0

    for e in edges:
        G_a.remove_edge(e[0], e[1])
        if not nx.has_path(G_a, s, t):
            min_edge = e
            min_throughput = throughput[e]
            break

    path_a = nx.shortest_path(G, s, min_edge[0])
    path_b = nx.shortest_path(G, min_edge[1], t)

    return path_a + path_b, min_throughput
