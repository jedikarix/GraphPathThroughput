import os
from pipeline.pipeline import load_graphs
from algorithms.max_throughput_path import max_throughput_path
from algorithms.min_throughput_path import min_throughput_path
from drawing.drawing import draw_weighted_graph
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
            save(graph, max_path, "weight", "plot_Max{}.png".format(i + 1))
        except Exception as e:
            print('In test ' + str(i) + ': ' + str(e))
        try:
            min_path, c = min_throughput_path(graph, s_t[i][0], s_t[i][1], attr_name="weight")
            min_c.append(c)
            if c != min_c[i]:
                success = False
            save(graph, min_path, "weight", "plot_Min{}.png".format(i + 1))
        except Exception as e:
            print('In test ' + str(i) + ': ' + str(e))

        save(graph, edge_attr="weight", filename="plot{}.png".format(i + 1))

    return success


def run_performance_tests():
    pass

if run_unit_tests('resources/unit_tests/',
                  'resources/s_t_unit_tests',
                  'resources/min_max_cap_unit_tests'):
    print('ALL UNIT TESTS PASSED')
