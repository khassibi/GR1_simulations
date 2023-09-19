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

class PatrollingCar(simulations.Simulation):

    def make_specs(self):
        path = 'patrolling_car/'

        # Define the states of the system
        states = []
        for x in range(5):
            for y in range(5):
                states.append("c{}{}".format(x, y))
        
        # Variables
        env_vars = {'b': (0,4)}
        sys_vars = {'r': states,
                    'fuel': (0,8),
                    'move': 'boolean',
                    'will_refuel': 'boolean'
        }

        # Initialization
        env_init = {'b=0'}
        sys_init = {'r="c40"',
                    'fuel=8',
                    '!move',
                    '!will_refuel'
        }

        # Safety
        env_safe = {'(b=0) -> X(b=1)', '(b=4) -> X(b=3)'}
        for i in range(1,4):
            env_safe |= {'(b={0}) -> X((b={1}) | (b={2}))'.format(i, i-1, i+1)}

        sys_safe = set()

        for x in range(1,4):
            sys_safe |= {'(r="c{}{}") -> (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move)'.format(x,0, x-1,0, x+1,0, x,1),
                        '(r="c{}{}") -> (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move)'.format(x,4, x-1,4, x+1,4, x,3),
                        '(r="c{}{}") -> (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move)'.format(0,x, 0,x+1, 0,x-1, 1,x),
                        '(r="c{}{}") -> (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move)'.format(4,x, 4,x+1, 4,x-1, 3,x)
            }
            for y in range(1,4):
                sys_safe |= {'(r="c{}{}") -> (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move)'.format(x,y, x+1,y, x-1,y, x,y+1, x,y-1)}

        # Corners
        sys_safe |= {'(r="c00") -> (X((r="c10") | (r="c01")) & X move)',
                    '(r="c40") -> (X((r="c30") | (r="c41")) & X move)',
                    '(r="c44") -> (X((r="c34") | (r="c43")) & X move)',
                    '(r="c04") -> (X((r="c03") | (r="c14")) & X move)'
        }

        sys_safe |= {'fuel != 0',
                    'X(r="c42") -> X(will_refuel)', # TODO: make sure this works
                    'will_refuel -> X(fuel = 8)',
                    '(X(move)) -> (X(fuel) = fuel - 1) | (will_refuel)'
        }
        for i in range(0,5):
            sys_safe |= {'!((r="c1{0}") & (b={0}))'.format(i),
                        '!((r="c1{0}") & X(b={0}))'.format(i)}
        
        # Progress
        env_prog = set()
        sys_prog = {'r="c04"'}

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

if __name__ == '__main__':
    path = 'patrolling_car/'
    sims = []
    f2 = open(path + "errors.txt", "w")
    f = open(path + "realizable.txt", "w")
    f.write("The simulations of patrolling car that have a realizable controller\n")
    for plus_one in [True, False]:
        for moore in [True, False]:
            for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                run = PatrollingCar(plus_one, moore, qinit)
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