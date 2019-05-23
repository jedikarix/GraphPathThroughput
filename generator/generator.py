import networkx as nx
import random

from typing import List, Tuple


def generate_graph(num_of_ver: int, num_of_edg: int,
                   min_weight: int = 1, max_weight: int = 10) -> nx.Graph:
    """
    Generate graph
    :param num_of_ver: number of vertices
    :param num_of_edg: number of edges
    :param min_weight: min weight of edge
    :param max_weight: max weight of edge
    :return: new created graph
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(1, num_of_ver + 1))

    all_edges = generate_all_edges(num_of_ver)
    graph_edges = random.sample(all_edges, num_of_edg)

    weight_edges = list()
    for ge in graph_edges:
        weight_edges.append((ge[0], ge[1], random.randint(min_weight, max_weight)))

    graph.add_weighted_edges_from(weight_edges)
    return graph


def save_graph(graph: nx.Graph, filename : str) -> None:
    """
    Save graph into file using format readable by pipeline.load_graphs_from_file()
    :param graph: graph to save
    :param filename: name of file
    :return: None
    """
    with open(filename, 'w+') as file:
        for (u, v, wt) in graph.edges.data('weight'):
            if wt:
                file.write(str(u) + ' ' + str(v) + ' {\'weight\' : ' + str(wt) + '}\n')
    return


def generate_all_edges(num_of_ver : int, index : int = 0) -> List[Tuple[int, int]]:
    """
    Generate all possible edges for a graph with very number of vertices
    :param num_of_ver: number of vertices
    :param index: index of shift
    :return: list of possible edges
    """
    edges = list()
    for a in range(index + 1, num_of_ver + 1 + index):
        r = range(a + 1, num_of_ver + 1 + index)
        for b in r:
            edges.append((a, b))

    return edges


def generate_complex_graph(n_v: int, max_num_of_sub_ver: int, min_weight: int = 1, max_weight: int = 10000) -> nx.Graph:
    """
    Generate complex graph
    :param n_v: number of nodes
    :param max_num_of_sub_ver: max number of vertices in subgraph
    :param min_weight: min weight of edge
    :param max_weight: max weight of edge
    :return: new created graph
    """
    num_of_sub_ver = max_num_of_sub_ver
    graph = nx.complete_graph(num_of_sub_ver)

    num_of_ver = num_of_sub_ver

    while num_of_ver < n_v:
        num_of_sub_ver = random.randint(5, max_num_of_sub_ver)

        # subgraph = nx.connected_watts_strogatz_graph(num_of_sub_ver, min(5, num_of_sub_ver - 1), 1.0)
        subgraph = nx.barabasi_albert_graph(num_of_sub_ver, 4)

        graph = nx.disjoint_union(graph, subgraph)

        rand = random.randint(0, num_of_ver - 1)
        nx.relabel_nodes(graph, dict([(max(graph.nodes()), rand)]), copy=False)
        # graph.add_edge(random.randint(0, num_of_ver - 1), random.randint(num_of_ver, num_of_ver + num_of_sub_ver - 1))

        num_of_ver += num_of_sub_ver - 1

    for e in graph.edges():
        graph[e[0]][e[1]]['weight'] = random.randint(min_weight, max_weight)

    return graph


def complex_generator_wrapper(ns: List[int], max_num_of_sub_ver: int, max_weight: int):
    for n in ns:
        yield generate_complex_graph(n, max_num_of_sub_ver, max_weight=max_weight)
