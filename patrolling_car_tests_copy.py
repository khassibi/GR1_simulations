from patrolling_car_copy.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

path = 'patrolling_car_copy/'

def no_repeat_rand_tests(G, ctrl):
    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Most Red - No Repeat"
    num_red_sys_metric = hard_tests.find_num_red_successors(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
    animate_test(ctrl, b_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Percent Red - No Repeat"
    percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Min Robustness - Minimizing - No Repeat"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Average Robustness - Minimizing - No Repeat"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Min Robustness - Averaging - No Repeat"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Average Robustness - Averaging - No Repeat"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    b_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

def no_repeat_rand_test_with_metric(G, init_node, test, metric, max_runs):
    curr_num = init_node
    trajectory = [curr_num]

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    b = init_state['b']
    
    # Initializing signals
    b_signal = [b]

    # Finding the transitions for the test
    test_transitions = test(G, metric)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, b)
    env_state.update({'b': b, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])
    # curr_num = test_transitions[curr_num][0]

    # Running the test
    counter = 0
    visited = [curr_num]
    while env_state['r'] != 'c04' and counter < max_runs:
        sys_state = G.nodes[curr_num]
        b = sys_state['b']

        # Keeping track of signals
        b_signal.append(b)

        env_state = sys_ctrl.move(sys_control, b)
        env_state.update({'b': b, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)
        trajectory.append(curr_num)

        # Choosing the next state to go to
        unvisited_next = set(test_transitions[curr_num]) - set(visited)
        if len(unvisited_next) == 0:
            curr_num = random.choice(test_transitions[curr_num])
        else:
            curr_num = random.choice(list(unvisited_next))
        # curr_num = random.choice(test_transitions[curr_num])
        visited.append(curr_num)
        # curr_num = random.choice(test_transitions[curr_num])
        counter += 1
    
    return b_signal, trajectory

def rand_tests(G, ctrl):
    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Most Red"
    num_red_sys_metric = hard_tests.find_num_red_successors(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
    animate_test(ctrl, b_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Percent Red"
    percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Min Robustness - Minimizing"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Average Robustness - Minimizing"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Min Robustness - Averaging"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

    title = "Memoryless Average Robustness - Averaging"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    b_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
    animate_test(ctrl, b_signal, title)

def rand_test_with_metric(G, init_node, test, metric, max_runs):
    curr_num = init_node
    trajectory = [curr_num]

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    b = init_state['b']
    
    # Initializing signals
    b_signal = [b]

    # Finding the transitions for the test
    test_transitions = test(G, metric)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, b)
    env_state.update({'b': b, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])
    # curr_num = test_transitions[curr_num][0]

    # Running the test
    counter = 0
    while env_state['r'] != 'c04' and counter < max_runs:
        sys_state = G.nodes[curr_num]
        b = sys_state['b']

        # Keeping track of signals
        b_signal.append(b)

        env_state = sys_ctrl.move(sys_control, b)
        env_state.update({'b': b, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)
        trajectory.append(curr_num)

        curr_num = random.choice(test_transitions[curr_num])
        counter += 1
    
    return b_signal, trajectory

def animate_test(ctrl, b_signal, title):
    time, states = ctrl.run('Sinit', {'b': b_signal})

    car_path = states['r']
    fuel_path = states['fuel']
    b_conversion = ['c10', 'c11', 'c12', 'c13', 'c14']
    b_path = [b_conversion[b] for b in b_signal]

    # Animate the results
    anim = animate.animate_pat_car_copy(fuel_path, (car_path, b_path), title)
    anim.save(path + title + '.gif')

def organize_graph_and_controller():
    # Load the graph from the saved file
    with open(path + 'graph', "rb") as file:
        G = pickle.load(file)

    # Load the system controller from the saved file
    with open(path + "ctrl", "rb") as file:
        ctrl = pickle.load(file)
    
    # Labeling the nodes like system nodes
    for edge in ctrl.edges:
        for (key, val) in ctrl.edges[edge].items():
            ctrl.nodes[edge[1]][key] = val
    
    # Conversions
    r_conversion = ['c00', 'c01', 'c02', 'c03', 'c04', 'c10', 'c11', 'c12', 'c13', 'c14', 'c20', 'c21', 'c22', 'c23', 'c24', 'c30', 'c31', 'c32', 'c33', 'c34', 'c40', 'c41', 'c42', 'c43', 'c44'] # TODO: Double check this conversion
    for node in G.nodes:
        G.nodes[node]['r'] = r_conversion[G.nodes[node]['r']]

    # Relabeling the nodes in order
    nodes = list(G.nodes)
    new_labels = list(range(len(nodes)))
    mapping = dict(zip(nodes, new_labels))
    G = nx.relabel_nodes(G, mapping)

    return G, ctrl

def experiment():
    G, ctrl = organize_graph_and_controller()
    no_repeat_rand_tests(G, ctrl)

    
if __name__ == "__main__":
    experiment()

