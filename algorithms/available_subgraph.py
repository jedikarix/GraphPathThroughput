from typing import Dict, Set, List, Tuple

import networkx as nx

from algorithms.segment_graph import segment_graph


def node_segment(node: int, segments: Dict[int, Set], art_dict: Dict[int, bool]) -> int:
    """
    Finds segment containing given node
    :param node:
    :param segments:
    :param art_dict:
    :return:
    """
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


def available_subgraph(G: nx.Graph, s: int, t: int) -> Tuple[nx.Graph, nx.Graph, List[int]]:
    """
    Computes subgraph of G using edges which can be used to build path between s and t nodes
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: supgraph of G
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
    available_nodes = set(
        [node for segment in segment_path if segment in segments.keys() for node in segments[segment]])

    return G.subgraph(available_nodes), H, segment_path
