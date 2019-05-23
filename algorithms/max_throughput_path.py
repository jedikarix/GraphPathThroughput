from typing import Tuple, List, Dict

import networkx as nx

from algorithms.available_subgraph import available_subgraph
from algorithms.utils import filter_null_edges, path_with_edge


def max_throughput_path(G: nx.Graph, s: int, t: int, attr_name="throughput") -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with maximal throughput
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


def segments_gates(path: List[int], segments: Dict[int, List[int]], art_points: List[int], s:int , t: int) -> List[Tuple[int, int]]:
    """
    Determines entrance and exit nodes in every segment on segments path
    :param path: segments path. List of segments' indices.
    :param segments: mapping segments on list of nodes in these segments
    :param art_points: list of articulation points in graph
    :return: list of pairs (entrance, exit) for every segment in path
    """
    seg_art_points = [set(art_points).intersection(segments[segment]) for segment in path]

    if len(path) == 1:
        return [(s, t)]

    entrance = s
    exit = list(seg_art_points[0].intersection(seg_art_points[1]))[0]

    gates = [(entrance, exit)]

    for i in range(1, len(path) - 1):
        entrance = exit
        exit = list(seg_art_points[i].intersection(seg_art_points[i+1]))[0]
        gates.append((entrance, exit))

    gates.append((exit, t))
    return gates


def edges_segments(G: nx.Graph, segments: Dict[int, List[int]], path: List[int]) -> Dict[Tuple[int, int], int]:
    """
    Determines segment for every edge in graph
    :param G:
    :param segments:
    :param path:
    :return:
    """
    edge_seg = dict()
    for i, segment in enumerate(path):
        G_sub = G.subgraph(list(segments[segment]))
        edges = G_sub.edges()
        edge_seg.update([(edge, i) for edge in edges])
    return edge_seg


def max_throughput_path_opt(G: nx.Graph, s: int, t: int,
                            remove_null:bool = False, attr_name="throughput") -> Tuple[List[int], int]:
    """
    Finds path between s and t nodes with maximal throughput. Using optimization for checking
    connection between source and target.
    :param G: input graph
    :param s: source node
    :param t: target node
    :return: tuple (path, throughput)
    """

    if remove_null:
        G = filter_null_edges(G)

    if not nx.has_path(G, s, t):
        raise Exception("There is not path between s and t")
    if s == t:
        raise Exception("Source and target are the same node")

    G_a, H, seg_path = available_subgraph(G, s, t)

    segments = nx.get_node_attributes(H, "segment")
    art_points_H = nx.get_node_attributes(H, "articulation")

    art_points = [node for node in G_a.nodes() if art_points_H.get(node, False)]
    seg_path = [seg for seg in seg_path if seg in segments.keys()]

    G_a = nx.Graph(G_a)

    throughput = nx.get_edge_attributes(G_a, attr_name)
    edges = sorted(G_a.edges(), key=lambda e: throughput[e])

    e_seg = edges_segments(G_a, segments, seg_path)
    seg_gates = segments_gates(seg_path, segments, art_points, s, t)

    min_edge = None
    min_throughput = 0

    for e in edges:
        G_a.remove_edge(*e)
        seg = e_seg.get(e, None)
        if seg is None:
            seg = e_seg[(e[1], e[0])]
        gates = seg_gates[seg]
        if not nx.has_path(G_a, gates[0], gates[1]):
            min_edge = e
            min_throughput = throughput[e]
            break

    path = path_with_edge(G_a, s, t, min_edge)

    return path, min_throughput
