from left_turn.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

from test_builder import *

path = 'left_turn/'

class LeftTurnTest(Test):
    def removing_env_unsafe_nodes(self, G):
        # Removing nodes that violate the environment's safety
        unsafe_env_nodes = set()
        for node in G.nodes:
            if G.nodes[node]['light'] == 'r':
                if (G.nodes[node]['vh'] == 4 or G.nodes[node]['vh'] == 5):
                    unsafe_env_nodes.add(node)
            if G.nodes[node]['light'] == 'y2':
                if G.nodes[node]['vh'] == 4:
                    unsafe_env_nodes.add(node)
        return unsafe_env_nodes
    
    def animate_test(self, ctrl, signals, title):
        # signals = {'light': light_signal, 'vh': vh_signal}
        time, states = ctrl.run('Sinit', signals)

        # Grab the location
        va_path = states['loc']
        vh_path = ['c'+str(i) for i in signals['vh']]
        light_path = signals['light']

        # Animate the results
        anim = animate.animate_intersection(light_path, (va_path, vh_path), title)
        anim.save(path + title + '.gif')
    
    def no_repeat_rand_test_with_metric(self, G, init_node, test, metric, max_runs):
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

        signals = {'light': light_signal, 'vh': vh_signal}
        
        return signals, trajectory
    
    def rand_test_with_metric(self, G, init_node, test, metric, max_runs):
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

        signals = {'light': light_signal, 'vh': vh_signal}

        return signals, trajectory

def experiment():
    conversion = {'light': ['g1', 'g2', 'g3', 'y1', 'y2', 'r'], 
                  'loc': ['c4', 'c7', 'c8', 'c9']}
    test = LeftTurnTest(path, conversion)
    G, ctrl = test.organize_graph_and_controller()

    # env_prog_dict = {'vh': 6, 'light': 0}
    env_prog_dict = {'vh': 6, 'light': 'g1'}
    # env_prog_nodes = test.get_env_prog_nodes(G, env_prog_dict)
    # prog_cycles = test.get_prog_cycles(G, env_prog_dict, env_prog_nodes)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.5, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.25, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 1, 30)

    # test.rand_tests(G, ctrl)
    # test.no_repeat_rand_tests(G, ctrl)

if __name__ == "__main__":
    experiment()