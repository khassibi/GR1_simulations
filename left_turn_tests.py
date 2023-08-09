from left_turn.controller import sys_ctrl
import pickle
import hardest_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

path = 'left_turn/'

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

def animate_test(ctrl, vh_signal, light_signal, title):
    time, states = ctrl.run('Sinit', {'light': light_signal, 'vh': vh_signal})

    # Grab the location
    va_path = states['loc']
    vh_path = ['c'+str(i) for i in vh_signal]
    light_path = light_signal

    # Animate the results
    anim = animate.animate_intersection(light_path, (va_path, vh_path), title)
    anim.save(path + title + '.gif')

def experiment():
    # Load the graph from the saved file
    with open(path + 'graph', "rb") as file:
        G = pickle.load(file)

    # Load the system controller from the saved file
    with open(path + "ctrl", "rb") as file:
        ctrl = pickle.load(file)
    
    # Conversions
    light_conversion = ["g", "y", "r"]
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

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Greedy Most Red"
    vh_signal, light_signal = test(G, 0, hardest_tests.greedy_most_red, 20)
    animate_test(ctrl, vh_signal, light_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Greedy Percent Red"
    vh_signal, light_signal = test(G, 0, hardest_tests.greedy_percent_red, 20)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "Greedy Min Robustness"
    vh_signal, light_signal = test(G, 0, hardest_tests.greedy_min_robustness, 20)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "BFS Most Red"
    vh_signal, light_signal = test(G, 0, hardest_tests.BFS_most_red, 20)
    animate_test(ctrl, vh_signal, light_signal, title)

    title = "BFS Percent Red"
    vh_signal, light_signal = test(G, 0, hardest_tests.BFS_percent_red, 20)
    animate_test(ctrl, vh_signal, light_signal, title)


if __name__ == "__main__":
    experiment()