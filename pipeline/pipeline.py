from typing import List, Union, Tuple
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


def pipeline(graphs_list: Union[List[Union[str, nx.Graph]], str] = None) -> None:
    if isinstance(graphs_list, str):
        graphs = load_graphs_from_file(graphs_list)
    elif isinstance(graphs_list, List):
        graphs = load_graphs(graphs_list)
    else:
        raise Exception("graphs_list should be filename or list")
    graphs = load_graphs(graphs)
    results = run_algorithm(graphs)
    process_results(results)
    pass


def run_algorithm(graphs: List[nx.Graph]) -> List[Tuple[float, List[int], int]]:
    return list()


def process_results(results):
    pass
