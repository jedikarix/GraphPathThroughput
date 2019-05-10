from typing import List, Union, Tuple
import networkx as nx


def load_graphs_list(filename: str) -> List[nx.Graph]:
    return list()


def load_graphs(graphs: List[Union[str, nx.Graph]]) -> List[nx.Graph]:
    return list()


def pipeline(graphs: List[Union[str, nx.Graph]]) -> None:
    graphs = load_graphs(graphs)
    results = run_algorithm(graphs)
    process_results(results)
    pass


def run_algorithm(graphs: List[nx.Graph]) -> List[Tuple[float, List[int], int]]:
    return list()


def process_results(results):
    pass
