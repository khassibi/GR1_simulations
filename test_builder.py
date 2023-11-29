import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

class Test:
    def __init__(self, path, conversion):
        self.path = path
        self.conversion = conversion # key is the variable name and value is a list of conversions

    def no_repeat_rand_tests(self, G, ctrl):
        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        title = "Memoryless Most Red - No Repeat"
        num_red_sys_metric = hard_tests.find_num_red_successors(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
        self.animate_test(ctrl, signal, title)

        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        title = "Memoryless Percent Red - No Repeat"
        percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
        self.animate_test(ctrl, signal, title)

        title = "Memoryless Min Robustness - Minimizing - No Repeat"
        min_robustness_env_metric = hard_tests.find_min_robustness(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
        self.animate_test(ctrl, signal, title)

        title = "Memoryless Average Robustness - Minimizing - No Repeat"
        avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
        self.animate_test(ctrl, signal, title)

        title = "Memoryless Min Robustness - Averaging - No Repeat"
        # min_robustness_env_metric = hard_tests.find_min_robustness(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
        self.animate_test(ctrl, signal, title)

        title = "Memoryless Average Robustness - Averaging - No Repeat"
        # avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        signal, trajectory = self.no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
        self.animate_test(ctrl, signal, title)


    def no_repeat_rand_test_with_metric(self, G, init_node, test, metric, max_runs):
        pass

    def rand_tests(self, G, ctrl):
        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        title = "Memoryless Most Red"
        num_red_sys_metric = hard_tests.find_num_red_successors(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
        self.animate_test(ctrl, signals, title)

        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        title = "Memoryless Percent Red"
        percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
        self.animate_test(ctrl, signals, title)

        title = "Memoryless Min Robustness - Minimizing"
        min_robustness_env_metric = hard_tests.find_min_robustness(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
        self.animate_test(ctrl, signals, title)

        title = "Memoryless Average Robustness - Minimizing"
        avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
        self.animate_test(ctrl, signals, title)

        title = "Memoryless Min Robustness - Averaging"
        # min_robustness_env_metric = hard_tests.find_min_robustness(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
        self.animate_test(ctrl, signals, title)

        title = "Memoryless Average Robustness - Averaging"
        # avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
        self.animate_test(ctrl, signals, title)

    def rand_test_with_metric(self, G, init_node, test, metric, max_runs):
        pass

    def animate_test(self, ctrl, signals, title):
        pass

    def removing_env_unsafe_nodes(self, G):
        return set()

    def organize_graph_and_controller(self):
        # Load the graph from the saved file
        with open(self.path + 'graph', "rb") as file:
            G = pickle.load(file)

        # Load the system controller from the saved file
        with open(self.path + "ctrl", "rb") as file:
            ctrl = pickle.load(file)
        
        # Conversions
        for node in G.nodes:
            for key, value in self.conversion.items():
                G.nodes[node][key] = value[G.nodes[node][key]]

        # Removing nodes that violate the environment's safety
        unsafe_env_nodes = self.removing_env_unsafe_nodes(G)
        G.remove_nodes_from(unsafe_env_nodes)

        # Relabeling the nodes in order
        nodes = list(G.nodes)
        new_labels = list(range(len(nodes)))
        mapping = dict(zip(nodes, new_labels))
        G = nx.relabel_nodes(G, mapping)

        return G, ctrl