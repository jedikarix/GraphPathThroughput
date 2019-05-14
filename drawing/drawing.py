import networkx as nx


def draw_weighted_graph(G: nx.Graph, edge_attr='throughput'):
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, edge_attr))


def draw_segment_graph(G: nx.Graph, segment_color='red', art_color='green'):
    colors = list()
    articulation = nx.get_node_attributes(G, 'articulation')
    for node in G.nodes():
        colors.append(art_color if articulation[node] else segment_color)
    nx.draw(G, with_labels=True, node_color=colors)
