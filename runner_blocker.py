import logging
from tulip import spec
from tulip import synth
from tulip.transys import machines
from tulip import dumpsmach
import pickle
import simulations

logging.basicConfig(level=logging.WARNING)

class RunnerBlocker(simulations.Simulation):
    def make_specs(self):
        env_vars = {}
        sys_vars = {}
        env_vars['b'] = (1,3)
        if self.aug:
            sys_vars['r'] = (1,5)
        else:
            sys_vars['r'] = (1,4)

        env_init = {'b=2'}
        sys_init = {'r=1'}

        env_safe = {
                    'b=1 -> X(b=2)',
                    'b=2 -> X(b=1 || b=3)',
                    'b=3 -> X(b=2)'
                }


        if self.aug:
            sys_safe = {
                        'r = 1 -> X(r=2 || r=3 || r=5)',
                        'r = 2 -> X(r=4)',
                        'r = 3 -> X(r=4)',
                        'r = 4 -> X(r=4)',
                        'r = 5 -> X(r=4)'
                    }
        else:
            sys_safe = {
                        'r = 1 -> X(r=2 || r=3)',
                        'r = 2 -> X(r=4)',
                        'r = 3 -> X(r=4)',
                        'r = 4 -> X(r=4)'
                    }
        

        # Avoid collision:
        sys_safe |= {
                    '(b=1 -> !(r=2))',
                    '(b=3 -> !(r=3))',
        }

        if self.aug:
            sys_safe |= {'(b=2 -> !(r=5))'}

        # Cannot be collided into:
        if self.primed:
            sys_safe |= {
                        "(!(r=2 & X(b=1)))",
                        "(!(r=3 & X(b=3)))",
                        "(!(r=5 & X(b=2)))",
            }

        env_prog = {}
        sys_prog = {'r=4'}

        # Create a GR(1) specification
        specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)
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
    path = 'runner_blocker/'
    sims = []
    f = open(path + "runs.txt", "w")
    f.write("The simulations of runner blocker that have a realizable controller\n")
    for aug in [True, False]:
        for primed in [True, False]:
            for plus_one in [True, False]:
                for moore in [True, False]:
                    for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                        run = RunnerBlocker(aug,  primed, plus_one, moore, qinit)
                        run.give_name('rb')
                        run.make_specs()
                        run.make_strat(path)
                        sims.append(run)
                        if run.realizable:
                            f.write('\n------\n')
                            f.write(run.name)
    f.close()
