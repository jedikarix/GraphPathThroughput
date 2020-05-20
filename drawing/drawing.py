import networkx as nx

from algorithms.utils import path_from_list
from algorithms.available_subgraph import available_subgraph


def draw_weighted_graph(G: nx.Graph, edge_attr='throughput', path=None, pos=None):
    """
    Draw graph with weight on edges
    :param G: graph
    :param edge_attr: attribute name
    :param path: path in graph to mark
    :param pos: position of nodes
    :return: generated position of nodes
    """
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
    """
    Draw G segment graph
    :param G:
    :param segment_color:
    :param art_color:
    :return:
    """
    colors = list()
    articulation = nx.get_node_attributes(G, 'articulation')
    for node in G.nodes():
        colors.append(art_color if articulation[node] else segment_color)
    nx.draw(G, with_labels=True, node_color=colors)


def draw_available_subgraph(G: nx.Graph, s: int, t: int, remove_rest: bool = False, pos=None):
    """
    Draw available subgraph of G for path from s to t.
    :param G: graph
    :param s: source node
    :param t: target node
    :param remove_rest: if True draw whole G graph with marked subgraph, otherwise draw only subgraph
    :param pos: nodes position
    :return:
    """
    if pos is None:
        pos = nx.spring_layout(G)
    H = available_subgraph(G, s, t)
    if remove_rest:
        draw_weighted_graph(H, pos)
    else:
        nodes_colors = ['red' if H.has_node(v) else 'green' for v in G.nodes()]
        edges_color = ['red' if H.has_edge(e[0], e[1]) else 'black' for e in G.edges()]
        nx.draw(G, pos=pos, with_labels=True, edge_color=edges_color, node_color=nodes_colors)
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, 'throughput'))
    return pos
