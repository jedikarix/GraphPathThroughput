import os
import time
import random
from typing import Tuple

from pipeline.pipeline import load_graphs
from algorithms.max_throughput_path import max_throughput_path, max_throughput_path_opt
from generator.generator import generate_complex_graph, generate_graph
from algorithms.min_throughput_path import min_throughput_path
from drawing.drawing import draw_weighted_graph
from math import pow, sqrt
import matplotlib.pyplot as plt


def save(graph, path=None, edge_attr="weight", filename="plot"):
    """
    Draw graph in file
    :param graph: graph to draw
    :param path: path to mark {min_path, max_path}
    :param edge_attr: edge attribute
    :param filename: filename
    :return: None
    """
    draw_weighted_graph(graph, path=path, edge_attr=edge_attr)
    plt.savefig(filename)
    plt.clf()


def run_unit_tests(dir, s_t_filename, min_max_cap_filename) -> bool:
    """
    Run unit tests for graphs from directory
    :param dir: graphs directory
    :param s_t_filename: file with list of source and target
    :param min_max_cap__filename: file with max and min capacity
    :return: result of unit test
    """
    s_t = []
    min_c = []
    max_c = []
    with open(s_t_filename) as file:
        for w in [line.split() for line in file]:
            s_t.append((int(w[0]), int(w[1])))

    with open(min_max_cap_filename) as file:
        for w in [line.split() for line in file]:
            min_c.append(int(w[0]))
            max_c.append(int(w[1]))

    files = [os.path.join(dir, filename) for filename in sorted(os.listdir(dir), key=lambda x: (len(x), x))]
    graphs = load_graphs(files)
    success = True

    for i, graph in enumerate(graphs):
        try:
            max_path, c = max_throughput_path(graph, s_t[i][0], s_t[i][1], attr_name='weight')
            max_c.append(c)
            if c != max_c[i]:
                success = False
                print("Test {}: max_throughput_path - not passed".format(i))
            else:
                print("Test {}: max_throughput_path - passed".format(i))
            save(graph, max_path, "weight", "plot_Max{}.png".format(i + 1))
        except Exception as e:
            print('In test ' + str(i) + ': ' + str(e))
        try:
            min_path, c = min_throughput_path(graph, s_t[i][0], s_t[i][1], attr_name="weight")
            min_c.append(c)
            if c != min_c[i]:
                success = False
                print("Test {}: min_throughput_path - not passed".format(i))
            else:
                print("Test {}: min_throughput_path - passed".format(i))
            save(graph, min_path, "weight", "plot_Min{}.png".format(i + 1))
        except Exception as e:
            print('In test ' + str(i) + ': ' + str(e))

        save(graph, edge_attr="weight", filename="plot{}.png".format(i + 1))

    return success


def run_performance_tests(graphs, num_of_pairs: int,
                          algorithm) -> Tuple[float, float]:
    """
    Run performance test of algorithm
    :param num_of_ver: number of vertices
    :param max_num_of_sub_ver: max number of vertices in subgraph
    :param num_of_rep: number of repetitions
    :param algorithm: used algorithm
    :return: average time and standard deviation
    """
    times = []
    for i in range(len(graphs)):
        for j in range(num_of_pairs):
            s, t = tuple(random.sample(range(len(graphs[i].nodes())), 2))

            start = time.time()

            algorithm(graphs[i], s=s, t=t, attr_name="weight")
            end = time.time()
            times.append(end - start)

    avrg = sum(times) / len(times)

    s = 0
    for t in times:
        s += pow((avrg - t), 2)

    return avrg, sqrt((s/len(times)))


class ExperimentGraphs:
    def __init__(self, n, nodes, segment_nodes):
        self.nodes = nodes
        self.segment_nodes = segment_nodes
        self.graphs = [None] * n
        self.n = n

    def __getitem__(self, i):
        if i < 0:
            i += self.n
        if 0 <= i < self.n:
            if self.graphs[i] is None:
                self.graphs[i] = generate_complex_graph(self.nodes, self.segment_nodes)
            return self.graphs[i]
        raise IndexError('Index out of range: {}'.format(i))

    def __len__(self):
        return self.n


def run_tests_set(ns, ss, algorithms, rep, pairs):

    results = dict()

    for n in ns:
        for s in ss:
            if s > n:
                break
            graphs = ExperimentGraphs(rep, n, s)
            for alg in algorithms:
                time = run_performance_tests(graphs, pairs, alg)
                print("nodes: {}\tsegment size:{}\talgorithm:{}\t->\ttime:{}".format(n, s, alg, time))
                results[(n, s, alg)] = time

    return results


if __name__ == "__main__":

    ns = [100, 330, 1000, 3300, 10000]
    ss = [10, 33, 100, 330, 1000, 3300, 10000]
    algorithms = [min_throughput_path, max_throughput_path, max_throughput_path_opt]
    rep = 10
    pairs = 50

    run_tests_set(ns, ss, algorithms, rep, pairs)