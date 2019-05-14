import networkx as nx

from algorithms.utils import path_from_list


def draw_weighted_graph(G: nx.Graph, edge_attr='throughput', path=None, pos=None):
    if pos is None:
        pos = nx.spring_layout(G)
    edge_cmap = ['k' for _ in G.edges()]
    if path is not None:
        P = path_from_list(path)
        edge_cmap = ['r' if e in P.edges() else 'k' for e in G.edges()]
    nx.draw(G, pos=pos, with_labels=True, edge_color=edge_cmap)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, edge_attr))
    return pos


def draw_segment_graph(G: nx.Graph, segment_color='red', art_color='green'):
    colors = list()
    articulation = nx.get_node_attributes(G, 'articulation')
    for node in G.nodes():
        colors.append(art_color if articulation[node] else segment_color)
    nx.draw(G, with_labels=True, node_color=colors)
