import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines
import simulations

import logging

from tulip import dumpsmach
import pickle

class ElectricPower(simulations.Simulation):

    def make_specs(self):

        # Variables
        env_vars = {'g1': (0,1), 'g2': (0,1), 'g3': (0,1), 'g4': (0,1),
                    'r1': (0,1), 'r2': (0,1),
                    'c1': (0,1), 'c2': (0,1), 'c3': (0,1), 'c4': (0,1),
                    'c5': (0,1), 'c6': (0,1), 'c7': (0,1), 
                    'c8': (0,1), 'c9': (0,1), 'c10': (0,1),
                    'x1': (0,2), 'x2': (0,2), 'x3': (0,2), 'x4': (0,2)}

        sys_vars = {'til_c1': (0,1), 'til_c2': (0,1), 'til_c3': (0,1), 'til_c4': (0,1),
                    'til_c5': (0,1), 'til_c6': (0,1), 'til_c7': (0,1), 
                    'til_c8': (0,1), 'til_c9': (0,1), 'til_c10': (0,1),
                    'b1': (0,1), 'b2': (0,1), 'b3': (0,1), 'b4': (0,1), 'b5': (0,1), 'b6': (0,1),
                    't1': (0,3), 't4': (0,3)}
        
        # Initialization
        env_init = {'g1=1', 'g2=1', 'g3=1', 'g4=1',
                    'r1=1', 'r2=1',
                    'c1=1', 'c2=1', 'c3=1', 'c4=1',
                    'c5=0', 'c6=0', 'c7=0', 
                    'c8=1', 'c9=1', 'c10=1',
                    'x1=0', 'x2=0', 'x3=0', 'x4=0'}

        sys_init = {'til_c1=1', 'til_c2=1', 'til_c3=1', 'til_c4=1',
                    'til_c5=0', 'til_c6=0', 'til_c7=0', 
                    'til_c8=1', 'til_c9=1', 'til_c10=1',
                    'b1=1', 'b2=1', 'b3=1', 'b4=1', 'b5=1', 'b6=1',
                    't1=0', 't4=0'}

        # Safety
        env_safe = {'(g1 = 1) | (g2 = 1) | (g3 = 1) | (g4 = 1)',
                    '(r1 = 1) | (r2 = 1)'}
        
        # Unhealthy generator remaining unhealthy
        for i in range(1,5):
            env_safe |= {'(g{0}=0) -> X(g{0})=0'.format(i)}

        # Contactor Delays
        for i in range(1,5):
            env_safe |= {'(X(c{0}) = til_c{0}) -> (X(x{0}) = 0)'.format(i),
                        '(til_c{0} = c{0}) -> (X(c{0}) = c{0})'.format(i),
                        '(c{0} != til_c{0}) -> ((X(c{0}) = til_c{0}) | (X(x{0}) = (x{0} + 1)))'.format(i),
                        'x{0} <= 2'.format(i)}
        for i in range(6,11):
            env_safe |= {'X(c{0}) = til_c{0}'.format(i)}
        
        # Unhealthy Sources
        sys_safe = set()
        neighbors = {('g1', 'til_c1'), ('g2', 'til_c2'), ('g3', 'til_c3'), ('g4', 'til_c4'),
                    ('r1', 'til_c8'), ('r2', 'til_c9')}
        for a,b in neighbors:
            sys_safe |= {'({0} = 0) -> ({1} = 0)'.format(a, b)}

        # No Parallelization of AC Sources
        env_safe |= {'!(c1=1 & c5=1 & c2=1)',
                    '!(c1=1 & c5=1 & c6=1 & c3=1)',
                    '!(c1=1 & c5=1 & c6=1 & c7=1 & c4=1)',
                    '!(c2=1 & c6=1 & c3=1)',
                    '!(c2=1 & c6=1 & c7=1 & c4=1)',
                    '!(c3=1 & c7=1 & c4=1)'}
        
        # Power Status of Buses
        top_graph = nx.Graph()
        top_graph.add_nodes_from(['g1', 'g2', 'g3', 'g4',
                    'c1', 'c2', 'c3', 'c4',
                    'c5', 'c6', 'c7',
                    'b1', 'b2', 'b3', 'b4'])
        top_graph.add_edges_from([('g1', 'c1'), ('g2', 'c2'), ('g3', 'c3'), ('g4', 'c4'),
                    ('c1', 'b1'), ('c2', 'b2'), ('c3', 'b3'), ('c4', 'b4'),
                    ('b1', 'c5'), ('c5', 'b2'), ('b2', 'c6'), ('c6', 'b3'), ('b3', 'c7'), ('c7', 'b4')])
        for b in range(1,5):
            unpowered = []
            for g in range(1,5):
                path = list(nx.all_simple_paths(top_graph,'b' + str(b), 'g' + str(g)))[0]
                path.remove('b' + str(b))
                safety = '('
                for elem in path:
                    safety += elem + '=1 & '
                safety = safety[:-3] + ')'
                unpowered.append(safety)
                safety += ' -> (b{} = 1)'.format(b)
                sys_safe |= {safety}
            sys_safe |= {'!(' + " | ".join(unpowered) + ') -> (b{} = 0)'.format(b)}
        
        bottom_graph = nx.Graph()
        bottom_graph.add_nodes_from(['b1', 'c8', 'r1', 'b5', 'c10', 'b6', 'r2', 'c9', 'b4'])
        bottom_graph.add_edges_from([('b1', 'c8'), ('c8', 'r1'), ('r1', 'b5'), ('b5', 'c10'),
                                ('c10', 'b6'), ('b6', 'r2'), ('r2', 'c9'), ('c9', 'b4')])
        for orange in [5, 6]:
            unpowered = []
            for blue in [1,4]:
                path = list(nx.all_simple_paths(bottom_graph,'b' + str(orange), 'b' + str(blue)))[0]
                path.remove('b' + str(orange))
                safety = '('
                for elem in path:
                    safety += elem + '=1 & '
                safety = safety[:-3] + ')'
                unpowered.append(safety)
                safety += ' -> (b{} = 1)'.format(orange)
                sys_safe |= {safety}
            sys_safe |= {'!(' + " | ".join(unpowered) + ') -> (b{} = 0)'.format(orange)}

        # Essential Buses
        for i in [1, 4]:
            sys_safe |= {'(b{0} = 0) -> (X(t{0}) = t{0} + 1)'.format(i),
                        '(b{0} = 1) -> (X(t{0}) = 0)'.format(i),
                        't{0} <= 3'.format(i)}
            
        # DC Buses Always Remain Powered
        sys_safe |= {'(b5 = 1) & (b6 = 1)'}

        # Progress
        env_prog = {}
        sys_prog = {}

        specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                                env_safe, sys_safe, env_prog, sys_prog)
        # Print specifications:
        # print(specs.pretty())
        #
        # Controller synthesis
        #
        # The controller decides based on current variable values only,
        # without knowing yet the next values that environment variables take.
        # A controller with this information flow is known as Moore.
        specs.moore = self.moore

        specs.plus_one = self.plus_one

        # Ask the synthesizer to find initial values for system variables
        # that, for each initial values that environment variables can
        # take and satisfy `env_init`, the initial state satisfies
        # `env_init /\ sys_init`.

        specs.qinit = self.qinit  # i.e., "there exist sys_vars: forall env_vars"

        self.specs = specs

        # self.make_strat(specs, sys, path)


if __name__ == '__main__':
    path = 'electric_power/'
    sims = []
    f2 = open(path + "errors.txt", "w")
    f = open(path + "realizable.txt", "w")
    f.write("The simulations of electric power that have a realizable controller\n")
    for plus_one in [True, False]:
        for moore in [True, False]:
            for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                run = ElectricPower(plus_one, moore, qinit)
                run.give_name('lt')
                run.make_specs()
                try:
                    run.make_strat(path)
                except:
                    run.error = True
                    f2.write(run.name + '\n')
                sims.append(run)
                if run.realizable:
                    f.write(run.name + '\n')
    f.close()
    f2.close()
