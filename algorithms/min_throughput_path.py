from typing import Tuple, Dict, Set, List

import networkx as nx

from algorithms.available_subgraph import available_subgraph


def min_throughput_path(G: nx.Graph, s: int, t: int) -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with minimal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """
    G_a = available_subgraph(G, s, t)

    edges = G_a.edges()
    throughputs = nx.get_edge_attributes(G_a, "throughput")
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
