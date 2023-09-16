import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines

from tulip import dumpsmach
import pickle

def experiment():
    path = 'patrolling_car/'

    # System definition
    sys = tlp.transys.FTS()

    # Define the states of the system
    states = []
    for x in range(5):
        for y in range(5):
            states.append("({},{})".format(x, y))
    sys.states.add_from(states)
    sys.states.initial.add('(4,0)')

    for x in range(1,4):
        sys.transitions.add_comb({'({},{})'.format(x, 0)}, {'({},{})'.format(x-1, 0), '({},{})'.format(x+1, 0), '({},{})'.format(x,1)})
        sys.transitions.add_comb({'({},{})'.format(x, 4)}, {'({},{})'.format(x-1, 4), '({},{})'.format(x+1, 4), '({},{})'.format(x,3)})
        sys.transitions.add_comb({'({},{})'.format(0, x)}, {'({},{})'.format(0, x+1), '({},{})'.format(0, x-1), '({},{})'.format(1,x)})
        sys.transitions.add_comb({'({},{})'.format(4, x)}, {'({},{})'.format(4, x+1), '({},{})'.format(4, x-1), '({},{})'.format(3,x)})
        for y in range(1,4):
            sys.transitions.add_comb({'({},{})'.format(x, y)}, {'({},{})'.format(x+1, y), '({},{})'.format(x-1, y), '({},{})'.format(x,y+1), '({},{})'.format(x,y-1)})
    
    sys.transitions.add_comb({'(0,0)'}, {'(1,0)', '(0,1)'})
    sys.transitions.add_comb({'(4,0)'}, {'(3,0)', '(4,1)'})
    sys.transitions.add_comb({'(4,4)'}, {'(3,4)', '(4,3)'})
    sys.transitions.add_comb({'(0,4)'}, {'(0,3)', '(1,4)'})

    sys.atomic_propositions.add_from({'goal', 'refueling', 'r0', 'r1', 'r2', 'r3', 'r4'})
    sys.states.add('(0,4)', ap={'goal'})
    sys.states.add('(4,2)', ap={'refueling'})
    for r in range(0,5):
        sys.states.add('(1,{})'.format(r), ap={'r{}'.format(r)})

    # Variables
    env_vars = {'b': (0,4)}
    sys_vars = {'fuel': (0,8)}

    # Initialization
    env_init = {'b=0'}
    sys_init = {'fuel=8'}

    # Safety
    env_safe = {'(b=0) -> X(b=1)', '(b=4) -> X(b=3)'}
    for i in range(1,4):
        env_safe |= {'(b={0}) -> X((b={1}) | (b={2}))'.format(i, i-1, i+1)}
    sys_safe = {'fuel > 0',
                'refueling -> fuel = 8' # TODO: make sure this works
    }
    for i in range(0,5):
        sys_safe |= {'!(r{0} & (b={0}))'.format(i),
                    '!(r{0} & X(b={0}))'.format(i)}
    
    # Progress
    env_prog = {}
    sys_prog = {'goal'}

if __name__ == '__main__':
    experiment()