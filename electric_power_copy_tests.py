from left_turn_pedestrian.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

import matplotlib
import matplotlib.pyplot as plt

path = 'electric_power_copy/'

def test(G, init_node, test, max_runs):
    curr_num = init_node

    # Initializing the initial state
    init_state = G.nodes[curr_num]
    GL = init_state['GL']
    GR = init_state['GR']
    AL = init_state['AL']
    AR = init_state['AR']
    
    # Initializing signals
    GL_signal = [GL]
    GR_signal = [GR]
    AL_signal = [AL]
    AR_signal = [AR]

    # Finding the transitions for the test
    test_transitions = test(G)
    
    sys_control = sys_ctrl()
    env_state = sys_ctrl.move(sys_control, GL, GR, AL, AR)
    env_state.update({'GL': GL, "GR": GR, 'AL': AL, 'AR': AR, 'shape': 'oval'})
    assert env_state == init_state, (env_state, init_state)

    curr_num = random.choice(test_transitions[curr_num])

    # Running the test
    counter = 0
    while counter < max_runs:
        sys_state = G.nodes[curr_num]
        GL = sys_state['GL']
        GR = sys_state['GR']
        AL = sys_state['AL']
        AR = sys_state['AR']

        # Keeping track of signals
        GL_signal.append(GL)
        GR_signal.append(GR)
        AL_signal.append(AL)
        AR_signal.append(AR)

        env_state = sys_ctrl.move(sys_control, GL, GR, AL, AR)
        env_state.update({'GL': GL, "GR": GR, 'AL': AL, 'AR':AR, 'shape': 'oval'})

        curr_num = list(G.nodes.values()).index(env_state)

        curr_num = random.choice(test_transitions[curr_num])
        counter += 1
    
    return GL_signal, GR_signal, AL_signal, AR_signal

def animate_test(ctrl, GL_signal, GR_signal, AL_signal, AR_signal, title):
    time, states = ctrl.run('Sinit', {'GL': GL_signal, 'GR': GR_signal, 
                                      'AL': AL_signal, 'AR': AR_signal})

    vars = ['GL', 'GR', 'AL', 'AR', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'B1', 'B2', 'B3', 'B4']
    num_figs = len(vars)
    fig, axs = plt.subplots(num_figs, sharex=True)
    # fig.suptitle('Vertically stacked subplots')
    for i in range(num_figs):
        y = states[vars[i]]
        x = list(range(len(y)))
        axs[i].step(x, y)
        # axs[i].set_title('Var' + str(i))
        axs[i].set(ylabel=vars[i])
        axs[i].label_outer()

    fig.savefig(path + title + '.png')

def experiment():
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
    # Does not seem necessary in this case

    # Removing nodes that violate the environment's safety
    unsafe_env_nodes = set()
    for node in G.nodes:
        if ((G.nodes[node]['GL'] != 1) and  (G.nodes[node]['AL'] != 1) 
        and (G.nodes[node]['AR'] != 1) and (G.nodes[node]['GR'] != 1)):
            unsafe_env_nodes.add(node)
    G.remove_nodes_from(unsafe_env_nodes)

    # env_safe = {'(GL = 1) | (AL = 1) | (GR = 1) | (AR = 1)'}

    # Relabeling the nodes in order
    nodes = list(G.nodes)
    new_labels = list(range(len(nodes)))
    mapping = dict(zip(nodes, new_labels))
    G = nx.relabel_nodes(G, mapping)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Greedy Most Red"
    GL_signal, GR_signal, AL_signal, AR_signal = test(G, 0, hard_tests.greedy_most_red, 20)
    animate_test(ctrl, GL_signal, GR_signal, AL_signal, AR_signal, title)

    # Running the test that greedily picks the next state with the most unsafe 
    # nodes
    title = "Greedy Percent Red"
    GL_signal, GR_signal, AL_signal, AR_signal = test(G, 0, hard_tests.greedy_percent_red, 20)
    animate_test(ctrl, GL_signal, GR_signal, AL_signal, AR_signal, title)

    title = "Greedy Min Robustness"
    GL_signal, GR_signal, AL_signal, AR_signal = test(G, 0, hard_tests.greedy_min_robustness, 20)
    animate_test(ctrl, GL_signal, GR_signal, AL_signal, AR_signal, title)

if __name__ == "__main__":
    experiment()