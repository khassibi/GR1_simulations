import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines
from tulip import dumpsmach

class Simulation:
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
        self.name = None
        self.error = False
        self.specs = None
        self.sys = None
    
    def give_name(self, start_str):
        # Naming
        self.name = start_str
        if self.aug:
            self.name += "_aug"
        if self.moore:
            self.name += '_moore'
        else:
            self.name += '_mealy'

        if self.plus_one:
            self.name += '_plus_one'

        if self.primed:
            self.name += '_primed'

        self.name += '_' + self.qinit[1] + self.qinit[-1]
    
    def make_specs(self):
        pass

    def make_strat(self, path=''):
        # At this point we can synthesize the controller
        # using one of the available methods.
        strategy = synth.synthesize(self.specs, sys=self.sys)
        if strategy is not None:
            self.realizable = True
            dumpsmach.write_python_case(path + self.name + '.py', strategy, classname='Strategy')
        else:
            self.realizable = False