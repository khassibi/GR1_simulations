from left_turn.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

path = 'left_turn/'

def no_repeat_rand_tests(G, ctrl):
    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Most Red - No Repeat"
    num_red_sys_metric = hard_tests.find_num_red_successors(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Percent Red - No Repeat"
    percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Min Robustness - Minimizing - No Repeat"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Average Robustness - Minimizing - No Repeat"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Min Robustness - Averaging - No Repeat"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Average Robustness - Averaging - No Repeat"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    vh_signal, light_signal, trajectory = no_repeat_rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)


def no_repeat_rand_test_with_metric(G, init_node, test, metric, max_runs):
    curr_num = init_node
    trajectory = [curr_num]

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    vh = init_state['vh']
    light = init_state['light']
    
    # Initializing signals
    vh_signal = [vh]
    light_signal = [light]

    # Finding the transitions for the test
    test_transitions = test(G, metric)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, vh, light)
    env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])
    # curr_num = test_transitions[curr_num][0]

    # Running the test
    counter = 0
    visited = [curr_num]
    while env_state['a9'] == False and counter < max_runs:
        sys_state = G.nodes[curr_num]
        vh = sys_state['vh']
        light = sys_state['light']

        # Keeping track of signals
        vh_signal.append(vh)
        light_signal.append(light)

        env_state = sys_ctrl.move(sys_control, vh, light)
        env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})

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
        counter += 1
    
    return vh_signal, light_signal, trajectory

def no_repeat_test(G, init_node, test, max_runs):
    curr_num = init_node

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    vh = init_state['vh']
    light = init_state['light']
    
    # Initializing signals
    vh_signal = [vh]
    light_signal = [light]

    # Finding the transitions for the test
    test_transitions = test(G)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, vh, light)
    env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])

    # Running the test
    counter = 0
    visited = [curr_num]
    while env_state['a9'] == False and counter < max_runs:
        sys_state = G.nodes[curr_num]
        # Finding the cycle that led to the node
        # if sys_state in visited:
        #     last_idx = len(visited) - visited[::-1].index(sys_state) - 1
        #     cycle = visited[last_idx:]
        visited.append(sys_state)
        # Taking the environment variable assignments from the system state
        vh = sys_state['vh']
        light = sys_state['light']

        # Keeping track of signals
        vh_signal.append(vh)
        light_signal.append(light)

        # The system takes its action
        env_state = sys_ctrl.move(sys_control, vh, light)
        # Adding the environment action to the env_state dictionary
        env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)

        # Choosing the next state to go to
        unvisited_next = set(test_transitions[curr_num]) - set(visited)
        if len(unvisited_next) == 0:
            curr_num = random.choice(test_transitions[curr_num])
        else:
            curr_num = random.choice(list(unvisited_next))
        visited.append(curr_num)
        counter += 1
    
    return vh_signal, light_signal

def test(G, init_node, test, max_runs):
    curr_num = init_node

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    vh = init_state['vh']
    light = init_state['light']
    
    # Initializing signals
    vh_signal = [vh]
    light_signal = [light]

    # Finding the transitions for the test
    test_transitions = test(G)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, vh, light)
    env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])

    # Running the test
    counter = 0
    while env_state['a9'] == False and counter < max_runs:
        sys_state = G.nodes[curr_num]
        vh = sys_state['vh']
        light = sys_state['light']

        # Keeping track of signals
        vh_signal.append(vh)
        light_signal.append(light)

        env_state = sys_ctrl.move(sys_control, vh, light)
        env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)

        curr_num = random.choice(test_transitions[curr_num])
        counter += 1
    
    return vh_signal, light_signal

def rand_tests(G, ctrl):
    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Most Red"
    num_red_sys_metric = hard_tests.find_num_red_successors(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Memoryless Percent Red"
    percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Min Robustness - Minimizing"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, min_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Average Robustness - Minimizing"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_minimization, avg_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Min Robustness - Averaging"
    min_robustness_env_metric = hard_tests.find_min_robustness(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Memoryless Average Robustness - Averaging"
    avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
    vh_signal, light_signal, trajectory = rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
    animate_test(ctrl, vh_signal, light_signal, title)

def rand_test_with_metric(G, init_node, test, metric, max_runs):
    curr_num = init_node
    trajectory = [curr_num]

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    vh = init_state['vh']
    light = init_state['light']
    
    # Initializing signals
    vh_signal = [vh]
    light_signal = [light]

    # Finding the transitions for the test
    test_transitions = test(G, metric)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, vh, light)
    env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])
    # curr_num = test_transitions[curr_num][0]

    # Running the test
    counter = 0
    while env_state['a9'] == False and counter < max_runs:
        sys_state = G.nodes[curr_num]
        vh = sys_state['vh']
        light = sys_state['light']

        # Keeping track of signals
        vh_signal.append(vh)
        light_signal.append(light)

        env_state = sys_ctrl.move(sys_control, vh, light)
        env_state.update({'vh': vh, 'light': light, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)
        trajectory.append(curr_num)

        curr_num = random.choice(test_transitions[curr_num])
        counter += 1

    return vh_signal, light_signal, trajectory

def animate_test(ctrl, vh_signal, light_signal, title):
    time, states = ctrl.run('Sinit', {'light': light_signal, 'vh': vh_signal})

    # Grab the location
    va_path = states['loc']
    vh_path = ['c'+str(i) for i in vh_signal]
    light_path = light_signal

    # Animate the results
    anim = animate.animate_intersection(light_path, (va_path, vh_path), title)
    anim.save(path + title + '.gif')

def organize_graph_and_controller():
    # Load the graph from the saved file
    with open(path + 'graph', "rb") as file:
        G = pickle.load(file)

    # Load the system controller from the saved file
    with open(path + "ctrl", "rb") as file:
        ctrl = pickle.load(file)
    
    # Conversions
    light_conversion = ['g1', 'g2', 'g3', 'y1', 'y2', 'r']
    loc_conversion = ['c4', 'c7', 'c8', 'c9']
    for node in G.nodes:
        G.nodes[node]['loc'] = loc_conversion[G.nodes[node]['loc']]
        G.nodes[node]['light'] = light_conversion[G.nodes[node]['light']]
    
    # Removing nodes that violate the environment's safety
    unsafe_env_nodes = set()
    for node in G.nodes:
        if G.nodes[node]['light'] == 'r':
            if (G.nodes[node]['vh'] == 4 or G.nodes[node]['vh'] == 5):
                unsafe_env_nodes.add(node)
        if G.nodes[node]['light'] == 'y':
            if G.nodes[node]['vh'] == 4:
                unsafe_env_nodes.add(node)
    G.remove_nodes_from(unsafe_env_nodes)

    # Relabeling the nodes in order
    nodes = list(G.nodes)
    new_labels = list(range(len(nodes)))
    mapping = dict(zip(nodes, new_labels))
    G = nx.relabel_nodes(G, mapping)

    # # Running the test that greedily picks the next state with the most unsafe 
    # # nodes
    # title = "Greedy Most Red - No Repeat"
    # vh_signal, light_signal = no_repeat_test(G, 0, hard_tests.greedy_most_red, 20)
    # animate_test(ctrl, vh_signal, light_signal, title)

    # # Running the test that greedily picks the next state with the most unsafe 
    # # nodes
    # title = "Greedy Percent Red - No Repeat"
    # vh_signal, light_signal = no_repeat_test(G, 0, hard_tests.greedy_percent_red, 20)
    # animate_test(ctrl, vh_signal, light_signal, title)

    # title = "Greedy Min Robustness - No Repeat"
    # vh_signal, light_signal = no_repeat_test(G, 0, hard_tests.greedy_min_robustness, 20)
    # animate_test(ctrl, vh_signal, light_signal, title)

    # title = "BFS Most Red - No Repeat"
    # vh_signal, light_signal = no_repeat_test(G, 0, hard_tests.BFS_most_red, 20)
    # animate_test(ctrl, vh_signal, light_signal, title)

    # title = "BFS Percent Red - No Repeat"
    # vh_signal, light_signal = no_repeat_test(G, 0, hard_tests.BFS_percent_red, 20)
    # animate_test(ctrl, vh_signal, light_signal, title)

    return G, ctrl

def experiment():
    G, ctrl = organize_graph_and_controller()
    # no_repeat_rand_tests(G, ctrl)
    rand_tests(G, ctrl)

if __name__ == "__main__":
    experiment()