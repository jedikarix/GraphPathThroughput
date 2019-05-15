import networkx as nx

from algorithms.utils import low


def segment_graph(G: nx.Graph) -> nx.Graph:
    """
    Generate graph of segments of G. Segments are linked with articulation points
    :param G: base Graph
    :return: graph H with segments and articulation points from G
    """
    segments = list()
    art_points = set()
    curr_seg = 0
    max_seg = 0
    root = list(G.nodes())[0]
    v_low, T = low(G, root)
    depth = nx.get_node_attributes(T, 'depth')
    v_seg = dict()
    for v in list(G.nodes()):
        v_seg[v] = list()

    if len(list(T.neighbors(root))) >= 0:
        art_points.add(root)
        for child in list(T.neighbors(root)):
            max_seg += 1
            segments.append(set())

            v_seg[root].append(max_seg-1)
            segments[max_seg-1].add(root)

            v_seg[child].append(max_seg-1)
            segments[max_seg-1].add(child)
    else:
        v_seg[root] = [curr_seg]
        segments[curr_seg].add(root)

    v_stack = list(T.neighbors(root))

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

                v_seg[curr].append(max_seg-1)
                segments[max_seg-1].add(curr)

                v_seg[child].append(max_seg-1)
                segments[max_seg-1].add(child)
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
    H.add_nodes_from(list(art_points), articulation=True)
    H.add_nodes_from(list(segments_dict.keys()), articulation=False)
    H.add_edges_from(E)

    nx.set_node_attributes(H, segments_dict, 'segment')

    return H
