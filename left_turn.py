import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines

from tulip import dumpsmach
import pickle

path = 'left_turn/'

class LeftTurn:
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
        self.name = 'lf'
        # self.ctrl_func = None

    def run(self):
        # Variables
        env_vars = {'vh': (2, 6), 'light': ["g1", "g2", "g3", "y1", "y2", "r"]}
        sys_vars = {'a': [7, 8, 4, 9]}

        # Initialization
        env_init = {'vh = 2', 'light = "g1"'}
        sys_init = {'a = 7'}

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
            'a = 7 -> X(a=7 || a=8)',
            'a = 8 -> X(a=8 || a=4)',
            'a = 4 -> X(a=4 || a=9)',
            'a = 9 -> X(a=9)',
            # No collisions
            'vh = 4 -> !(a=4)',
            # No running reds
            '!(light = "r" & (a=4 || a=8))'
        }
        if self.primed:
            sys_safe |= {'!(X(vh=4) & (a=4))'}

        # Progress
        env_prog = {'vh = 6'}
        sys_prog = {'a = 9'}

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

        # At this point we can synthesize the controller
        # using one of the available methods.
        strategy = synth.synthesize(specs)
        if strategy is not None:
            self.realizable = True

            if self.aug:
                self.name += "_aug"
            if specs.moore:
                self.name += '_moore'
            else:
                self.name += '_mealy'

            if specs.plus_one:
                self.name += '_plus_one'

            if self.primed:
                self.name += '_primed'

            self.name += '_' + specs.qinit[1] + specs.qinit[-1]

            dumpsmach.write_python_case(path + self.name + '.py', strategy, classname='left_turn')
        else:
            self.realizable = False


if __name__ == '__main__':
    simulations = []
    f = open(path + "runs.txt", "w")
    f.write("The simulations of left turn that have a realizable controller\n\n")
    for aug in [True, False]:
        for primed in [True, False]:
            for plus_one in [True, False]:
                for moore in [True, False]:
                    for qinit in ['\E \A', '\A \E']: #, '\A \A', '\E \E']:
                        lt = LeftTurn(aug,  primed, plus_one, moore, qinit)
                        lt.run()
                        simulations.append(lt)
                        if lt.realizable:
                            f.write(lt.name)
    f.close()
    
    with open(path + 'simulations', 'wb') as file:
        pickle.dump(simulations, file)