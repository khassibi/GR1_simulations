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

class LeftTurn(simulations.Simulation):

    def make_specs(self):

        # System definition
        sys = tlp.transys.FTS()

        sys.atomic_propositions.add_from({'a4', 'a7', 'a8', 'a9'})
        sys.states.add('c4', ap={'a4'})
        sys.states.add('c7', ap={'a7'})
        sys.states.add('c8', ap={'a8'})
        sys.states.add('c9', ap={'a9'})
        sys.states.initial.add('c7')    # start in state c7

        sys.transitions.add_comb({'c7'}, {'c7', 'c8'})
        sys.transitions.add_comb({'c8'}, {'c8', 'c4'})
        ## Add remaining state transitions
        sys.transitions.add_comb({'c4'}, {'c4', 'c9'})
        sys.transitions.add_comb({'c9'}, {'c9'})

        # Variables
        env_vars = {'vh': (2, 6), 
                    'light': ["g1", "g2", "g3", "y1", "y2", "r"]}
        sys_vars = {}

        # Initialization
        env_init = {'vh = 2',
                    'light = "g1"'}
        sys_init = sys_init = {}
        
        # Safety
        env_safe = {
            # Human vehicle movement
            'vh = 2 -> next(vh) = 2 | next(vh) = 3',
            'vh = 3 -> next(vh) = 3 | next(vh) = 4',
            'vh = 4 -> next(vh) = 4 | next(vh) = 5',
            'vh = 5 -> next(vh) = 5 | next(vh) = 6',
            'vh = 6 -> next(vh) = 6',
            # Traffic light
            'light = "g1" -> next(light = "g2")',
            'light = "g2" -> next(light = "g3")',
            'light = "g3" -> next(light = "y1")',
            'light = "y1" -> next(light = "y2")',
            'light = "y2" -> next(light = "r")',
            'light = "r" -> next(light = "r") | next(light = "g1")',
            # Human vehicle does not run a red
            '!(light = "r" & (vh = 4 | vh = 5))'
        }
        sys_safe = {
            # No collision with human vehicle
            '!(a4 & vh = 4)',
            # No running a red
            '!(light="r" & (a4 || a8))'
        }

        # Progress
        env_prog = {'vh = 6',
                    'light = "g1"'}
        sys_prog = {'a9'}
        
        if self.primed:
            sys_safe |= {'!(a4 & X(vh = 4))'}

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
    path = 'left_turn/'
    sims = []
    f2 = open(path + "errors.txt", "w")
    f = open(path + "realizable.txt", "w")
    f.write("The simulations of left turn that have a realizable controller\n")
    for primed in [True, False]:
        for plus_one in [True, False]:
            for moore in [True, False]:
                for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                    run = LeftTurn(plus_one, moore, qinit, primed)
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
