import os
from pipeline.pipeline import load_graphs
from algorithms.max_throughput_path import max_throughput_path
from algorithms.min_throughput_path import min_throughput_path
from drawing.drawing import draw_weighted_graph
import matplotlib.pyplot as plt


def run_unit_tests(dir):

    s_t = [(1, 2), (1, 2), (1, 2), (1, 2), (1, 2),
           (1, 2), (1, 2), (1, 2), (1, 2), (1, 2),
           (1, 2), (1, 2), (1, 2), (1, 2), (1, 2),
           (1, 2), (1, 2), (1, 2), (1, 2), (1, 2),
           (1, 2), (1, 2), (1, 2), (1, 2), (1, 2),
           (1, 2), (1, 2)]

    files = [os.path.join(dir, filename) for filename in sorted(os.listdir(dir))]
    graphs = load_graphs(files)
    for i, graph in enumerate(graphs):
        print(list(graph.nodes()))
        max_path, _ = max_throughput_path(graph, s_t[i][0], s_t[i][1], attr_name="weight", remove_null=False)
        draw_weighted_graph(graph, path=max_path, edge_attr="weight")
        plt.savefig("plot_Max{}.png".format(i))
        plt.clf()

        min_path, _ = min_throughput_path(graph, s_t[i][0], s_t[i][1], attr_name="weight", remove_null=False)
        draw_weighted_graph(graph, path=min_path, edge_attr="weight")
        plt.savefig("plot_Min{}.png".format(i))
        plt.clf()

        draw_weighted_graph(graph, edge_attr="weight")
        plt.savefig("plot_{}.png".format(i), edge_attr="weight")
        plt.clf()

