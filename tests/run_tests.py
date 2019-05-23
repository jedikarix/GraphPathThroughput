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


def run_performance_tests(num_of_ver: int, max_num_of_sub_ver: int, num_of_rep, algorithm) -> Tuple[float, float]:
    """
    Run performance test of algorithm
    :param num_of_ver: number of vertices
    :param max_num_of_sub_ver: max number of vertices in subgraph
    :param num_of_rep: number of repetitions
    :param algorithm: used algorithm
    :return: average time and standard deviation
    """
    times = []
    for i in range(num_of_rep):
        graph = generate_complex_graph(num_of_ver, max_num_of_sub_ver)
        start = time.time()
        algorithm(graph, s=random.randint(1, num_of_ver), t=random.randint(1, num_of_ver), attr_name="weight")
        end = time.time()
        times.append(start - end)

    avrg = sum(times) / num_of_rep
    s = 0
    for t in times:
        s += pow((avrg - t), 2)

    return avrg, sqrt((s/num_of_rep))


if __name__ == "__main__":
    if run_unit_tests('resources/unit_tests/',
                      'resources/s_t_unit_tests',
                      'resources/min_max_cap_unit_tests'):
        print('ALL UNIT TESTS PASSED')

    t1 = run_performance_tests(1000, 20, 1, min_throughput_path)
    t2 = run_performance_tests(1000, 20, 1, max_throughput_path)
    t3 = run_performance_tests(1000, 20, 1, max_throughput_path_opt)
    print('wynik: ' + str(t1[0]) + ' ' + str(t1[1]))
    print('wynik: ' + str(t2[0]) + ' ' + str(t2[1]))
    print('wynik: ' + str(t3[0]) + ' ' + str(t3[1]))
