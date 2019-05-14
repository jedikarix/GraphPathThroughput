from typing import Dict, List, Tuple

import networkx as nx


def build_dfs_tree(G: nx.Graph, root=None) -> nx.DiGraph:
    """
    Build DFS tree based on given graph. Add to result graph's nodes attribute with node's depth in tree.
    :param G: Graph for building tree.
    :param root: root node. If unspecified, algorithm take first node from nodes list as root.
    :return: Oriented tree with depth assigned to nodes.
    """
    if root is None:
        root = list(G.nodes())[0]
    depth = dict()
    T = nx.DiGraph()
    track = [root]
    T.add_node(root)
    depth[root] = 0
    while len(track) != 0:
        curr = track[-1]
        child_candidates = [v for v in G.neighbors(curr) if not T.has_node(v)]
        if len(child_candidates) == 0:
            track.pop()
        else:
            child = child_candidates[0]
            track.append(child)
            T.add_node(child)
            T.add_edge(curr, child)
            depth[child] = depth[curr] + 1
    nx.set_node_attributes(T, depth, "depth")
    return T


def low(G: nx.Graph, root) -> Tuple[Dict[int, int], nx.Graph]:
    """
    Calculate low function values for graph nodes.
    :param G: input Graph
    :param root: root node
    :return: tuple (low_map, tree) with dictionary mapping nodes to low function values and tree used in computations
    """
    low_map = dict()

    T = build_dfs_tree(G, root)
    depth = nx.get_node_attributes(T, "depth")
    T_nodes = sorted(list(T.nodes()), reverse=True, key=lambda v: depth[v])
    T_ud = T.to_undirected()
    G_secondary = nx.difference(G, T_ud)

    for v in T_nodes:
        v_children_low = [low_map[w] for w in T.neighbors(v)]
        v_sec_dep = [depth[w] for w in G_secondary.neighbors(v)]
        v_dep = depth[v]
        low_map[v] = min(v_children_low + v_sec_dep + [v_dep])

    return low_map, T


def path_from_list(node_list: List[int]) -> nx.Graph():
    P = nx.Graph()
    P.add_nodes_from(node_list)
    edges = [(i, j) for i, j in zip(node_list[:-1], node_list[1:])]
    P.add_edges_from(edges)
    return P
