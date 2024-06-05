import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML
from pathlib import Path
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

    def test_with_metric_and_prog(self, G, init_node, robustness, env_prog_dict, penalty, max_runs, length_bound=None):
        pass

    def run_prog_tests(self, G, ctrl, env_prog_dict, penalty, max_runs, length_bound=None):
        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        # title = "Memoryless Most Red"
        # num_red_sys_metric = hard_tests.find_num_red_successors(G)
        # signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, num_red_sys_metric, 30)
        # self.animate_test(ctrl, signals, title)

        # Running the test that greedily picks the next state with the most unsafe 
        # nodes
        # title = "Memoryless Percent Red"
        # percent_red_sys_metric = hard_tests.find_percent_red_successors(G)
        # signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_max_metric, percent_red_sys_metric, 30)
        # self.animate_test(ctrl, signals, title)
        '''
        title = "Progress Min Robustness, Penalty=" + str(penalty)
        min_robustness_env_metric = hard_tests.find_min_robustness(G)
        signals, trajectory, R = self.test_with_metric_and_prog(G, 0, min_robustness_env_metric, env_prog_dict, penalty, max_runs, length_bound=length_bound)
        self.animate_test(ctrl, signals, title)
        self.animate_R(R, trajectory, "R's Min Robustness, Penalty=" + str(penalty))
        '''

        title = "Progress Average Robustness, Penalty=" + str(penalty)
        avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        signals, trajectory, R = self.test_with_metric_and_prog(G, 0, avg_robustness_env_metric, env_prog_dict, penalty, max_runs, length_bound=length_bound)
        '''
        self.animate_test(ctrl, signals, title)
        self.animate_R(R, trajectory, "R's Average Robustness, Penalty=" + str(penalty))
        '''

        # title = "Memoryless Min Robustness - Averaging"
        # # min_robustness_env_metric = hard_tests.find_min_robustness(G)
        # signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, min_robustness_env_metric, 30)
        # self.animate_test(ctrl, signals, title)

        # title = "Memoryless Average Robustness - Averaging"
        # # avg_robustness_env_metric = hard_tests.find_avg_robustness(G)
        # signals, trajectory = self.rand_test_with_metric(G, 0, hard_tests.memoryless_robustness_averaging, avg_robustness_env_metric, 30)
        # self.animate_test(ctrl, signals, title)

    def animate_test(self, ctrl, signals, title):
        pass

    def animate_R(self, R, trajectory, title):
        pass

    def removing_env_unsafe_nodes(self, G):
        return set()

    def organize_graph_and_controller(self):
        # Load the graph from the saved file
        # print(Path.cwd())
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
    
    def get_env_prog_nodes(self, G, env_prog_dict):
        # find the nodes in the graph that satisfy any of the environment's progress conditions
        # each entry in the dictionary is a list of nodes that satisfying each progress condition
        env_prog_nodes = {}
        for item in env_prog_dict.items():
            env_prog_nodes[item] = []
        for node in G.nodes:
            for item in env_prog_dict.items():
                if item in G.nodes[node].items():
                    env_prog_nodes[item].append(node)
        
        # print("env_prog_nodes:\n",env_prog_nodes)
        
        return env_prog_nodes
    
    def get_prog_cycles(self, G, env_prog_dict, env_prog_nodes, length_bound=None, path=None):
        
        # find all the simple cycles in G
        cycles = list(nx.simple_cycles(G, length_bound=length_bound)) # TAKES TOO LONG TO RUN
        # if path:
        #     pickle.dump(cycles, path)
        # print('cycles found')

        # print("cycles:", cycles)

        # make the cycles into frozensets (immutable sets)
        old_cycles = set()
        for cycle in cycles:
            old_cycles.add(frozenset(cycle))
        
        # print("old_cycles:", old_cycles)

        # removing subsets
        # new_cycles = old_cycles.copy()
        # for cycle1 in old_cycles:
        #     for cycle2 in old_cycles:
        #         if cycle1.issubset(cycle2) and cycle1 != cycle2:
        #             new_cycles.remove(cycle1)

        # Combining simple cycles together and adding those to set of cycles
        new_cycles = old_cycles.copy()
        while True:
            for cycle1 in old_cycles:
                for cycle2 in old_cycles:
                    # if not (cycle1.issubset(cycle2) or cycle2.issubset(cycle1)) and not cycle1.isdisjoint(cycle2):
                    if cycle1 != cycle2:
                        # get the intersection of the 2 nodes
                        # get the environment nodes
                        # loop over these nodes
                        # loop over succesors of environment nodes
                        # if one successor in cycle 1
                        # and another successor in cycle 2
                        # then add the union of the 2 cycles together
                        cyc_intersection = cycle1.intersection(cycle2)
                        env_intersection = [node for node in cyc_intersection if G.nodes[node]['shape'] == 'oval']
                        for env_node in env_intersection:
                            to_cycle1 = False
                            to_cycle2 = False
                            for succ in G.successors(env_node):
                                if succ in cycle1:
                                    to_cycle1 = True
                                elif succ in cycle2:
                                    to_cycle2 = True
                                if to_cycle1 and to_cycle2:
                                    break
                            if to_cycle1 and to_cycle2:
                                    new_cycles.add(frozenset(cycle1.union(cycle2)))
                                    break
            # print(len(old_cycles), len(new_cycles))
            if new_cycles == old_cycles:
                break
            else:
                old_cycles = new_cycles.copy()

        cycles = new_cycles
        # print(cycles == old_cycles)
        # print("cycles:", cycles)

        # for cycle in cycles:
        #     prnt_str = ''
        #     for node in cycle:
        #         prnt_str += str(G.nodes[node])
        #     print(prnt_str)
        #     print()

        # Filter cycles that contain nodes that satisfy each type of progress condition
        prog_satisfying_cycles = []
        for cycle in cycles:
            satisfies_prog_counter = 0
            # for env_prog_cond in env_prog_nodes.values()
            for lst in env_prog_nodes.values():
                for node in lst:
                    if node in cycle:
                        satisfies_prog_counter += 1
                        break
            # print(satisfies_prog_counter)
            if satisfies_prog_counter == len(env_prog_dict):
                prog_satisfying_cycles.append(cycle)
        
        # print("prog_satisfying_cycles:", prog_satisfying_cycles)

        # Remove any cycles with the system leaving
        no_leave_cycles = []
        for cycle in prog_satisfying_cycles:
            cycle_left = False
            for node in cycle:
                # if g0.nodes[node]['shape'] != 'oval':
                if G.nodes[node]['shape'] == 'oval':
                    continue
                # node is a node from which the system takes the action
                for succ in G.successors(node):
                    if succ not in cycle:
                        cycle_left = True
                        break
                if cycle_left:
                    break
            if not cycle_left:
                no_leave_cycles.append(cycle)
        
        # print("no_leave_cycles:", no_leave_cycles)
        
        # Take the cycles that encompass the others
        # QUESTION: is this set even necessary?
        largest_cycles = []
        for cycle in no_leave_cycles:
            is_subset = False
            for other_cycle in no_leave_cycles:
                if cycle != other_cycle and cycle.issubset(other_cycle):
                    is_subset = True
                    break
            if not is_subset:
                largest_cycles.append(cycle)
        
        # print("largest_cycles:", largest_cycles)
        
        return largest_cycles
    
    def find_R_i(self, curr_node, R):
        i = 0
        assert curr_node is not None
        while i < len(R):
            if curr_node not in R[i]:
                i += 1
            else:
                break
        # print("curr_node: ", curr_node, ", i:", i, ", len(R): ", len(R))
        assert curr_node in R[i] #, f"curr_node: {curr_node}, i: {i}, len(R): {len(R)}"
        return i
    
    def find_time_in_Ri(self, T, i):
        time_in_Ri = 0
        # Ranges from 0 to i, inclusive
        for j in range(i+1):
            time_in_Ri += T[j]
        return time_in_Ri

    def find_trans_prog(self, g, env_node, R, i, T, penalty, env_robustness):
        maximized_robustness = {}
        closer_to_R0 = {}
        # look at environment actions
        for sys_suc in list(g.successors(env_node)):
            max_rob = -1
            # look at responding system actions
            for env_suc in list(g.successors(sys_suc)):
                max_rob = max(max_rob, env_robustness[env_suc])
            # I have the maximimum robustness that can result from environment 
            # doing action sys_suc
            maximized_robustness[sys_suc] = max_rob
            # is sys_suc in the set of nodes??
            closer_to_R0[sys_suc] = int(self.find_R_i(sys_suc, R) >= i)
        
        # i that the system brought us to
        i = self.find_R_i(env_node, R)
        T[i] += 1 # added

        time_in_Ri = self.find_time_in_Ri(T, i)
        # print('i: ', i, ", time_in_Ri: ", time_in_Ri)

        metric = {}

        # look at environment actions
        for sys_suc in list(g.successors(env_node)):
            metric[sys_suc] = maximized_robustness[sys_suc] + closer_to_R0[sys_suc] * time_in_Ri * penalty
        
        # print("metric:", metric)
        
        # find the key (node) in the metric dictionary that has the minimum metric
        # min_key = min(metric, key=lambda k: metric[k])
        min_value = min(metric.values())
        min_keys = [k for k, v in metric.items() if v == min_value]
        node = random.choice(min_keys)

        return node
    
    def union_every_other(self, dictionary, i):
        big_lst = set()
        for idx in range(i % 2, i + 1, 2):
            big_lst |= set(dictionary[idx])
        return big_lst
    
    def union_upto(self, dictionary, i):
        big_lst = set()
        for idx in range(i+1):
            big_lst |= set(dictionary[idx])
        return big_lst
    
    def calculate_winning_sets(self, G, R0, possible_actions=None):
        # print("R0:", R0)
        R0_env = {node for node in R0 if G.nodes[node]['shape'] == 'box'}
        # print("R0_env:", R0_env)

        # calculate the "levels" from the env prog cycle outwards
        R = {}
        i = 0
        R[i] = R0_env
        while True:
            new_nodes = set()
            for node in R[i]:
                if possible_actions != None:
                    # Add the predecessors of the node (that are part of possible_actions) to new_nodes
                    new_nodes |= (set(G.predecessors(node)) & possible_actions)
                else:
                    # Add the predecessors of the node to new_nodes
                    new_nodes |= set(G.predecessors(node))
            # Take the union of the new_nodes & the previous set of nodes
            R[i+1] = new_nodes | R[i]

            new_nodes = set()
            # Looking at next set
            for node in R[i+1]:
                # looking at predecessors to R[i+1]
                for prev in set(G.predecessors(node)):
                    # seeing if all the transitions from these predecessors goes into R[i+1]
                    all_transitions_to_Ri1 = True
                    # looking at all actions of predecessors to this set
                    for trans in set(G.successors(prev)):
                        if trans not in R[i+1]:
                            all_transitions_to_Ri1 = False
                            break
                    if all_transitions_to_Ri1:
                        new_nodes.add(prev)
            R[i+2] = new_nodes | R[i+1]

            if R[i+2] == R[i]:
                R.pop(i+2)
                R.pop(i+1)
                break
            else:
                i += 2
        

        # can_go_up = False
        # for key, level in R.items():
        #     for node in level:
        #         for trans in set(G.successors(node)):
        #             for idx in range(key+1, len(R)+1):
        #                 if trans in R[idx]:
        #                     can_go_up = True
        #                     break
        #             if can_go_up:
        #                 break
        #         if can_go_up:
        #             break
        #     if can_go_up:
        #         break
        # assert not can_go_up

        return R
    
    # def calculate_winning_sets(self, G, R0, possible_actions=None):
    #     print("R0:", R0)
    #     R0_env = {node for node in R0 if G.nodes[node]['shape'] == 'box'}
    #     print("R0_env:", R0_env)

    #     # calculate the "levels" from the env prog cycle outwards
    #     R = {}
    #     i = 0
    #     R[i] = R0_env
    #     while True:
    #         new_nodes = set()
    #         for node in R[i]:
    #             if G.nodes[node]['shape'] == 'box':
    #                 if possible_actions != None:
    #                     # Add the predecessors of the node (that are part of possible_actions) to new_nodes
    #                     new_nodes |= (set(G.predecessors(node)) & possible_actions)
    #                 else:
    #                     # Add the predecessors of the node to new_nodes
    #                     new_nodes |= set(G.predecessors(node))
    #             else:
    #                 for prev in set(G.predecessors(node)):
    #                     # seeing if all the transitions from these predecessors goes into R[i+1]
    #                     all_transitions_to_Ri1 = True
    #                     # looking at all actions of predecessors to this set
    #                     for trans in set(G.successors(prev)):
    #                         if trans not in R[i]:
    #                             all_transitions_to_Ri1 = False
    #                             break
    #                     if all_transitions_to_Ri1:
    #                         new_nodes.add(prev)
    #         # Take the union of the new_nodes & the previous set of nodes
    #         R[i+1] = new_nodes | R[i]

    #         if R[i+1] == R[i]:
    #             R.pop(i+1)
    #             break
    #         else:
    #             i += 1
        
    #     return R
    '''
    def calculate_winning_sets(self, G, R0, possible_actions=None):
        print("R0:", R0)
        if possible_actions != None:
            R0 = (set(R0) & possible_actions)
        R0_env = {node for node in R0 if G.nodes[node]['shape'] == 'box'} # nodes from which the system makes an action
        print("R0_env:", R0_env)

        # calculate the "levels" from the env prog cycle outwards
        R = {}
        S = {}
        i = 0
        R[i] = R0_env
        S[i] = R0_env
        while True:
            env_nodes = set()
            # for node in R[i]:
            for node in S[i]:
                if G.nodes[node]['shape'] != 'box':
                    continue
                if possible_actions != None:
                    # Add the predecessors of the node (that are part of possible_actions) to new_nodes
                    env_nodes |= (set(G.predecessors(node)) & possible_actions)
                else:
                    # Add the predecessors of the node to new_nodes
                    env_nodes |= set(G.predecessors(node)) # environment nodes that lead to R[i]
            # Take the union of the new_nodes & the previous set of nodes
            # R[i+1] = env_nodes | R[i] # R[i] (sys nodes) & env nodes that can lead to R[i] (env nodes)
            R[i+1] = env_nodes
            S[i+1] = env_nodes | S[i]

            sys_nodes = set()
            # Looking at next set
            # for node in R[i+1]:
            # for env_node in env_nodes:
            for env_node in S[i+1]:
                # looking at predecessors to R[i+1]
                if G.nodes[node]['shape'] == 'box':
                    continue
                for sys_node in set(G.predecessors(env_node)):
                    # seeing if all the transitions from these predecessors goes into R[i+1]
                    all_transitions_to_Ri1 = True
                    # looking at all actions of predecessors to this set
                    for trans in set(G.successors(sys_node)):
                        # if trans not in self.union_upto(R, i+1): # QUESTION: should it be something other than R[i]??
                        if trans not in S[i+1]:
                            all_transitions_to_Ri1 = False
                            break
                    if all_transitions_to_Ri1: # but wait we don't need this for the env nodes
                        sys_nodes.add(sys_node)
            S[i+2] = sys_nodes | S[i+1]
            R[i+2] = sys_nodes

            if R[i+2] == R[i] and S[i+2] == S[i]:
                R.pop(i+2)
                R.pop(i+1)
                S.pop(i+2)
                S.pop(i+1)
                break
            # if 0 in S[i+2]:
            #     break
            else:
                i += 2
        
        return S
    '''