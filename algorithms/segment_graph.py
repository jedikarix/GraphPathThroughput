from typing import Dict

import networkx as nx


def build_dfs_tree(G: nx.Graph, root=None) -> nx.DiGraph:
    if root is None:
        root = list(G.nodes())[0]
    depth = dict()
    T = nx.DiGraph()
    nodes = [root]
    T.add_node(root)
    depth[root] = 0
    while len(nodes) != 0:
        curr = nodes.pop()
        children = [v for v in G.neighbors(curr) if not T.has_node(v)]
        nodes += children
        for child in children:
            T.add_edge(curr, child)
            depth[child] = depth[curr] + 1
    nx.set_node_attributes(T, depth, "depth")
    return T


def low(G: nx.Graph) -> Dict[int, int]:
    pass


def segment_graph(G: nx.Graph) -> nx.Graph:
    pass
