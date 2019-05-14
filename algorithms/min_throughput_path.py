from typing import Tuple, Dict, Set, List

import networkx as nx

from algorithms.segment_graph import segment_graph


def node_segment(node: int, segments: Dict[int, Set], art_dict: Dict[int, bool]) -> int:
    V_node = None
    print(node)
    print(segments)
    print(art_dict)
    if art_dict.get(node, False):
        V_node = node
    else:
        for seg_i, seg_set in segments.items():
            if node in seg_set:
                V_node = seg_i
                break
    return V_node


def min_throughput_path(G: nx.Graph, s: int, t: int) -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with minimal throughput
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """
    H = segment_graph(G)
    segments = nx.get_node_attributes(H, "segment")
    art_dict = nx.get_node_attributes(H, 'articulation')

    V_s = node_segment(s, segments, art_dict)
    V_t = node_segment(t, segments, art_dict)

    if V_s is None or V_t is None:
        raise Exception("Source's segment or target's segment wasn't found")

    segment_path = nx.shortest_path(H, V_s, V_t)
    print(segments)
    available_nodes = set([node for segment in segment_path if segment in segments.keys() for node in segments[segment]])

    G_a = G.subgraph(available_nodes)

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
