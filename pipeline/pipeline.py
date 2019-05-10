import time
from typing import Any, Callable, Generator, List, Tuple, Union

import networkx as nx


def load_graphs_from_file(filename: str) -> List[nx.Graph]:
    """
    Loads graphs from files listed in file specified in argument
    :param filename: path to file with list of files containing graphs to load
    :return: loaded list of graphs
    """
    with open(filename) as file:
        graphs_filenames = file.read().splitlines()
    return [nx.read_edgelist(graph_filename) for graph_filename in graphs_filenames]


def load_graphs(graphs: List[Union[str, nx.Graph]]) -> List[nx.Graph]:
    """
    Processes list of graphs. When string occured, load graphs from file defined by this string.
    :param graphs: List of graphs or filenames
    :return: loaded list of graphs
    """
    loaded_graphs = list()
    for graph in graphs:
        if isinstance(graph, str):
            graph = nx.read_edgelist(graph)
        loaded_graphs.append(graph)
    return loaded_graphs


def pipeline(graphs_list: Union[Generator, List[Union[str, nx.Graph]], str],
             algorithm: Callable[[nx.Graph], Any],
             expected_results: List[Any] = None,
             verifying_function: Callable[[Any, Any], bool] = None) -> None:
    """
    Main pipeline of application. Answers for experiments execution. Loads data, collect algorithm testing results and
     put it for results processing function.
    :param graphs_list: contains one of
        - path to file with list of graphs
        - list of graphs and paths to files with graphs
        - graphs generator
    :param algorithm: Tested algorithm function. Should take nx.Graph as argument
    :param expected_results: list with expected algorithm result for consecutive graphs from graphs_list
    :param verifying_function: function determining result correctness if desired_result provided
    """
    if isinstance(graphs_list, str):
        graphs = load_graphs_from_file(graphs_list)
    elif isinstance(graphs_list, List):
        graphs = load_graphs(graphs_list)
    elif isinstance(graphs_list, Generator):
        graphs = graphs_list
    else:
        raise Exception("graphs_list should be filename or list")
    results = run_algorithm(graphs, algorithm)
    process_results(results, expected_results=expected_results, verifying_function=verifying_function)


def run_algorithm(graphs: Union[Generator, List[nx.Graph]],
                  algorithm: Callable[[nx.Graph], Any]) -> List[Tuple[float, Any]]:
    """
    Calls algorithm from graphs from list or generator. Measures execution time.
    :param graphs: List of graphs or graphs generator
    :param algorithm: Tested algorithm function. Should take nx.Graph as argument
    :return: list with tuples containing time execution and result for particular graphs
    """
    results = list()
    for graph in graphs:
        t0 = time.clock()
        alg_result = algorithm(graph)
        dt = time.clock() - t0
        results.append((dt, alg_result))
    return results


def process_results(results: List[Tuple[float, Any]], print_results=True,
                    expected_results: List[Any] = None,
                    verifying_function: Callable[[Any, Any], bool] = None):
    """
    Processes experiments results. Check tested algorithm's output correctness. Print experiments log
    :param results: List with results produced in experiments
    :param print_results: Print results if True
    :param expected_results: list of expected output for every graph
    :param verifying_function: function comparing output with expected result. '==' is used if None.
    :return: list with success value for every graph.
    """
    if expected_results is not None:
        if len(results) != len(expected_results):
            raise Exception("Length of results and expected_results must be equal")
        if verifying_function is None:
            def verifying_function(x, y):
                return x == y
        print(results)
        print(expected_results)
        success_list = [verifying_function(result[1], expected) for result, expected in zip(results, expected_results)]
    else:
        success_list = [None] * len(results)

    if print_results:
        for result, expected, success in zip(results, expected_results, success_list):
            print('time: {}\tout: {}\texpected: {}\tsuccess: {}'.format(result[0], result[1], expected, success))

    return success_list
