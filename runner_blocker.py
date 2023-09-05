import logging
from tulip import spec
from tulip import synth
from tulip.transys import machines
from tulip import dumpsmach
import pickle

logging.basicConfig(level=logging.WARNING)

class RunnerBlocker:
    def __init__(self, aug, primed, plus_one, moore, qinit):
        '''
        aug: boolean evaluating to True when the runner can go through the middle
        primed: boolean evaluating to True when we check if the next environment 
                state collides with the current system state
        plus_one: boolean
        moore: boolean if True is a moore machine and if False is mealy
        qinit: string 
        '''
        self.aug = aug
        self.primed = primed
        self.plus_one = plus_one
        self.moore = moore
        self.qinit = qinit
        self.realizable = None
        # self.ctrl_func = None

    def run(self):
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

        # At this point we can synthesize the controller
        # using one of the available methods.
        strategy = synth.synthesize(specs)
        if strategy is not None:
            self.realizable = True

            filename = 'runner_blocker/rb'
            if self.aug:
                filename += "_aug"
            if specs.moore:
                filename += '_moore'
            else:
                filename += '_mealy'

            if specs.plus_one:
                filename += '_plus_one'

            if self.primed:
                filename += '_primed'

            filename += '_' + specs.qinit[1] + specs.qinit[-1] + '.py'

            dumpsmach.write_python_case(filename, strategy, classname='runner')
        else:
            self.realizable = False


if __name__ == '__main__':
    simulations = []
    for aug in [True, False]:
        for primed in [True, False]:
            for plus_one in [True, False]:
                for moore in [True, False]:
                    for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                        rb = RunnerBlocker(aug,  primed, plus_one, moore, qinit)
                        rb.run()
                        simulations.append(rb)
    
    with open('runner_blocker/simulations', 'wb') as file:
        pickle.dump(simulations, file)
    

