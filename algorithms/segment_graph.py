from typing import Dict, Tuple

import networkx as nx


def build_dfs_tree(G: nx.Graph, root=None) -> nx.DiGraph:
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


def segment_graph(G: nx.Graph) -> nx.Graph:
    segments = list([set()])
    art_points = set()
    curr_seg = 0
    max_seg = 0
    root = list(G.nodes())[0]
    v_low, T = low(G, root)
    depth = nx.get_node_attributes(T, 'depth')
    v_stack = [root]
    v_seg = dict()
    for v in list(G.nodes()):
        v_seg[v] = list()

    v_seg[root] = [curr_seg]
    segments[curr_seg].add(root)

    if len(list(T.neighbors(root))) >= 0:
        art_points.add(root)

    while len(v_stack) > 0:
        curr = v_stack.pop()
        curr_seg = v_seg[curr][0]
        children = list(T.neighbors(curr))
        v_stack = v_stack + children
        for child in children:
            if v_low[child] >= depth[curr]:
                art_points.add(curr)
                max_seg += 1
                segments.append(set())

                v_seg[curr].append(max_seg)
                segments[max_seg].add(curr)

                v_seg[child].append(max_seg)
                segments[max_seg].add(child)
            else:
                v_seg[child].append(curr_seg)
                segments[curr_seg].add(child)

    segments_dict = dict()
    for i, segment in enumerate(segments):
        segments_dict[i + max(G.nodes()) + 1] = segment

    E = list()
    for a in art_points:
        for segment_label in segments_dict.keys():
            if a in segments_dict[segment_label]:
                E.append((a, segment_label))

    H = nx.Graph()
    H.add_nodes_from(list(art_points) + list(segments_dict.keys()))
    H.add_edges_from(E)
    nx.set_node_attributes(H, segments_dict, 'segment')
    return H
