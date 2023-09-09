import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines

import logging

from tulip import dumpsmach
import pickle

path = 'left_turn/'

class LeftTurn:

    def make_specs(self):
        sys = tlp.transys.FTS()

        sys.atomic_propositions.add_from({'a4', 'a7', 'a8', 'a9'})
        sys.states.add('c4', ap={'a4'})
        sys.states.add('c7', ap={'a7'})
        sys.states.add('c8', ap={'a8'})
        sys.states.add('c9', ap={'a9'})
        sys.states.initial.add('c7') 

        sys.transitions.add_comb({'c7'}, {'c7', 'c8'})
        sys.transitions.add_comb({'c8'}, {'c8', 'c4'})
        ## Add remaining state transitions
        sys.transitions.add_comb({'c4'}, {'c4', 'c9'})
        sys.transitions.add_comb({'c9'}, {'c9'})


        # Variables
        env_vars = {'vh': (2, 6), 'light': ["g1", "g2", "g3", "y1", "y2", "r"]}
        # sys_vars = {'a': (1,4)}
        sys_vars = {}

        # Initialization
        env_init = {'vh = 2', 'light = "g1"'}
        # sys_init = {'a = 1'}
        sys_init = {}

        # Safety
        env_safe = {
            # Vehicle h movement
            'vh = 2 -> X(vh=2 || vh=3)',
            'vh = 3 -> X(vh=3 || vh=4)',
            'vh = 4 -> X(vh=4 || vh=5)',
            'vh = 5 -> X(vh=5 || vh=6)',
            'vh = 6 -> X(vh=6)',
            # Traffic light
            'light = "g1" -> next(light = "g2")',
            'light = "g2" -> next(light = "g3")',
            'light = "g3" -> next(light = "y1")',
            'light = "y1" -> next(light = "y2")',
            'light = "y2" -> next(light = "r")',
            # 'light = "r" -> next(light = "r") | next(light = "g1")',
            # No running reds
            '!(light = "r" & (vh=4 || vh=5))'
        }

        sys_safe = {
            # Autonomous vehicle movement
            # 'a = 1 -> X((a=1) || (a=2))',
            # 'a = 2 -> X((a=2) || (a=3))',
            # 'a = 3 -> X((a=3) || (a=4))',
            # 'a = 4 -> X(a=4)',
            # No collisions
            # 'vh = 4 -> !(a=3)',
            'vh = 4 -> !(a4)',
            # No running reds
            # '!(light = "r" & (a=3 || a=2))'
            '!(light = "r" & (a8 || a4))'
        }
        if self.primed:
            # sys_safe |= {'!(X(vh=4) & (a=3))'}
            sys_safe |= {'!(X(vh=4) & (a4))'}

        # Progress
        env_prog = {'vh = 6'}
        # sys_prog = {'a = 4'}
        sys_prog = {'a9'}

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
        self.sys = sys

        # self.make_strat(specs, sys, path)


if __name__ == '__main__':
    simulations = []
    f2 = open(path + "visited.txt", "w")
    f = open(path + "errored_runs.txt", "w")
    f.write("The simulations of left turn that have a realizable controller\n\n")
    for aug in [True, False]:
        for primed in [True, False]:
            for plus_one in [True, False]:
                for moore in [True, False]:
                    for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                        lt = LeftTurn(aug,  primed, plus_one, moore, qinit)
                        lt.give_name()
                        f2.write(lt.name + '\n')
                        try:
                            lt.make_specs()
                        except:
                            lt.realizable = False
                            lt.error = True
                        if self.
                        simulations.append(lt)
                        # if lt.realizable:
                        #     f.write(lt.name)
                        if lt.error:
                            f.write('\n')
                            f.write(lt.name)
    f.close()
    f2.close()
    
    with open(path + 'simulations', 'wb') as file:
        pickle.dump(simulations, file)