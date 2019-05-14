import networkx as nx


def draw_weighted_graph(G: nx.Graph, edge_attr='throughput'):
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, edge_attr))
