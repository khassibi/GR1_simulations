from left_turn_pedestrian.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

from test_builder import *

path = 'left_turn_pedestrian/'

class LeftTurnPedestrianTest(Test):
    def removing_env_unsafe_nodes(self, G):
        # Removing nodes that violate the environment's safety
        unsafe_env_nodes = set()
        for node in G.nodes:
            if G.nodes[node]['light'] == 'r':
                if (G.nodes[node]['p'] == 4 or G.nodes[node]['vh'] == 4 
                or G.nodes[node]['p'] == 5 or G.nodes[node]['vh'] == 5):
                    unsafe_env_nodes.add(node)
            if G.nodes[node]['light'] == 'y2':
                if G.nodes[node]['p'] == 4 or G.nodes[node]['vh'] == 4:
                    unsafe_env_nodes.add(node)
        return unsafe_env_nodes
    
    def animate_test(self, ctrl, signals, title):
        # signals = {'light': light_signal, 'vh': vh_signal, 'p': p_signal}
        time, states = ctrl.run('Sinit', signals)

        # Grab the location
        va_path = states['loc']
        vh_path = ['c'+str(i) for i in signals['vh']]
        p_path = ['c'+str(i) for i in signals['p']]
        light_path = signals['light']

        # Animate the results
        anim = animate.animate_intersection(light_path, (va_path, vh_path, p_path),
                                            title)
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
        vh = init_state['vh']
        p = init_state['p']
        light = init_state['light']
        
        # Initializing signals
        vh_signal = [vh]
        p_signal = [p]
        light_signal = [light]

        # Finding the transitions for the test
        test_transitions = test(G, metric)
        
        sys_control = sys_ctrl()
        env_state = sys_ctrl.move(sys_control, vh, p, light)
        env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})
        assert env_state == init_state, (env_state, init_state)

        curr_num = random.choice(test_transitions[curr_num])
        # curr_num = test_transitions[curr_num][0]

        # Running the test
        counter = 0
        visited = [curr_num]
        while counter < max_runs:
        # while env_state['a9'] == False and counter < max_runs:
            sys_state = G.nodes[curr_num]
            vh = sys_state['vh']
            p = sys_state['p']
            light = sys_state['light']

            # Keeping track of signals
            vh_signal.append(vh)
            p_signal.append(p)
            light_signal.append(light)

            env_state = sys_ctrl.move(sys_control, vh, p, light)
            env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})

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
        
        signals = {'light': light_signal, 'vh': vh_signal, 'p': p_signal}
        
        return signals, trajectory   
    
    def rand_test_with_metric(self, G, init_node, test, metric, max_runs):
        curr_num = init_node
        trajectory = [curr_num]

        # Initializing the initial state
        init_state = G.nodes[curr_num]
        vh = init_state['vh']
        p = init_state['p']
        light = init_state['light']
        
        # Initializing signals
        vh_signal = [vh]
        p_signal = [p]
        light_signal = [light]

        # Finding the transitions for the test
        test_transitions = test(G, metric)
        
        sys_control = sys_ctrl()
        env_state = sys_ctrl.move(sys_control, vh, p, light)
        env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})
        assert env_state == init_state, (env_state, init_state)

        curr_num = random.choice(test_transitions[curr_num])
        # curr_num = test_transitions[curr_num][0]

        # Running the test
        counter = 0
        while counter < max_runs:
        # while env_state['a9'] == False and counter < max_runs:
            sys_state = G.nodes[curr_num]
            vh = sys_state['vh']
            p = sys_state['p']
            light = sys_state['light']

            # Keeping track of signals
            vh_signal.append(vh)
            p_signal.append(p)
            light_signal.append(light)

            env_state = sys_ctrl.move(sys_control, vh, p, light)
            env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})

            curr_num = list(G.nodes.values()).index(env_state)
            trajectory.append(curr_num)

            curr_num = random.choice(test_transitions[curr_num])
            counter += 1
        
        signals = {'light': light_signal, 'vh': vh_signal, 'p': p_signal}
        
        return signals, trajectory
    
    # def find_R_i(self, curr_node, R):
    #     i = 0
    #     while True:
    #         if curr_node in R[i]:
    #             i += 1
    #         else:
    #             break
    #     return i
    
    # def find_time_in_Ri(self, T, i):
    #     time_in_Ri = 0
    #     for j in range(i+1):
    #         time_in_Ri += T[j]
    #     return time_in_Ri

    # def find_trans_prog(self, g, env_node, R, i, T, penalty, env_robustness):
    #     maximized_robustness = {}
    #     closer_to_R0 = {}
    #     for sys_suc in list(g.successors(env_node)):
    #         max_rob = -1
    #         for env_suc in list(g.successors(sys_suc)):
    #             max_rob = max(max_rob, env_robustness[env_suc])
    #         # I have the maximimum robustness that can result from environment 
    #         # doing action sys_suc
    #         maximized_robustness[sys_suc] = max_rob
    #         if self.find_R_i(sys_suc, R) < i:
    #             closer_to_R0[sys_suc] = 0
    #         else:
    #             closer_to_R0[sys_suc] = 1
        
    #     i = self.find_R_i(env_node, R)

    #     time_in_Ri = self.find_time_in_Ri(T, i)

    #     metric = {}

    #     for sys_suc in list(g.successors(env_node)):
    #         metric[sys_suc] = maximized_robustness[sys_suc] + closer_to_R0[sys_suc] * penalty * time_in_Ri
        
    #     min_key = min(metric, key=lambda k: metric[k])

    #     return min_key

    # def calculate_winning_sets(self, G, R0, possible_actions=None):
    #     # calculate the "levels" from the env prog cycle outwards
    #     R = {}
    #     i = 0
    #     R[i] = R0
    #     while True:
    #         new_nodes = set()
    #         for node in R[i]:
    #             if possible_actions != None:
    #                 new_nodes |= (set(G.predecessors(node)) & possible_actions)
    #             else:
    #                 new_nodes |= set(G.predecessors(node))
    #         R[i+1] = new_nodes | R[i]

    #         new_nodes = set()
    #         for node in R[i+1]:
    #             for prev in set(G.predecessors(node)):
    #                 all_transitions_to_Ri1 = True
    #                 for trans in set(G.successors(prev)):
    #                     if trans not in R[i+1]:
    #                         all_transitions_to_Ri1 = False
    #                         break
    #                 if all_transitions_to_Ri1:
    #                     new_nodes.add(prev)
    #         R[i+2] = new_nodes | R[i+1]

    #         if R[i+2] == R[i]:
    #             R.pop(i+2)
    #             R.pop(i+1)
    #             break
    #         else:
    #             i += 2
        
    #     return R
    
    # def get_env_prog_nodes(self, G, env_prog_dict):
    #     # find the nodes in the graph that satisfy any of the environment's progress conditions
    #     # each entry in the dictionary is a list of nodes that satisfying each progress condition
    #     env_prog_nodes = {}
    #     for item in env_prog_dict.items():
    #         env_prog_nodes[item] = []
    #     for node in G.nodes:
    #         for item in env_prog_dict.items():
    #             if item in G.nodes[node].items():
    #                 env_prog_nodes[item].append(node)
        
    #     return env_prog_nodes
    
    # def get_prog_cycles(self, G, env_prog_dict, env_prog_nodes):
        
    #     # find all the simple cycles in G
    #     cycles = list(nx.simple_cycles(G))

    #     # make the cycles into frozensets (immutable sets)
    #     old_cycles = set()
    #     for cycle in cycles:
    #         old_cycles.add(frozenset(cycle))

    #     num_iters = 0
    #     new_cycles = old_cycles.copy()
    #     while True:
    #         for cycle in old_cycles:
    #             for node in cycle:
    #                 for cycle2 in old_cycles:
    #                     if node in cycle2:
    #                         new_cycles.add(frozenset(cycle | cycle2))
    #         if new_cycles == old_cycles:
    #             # print('num times it took to combine cycles:', num_iters)
    #             # print(new_cycles)
    #             break
    #         else:
    #             old_cycles = new_cycles.copy()
    #         num_iters += 1
        
    #     cycles = new_cycles

    #     print("cycles:", cycles)

    #     # Filter cycles that contain nodes that satisfy each type of progress condition
    #     prog_satisfying_cycles = []
    #     for cycle in cycles:
    #         satisfies_prog_counter = 0
    #         # for env_prog_cond in env_prog_nodes.values()
    #         for lst in env_prog_nodes.values():
    #             for node in lst:
    #                 if node in cycle:
    #                     satisfies_prog_counter += 1
    #                     break
    #         print(satisfies_prog_counter)
    #         if satisfies_prog_counter == len(env_prog_dict):
    #             prog_satisfying_cycles.append(cycle)
        
    #     print("prog_satisfying_cycles:", prog_satisfying_cycles)
        
    #     # Remove any cycles with the system leaving
    #     permanent_prog_cycles = []
    #     for cycle in prog_satisfying_cycles:
    #         cycle_left = False
    #         for node in cycle:
    #             # if g0.nodes[node]['shape'] != 'oval':
    #             if G.nodes[node]['shape'] == 'oval':
    #                 continue
    #             # node is a node from which the system takes the action
    #             for succ in G.successors(node):
    #                 if succ not in cycle:
    #                     cycle_left = True
    #                     break
    #             if cycle_left:
    #                 break
    #         if not cycle_left:
    #             permanent_prog_cycles.append(cycle)
        
    #     print("permanent_prog_cycles:", permanent_prog_cycles)
        
    #     largest_cycles = []
    #     for cycle in permanent_prog_cycles:
    #         is_subset = False
    #         for other_cycle in permanent_prog_cycles:
    #             if cycle != other_cycle and cycle.issubset(other_cycle):
    #                 is_subset = True
    #                 break
    #         if not is_subset:
    #             largest_cycles.append(cycle)
        
    #     print("largest_cycles:", largest_cycles)
        
    #     return largest_cycles
    
    def test_with_metric_and_prog(self, G, init_node, robustness, env_prog_dict, penalty, max_runs, length_bound=None):

        env_prog_nodes = self.get_env_prog_nodes(G, env_prog_dict)

        prog_cycles = self.get_prog_cycles(G, env_prog_dict, env_prog_nodes, length_bound=length_bound)

        # getting the nodes in the cycles that satisfy the env progress conditions
        nodes_satisfying_prog = set()
        for lst in prog_cycles:
            nodes_satisfying_prog |= set(lst)

        R = self.calculate_winning_sets(G, nodes_satisfying_prog)
        R_ret = R

        i = len(R) - 1
        print('i:', i)
        # assert init_node in R[i]

        T = [0] * len(R)

        # time_in_Ri = 1 # or 0?

        curr_num = init_node
        trajectory = [curr_num]

        # Initializing the initial state
        init_state = G.nodes[curr_num]
        vh = init_state['vh']
        p = init_state['p']
        light = init_state['light']
        
        # Initializing signals
        vh_signal = [vh]
        p_signal = [p]
        light_signal = [light]

        # Finding the transitions for the test
        # test_transitions = test(G, metric)
        
        sys_control = sys_ctrl()
        env_state = sys_ctrl.move(sys_control, vh, p, light)
        env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})
        assert env_state == init_state, (env_state, init_state)

        # use the metric to find the best environment action to take
        curr_num = self.find_trans_prog(G, curr_num, R, i, T, penalty, robustness)
        i = self.find_R_i(curr_num, R)
        print('i:', i, ', curr_num:', curr_num)
        print('R[i]:', R[i])
        T[i] += 1
        # curr_num = random.choice(test_transitions[curr_num])
        # curr_num = test_transitions[curr_num][0]

        # Running the test
        # while counter < max_runs:
        # while env_state['a9'] == False and counter < max_runs:
        print('before while loop')
        iter = 0
        while i != 0:
            print('iter:', iter, ', i:', i)
            # Update the current state, given the environment's action 
            sys_state = G.nodes[curr_num]
            vh = sys_state['vh']
            p = sys_state['p']
            light = sys_state['light']

            # Keeping track of signals
            vh_signal.append(vh)
            p_signal.append(p)
            light_signal.append(light)

            # Find the system's responding action
            env_state = sys_ctrl.move(sys_control, vh, p, light)
            env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})

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
                    vh = sys_state['vh']
                    p = sys_state['p']
                    light = sys_state['light']

                    # Keeping track of signals
                    vh_signal.append(vh)
                    p_signal.append(p)
                    light_signal.append(light)

                    # Find the system's responding action
                    env_state = sys_ctrl.move(sys_control, vh, p, light)
                    env_state.update({'vh': vh, "p": p, 'light': light, 'shape': 'oval'})

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
        
        signals = {'light': light_signal, 'vh': vh_signal, 'p': p_signal}
        
        return signals, trajectory, R_ret

def experiment():
    conversion = {'light': ['g1', 'g2', 'g3', 'y1', 'y2', 'r'], 
                  'loc': ['c4', 'c7', 'c8', 'c9']}
    test = LeftTurnPedestrianTest(path, conversion)
    G, ctrl = test.organize_graph_and_controller()
    # test.rand_tests(G, ctrl)
    # test.no_repeat_rand_tests(G, ctrl)
    env_prog_dict = {'vh': 6, 'p': 6, 'light': 'g1'}
    test.run_prog_tests(G, ctrl, env_prog_dict, 0, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.25, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.5, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 1, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 5, 30)

if __name__ == "__main__":
    experiment()