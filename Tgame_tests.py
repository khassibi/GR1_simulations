from Tgame.controller import sys_ctrl
import pickle
import hard_tests
import random
import visualization.animate as animate

import tulip as tlp
from tulip import transys, abstract, spec, synth
from IPython.display import HTML

import networkx as nx

from test_builder import *

path = 'Tgame/'

class TgameTest(Test):
    def animate_test(self, ctrl, signals, title):
        print('made it to animate')
        # signals = {'b': b_signal}
        time, states = ctrl.run('Sinit', signals)

        # Grab the location
        sys_path = states['loc']
        env_path = ['b='+str(b) for b in signals['b']]

        if len(env_path) == 101:
            title += '_Cut Short'

        # Animate the results
        anim = animate.animate_Tgame((sys_path, env_path), title)
        anim.save(path + title + '.gif')
    
    def animate_R(self, R, trajectory, title):
        # Animate the results
        ani = animate.animate_Rs(R, trajectory, title)
        ani.save(path + title + '.gif')
        # with open(path + title, 'w') as f:
        #     print(ani.to_jshtml(), file=f)

    def test_with_metric_and_prog(self, G, init_node, robustness, env_prog_dict, penalty, max_runs, length_bound=None):

        env_prog_nodes = self.get_env_prog_nodes(G, env_prog_dict)

        prog_cycles = self.get_prog_cycles(G, env_prog_dict, env_prog_nodes, length_bound=length_bound)
        with open(path + 'prog_cycles', "wb") as file:
            pickle.dump(prog_cycles, file)

        # getting the nodes in the cycles that satisfy the env progress conditions
        nodes_satisfying_prog = set()
        for lst in prog_cycles:
            nodes_satisfying_prog |= set(lst)

        R = self.calculate_winning_sets(G, nodes_satisfying_prog)
        R_ret = R
        i = len(R) - 1
        print('i:', i)
        T = [0] * len(R)

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
        while i != 0 and iter < 100:
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
            print('sys_action:', curr_num)
            trajectory.append(curr_num)

            # curr_num = random.choice(test_transitions[curr_num])
            # use the metric to find the best environment action to take
            curr_num = self.find_trans_prog(G, curr_num, R, i, T, penalty, robustness)
            print('env_action:', curr_num)
            i = self.find_R_i(curr_num, R)
            T[i] += 1
            iter += 1

        if iter >= 100:
            print("len(b_signal)", len(b_signal))
            signals = {'b': b_signal}
            return signals, trajectory, R_ret 

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
        
        signals = {'b': b_signal}
        
        return signals, trajectory, R_ret

def experiment():
    conversion = {'loc': ['c0', 'c1', 'c2', 'c3']}
    test = TgameTest(path, conversion)
    G, ctrl = test.organize_graph_and_controller()
    # test.rand_tests(G, ctrl)
    # test.no_repeat_rand_tests(G, ctrl)
    env_prog_dict = {'b': 4}
    test.run_prog_tests(G, ctrl, env_prog_dict, 0, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.25, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 0.5, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 1, 30)
    test.run_prog_tests(G, ctrl, env_prog_dict, 5, 30)

if __name__ == "__main__":
    experiment()