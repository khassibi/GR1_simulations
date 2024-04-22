from patrolling_car.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

from test_builder import *

path = 'patrolling_car/'


class PatrollingCarTest(Test):
    def animate_test(self, ctrl, signals, title):    
        # signals = {'b': b_signal}
        time, states = ctrl.run('Sinit', signals)

        car_path = states['r']
        fuel_path = states['fuel']
        b_conversion = ['c10', 'c11', 'c12', 'c13', 'c14']
        b_path = [b_conversion[b] for b in signals['b']]

        # Animate the results
        anim = animate.animate_pat_car(fuel_path, (car_path, b_path), title, fuel_path[0])
        anim.save(path + title + '.gif')    
    
    def no_repeat_rand_test_with_metric(self, G, init_node, test, metric, max_runs):
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

            # curr_num = random.choice(test_transitions[curr_num])
            # Choosing the next state to go to
            unvisited_next = set(test_transitions[curr_num]) - set(visited)
            if len(unvisited_next) == 0:
                curr_num = random.choice(test_transitions[curr_num])
            else:
                curr_num = random.choice(list(unvisited_next))
            # curr_num = random.choice(test_transitions[curr_num])
            visited.append(curr_num)
            counter += 1
        
        signals = {'b': b_signal}

        return signals, trajectory
    
    def rand_test_with_metric(self, G, init_node, test, metric, max_runs):
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
        
        signals = {'b': b_signal}

        return signals, trajectory
        

def experiment():
    conversion = {'r': ['c00', 'c01', 'c02', 'c03', 'c04', 'c10', 'c11', 'c12', 
                        'c13', 'c14', 'c20', 'c21', 'c22', 'c23', 'c24', 'c30', 
                        'c31', 'c32', 'c33', 'c34', 'c40', 'c41', 'c42', 'c43', 
                        'c44']}
    test = PatrollingCarTest(path, conversion)
    G, ctrl = test.organize_graph_and_controller()

    env_prog_dict = {'b': 0}
    print('before')
    env_prog_nodes = test.get_env_prog_nodes(G, env_prog_dict)
    print('middle')
    prog_cycles = test.get_prog_cycles(G, env_prog_dict, env_prog_nodes, '/Users/kimiahassibi/Desktop/Caltech/SURF2023/GR1_simulations/patrolling_car/cycles')

    # test.rand_tests(G, ctrl)
    # test.no_repeat_rand_tests(G, ctrl)

if __name__ == "__main__":
    experiment()
