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
    
    def animate_R(self, R, trajectory, title):
        # Animate the results
        anim = animate.animate_Rs(R, trajectory, title)
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
        
    def test_with_metric_and_prog(self, G, init_node, robustness, env_prog_dict, penalty, max_runs, length_bound=None):
        env_prog_nodes = self.get_env_prog_nodes(G, env_prog_dict)

        prog_cycles = self.get_prog_cycles(G, env_prog_dict, env_prog_nodes, length_bound)

        # getting the nodes in the cycles that satisfy the env progress conditions
        nodes_satisfying_prog = set()
        for lst in prog_cycles:
            nodes_satisfying_prog |= set(lst)

        R = self.calculate_winning_sets(G, nodes_satisfying_prog)
        R_ret = R

        i = len(R) - 1
        print('i:', i)
        assert init_node in R[i]

        T = [0] * len(R)

        # time_in_Ri = 1 # or 0?

        curr_num = init_node
        trajectory = [curr_num]

        # Initializing the initial state
        init_state = G.nodes[curr_num]
        b = init_state['b']

        # Initializing signals
        b_signal = [b]

        sys_control = sys_ctrl()
        env_state = sys_ctrl.move(sys_control, b)
        env_state.update({'b': b, 'shape': 'oval'})
        assert env_state == init_state, (env_state, init_state)

        # use the metric to find the best environment action to take
        curr_num = self.find_trans_prog(G, curr_num, R, i, T, penalty, robustness)
        i = self.find_R_i(curr_num, R)
        print('i:', i, ', curr_num:', curr_num)
        print('R[i]:', R[i])
        T[i] += 1

        # Running the test
        print('before while loop')
        iter = 0
        while i != 0:
            print('iter:', iter, ', i:', i)
            # Update the current state, given the environment's action 
            sys_state = G.nodes[curr_num]
            b = sys_state['b']

            # Keeping track of signals
            b_signal.append(b)

            # Find the system's responding action
            env_state = sys_ctrl.move(sys_control, b)
            env_state.update({'b': b, 'shape': 'oval'})

            # Get the node corresponding to the system's action
            curr_num = list(G.nodes.values()).index(env_state)
            trajectory.append(curr_num)

            # curr_num = random.choice(test_transitions[curr_num])
            # use the metric to find the best environment action to take
            curr_num = self.find_trans_prog(G, curr_num, R, i, T, penalty, robustness)
            i = self.find_R_i(curr_num, R)
            T[i] += 1
            iter += 1
        
        # CODE ABOUT GOING THROUGH PROGRESS NODES CONTINUOUSLY
        # find the cycle we are in
        cycle = []
        for c in prog_cycles:
            if curr_num in c:
                cycle = c
                break
        print('cycle:', cycle)

        counter = 0
        num_times_satisfying_prog = 0
        # while counter < max_runs:
        while counter < max_runs and num_times_satisfying_prog < 2:
            # print('counter:', counter)
            # prog_counter = 0
            for prog_cond_nodes in env_prog_nodes.values():
                # prog_counter += 1
                if counter >= max_runs:
                    break
                R = self.calculate_winning_sets(G, set(prog_cond_nodes), set(cycle))
                T = [0] * len(R)
                i = self.find_R_i(curr_num, R)
                # print(prog_counter, i)
                T[i] += 1
                
                while i != 0:
                    if counter >= max_runs:
                        break
                    # Update the current state, given the environment's action 
                    sys_state = G.nodes[curr_num]
                    b = sys_state['b']

                    # Keeping track of signals
                    b_signal.append(b)

                    # Find the system's responding action
                    env_state = sys_ctrl.move(sys_control, b)
                    env_state.update({'b': b, 'shape': 'oval'})

                    # Get the node corresponding to the system's action
                    curr_num = list(G.nodes.values()).index(env_state)
                    trajectory.append(curr_num)

                    # curr_num = random.choice(test_transitions[curr_num])
                    # use the metric to find the best environment action to take
                    curr_num = self.find_trans_prog(G, curr_num, R, i, T, penalty, robustness)
                    i = self.find_R_i(curr_num, R)
                    T[i] += 1
                    counter += 1
            print("num_times_satisfying_prog:", num_times_satisfying_prog)
            num_times_satisfying_prog += 1
        
        signals = {'b': b}
        
        return signals, trajectory, R_ret
        

def experiment():
    conversion = {'r': ['c00', 'c01', 'c02', 'c03', 'c04', 'c10', 'c11', 'c12', 
                        'c13', 'c14', 'c20', 'c21', 'c22', 'c23', 'c24', 'c30', 
                        'c31', 'c32', 'c33', 'c34', 'c40', 'c41', 'c42', 'c43', 
                        'c44']}
    test = PatrollingCarTest(path, conversion)
    G, ctrl = test.organize_graph_and_controller()

    env_prog_dict = {'b': 0}
    # print('before')
    # env_prog_nodes = test.get_env_prog_nodes(G, env_prog_dict)
    # print('middle')
    # prog_cycles = []
    # length_bound = 0
    # while len(prog_cycles) == 0:
    #     length_bound += 1
    #     prog_cycles = test.get_prog_cycles(G, env_prog_dict, env_prog_nodes, length_bound, '/Users/kimiahassibi/Desktop/Caltech/SURF2023/GR1_simulations/patrolling_car/cycles')
    # print(length_bound) # it is 4
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.5, 30, length_bound=4)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.25, 30, length_bound=4)
    test.run_prog_tests(G, ctrl, env_prog_dict, 1, 30, length_bound=4)
    test.run_prog_tests(G, ctrl, env_prog_dict, 5, 30, length_bound=4)


    # test.rand_tests(G, ctrl)
    # test.no_repeat_rand_tests(G, ctrl)

if __name__ == "__main__":
    experiment()
