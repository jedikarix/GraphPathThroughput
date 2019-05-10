import time
from typing import List, Union, Tuple, Generator, Callable, Any

import networkx as nx


def load_graphs_from_file(filename: str) -> List[nx.Graph]:
    with open(filename) as file:
        graphs_filenames = file.readlines()
    return [nx.read_edgelist(graph_filename) for graph_filename in graphs_filenames]


def load_graphs(graphs: List[Union[str, nx.Graph]]) -> List[nx.Graph]:
    loaded_graphs = list()
    for graph in graphs:
        if isinstance(graph, str):
            graph = nx.read_edgelist(graph)
        loaded_graphs.append(graph)
    return loaded_graphs


def pipeline(graphs_list: Union[Generator, List[Union[str, nx.Graph]], str],
             algorithm: Callable[[nx.Graph], Any]) -> None:
    if isinstance(graphs_list, str):
        graphs = load_graphs_from_file(graphs_list)
    elif isinstance(graphs_list, List):
        graphs = load_graphs(graphs_list)
    elif isinstance(graphs_list, Generator):
        graphs = graphs_list
    else:
        raise Exception("graphs_list should be filename or list")
    results = run_algorithm(graphs, algorithm)
    process_results(results)
    pass


def run_algorithm(graphs: Union[Generator, List[nx.Graph]],
                  algorithm: Callable[[nx.Graph], Any]) -> List[Tuple[float, Any]]:
    results = list()
    for graph in graphs:
        t0 = time.clock()
        alg_result = algorithm(graph)
        dt = time.clock() - t0
        results.append((dt, alg_result))
    return results


def process_results(results):
    pass
