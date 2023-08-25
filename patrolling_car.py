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
    # Making a finite transition system
    sys = tlp.transys.FTS()
    # .FiniteTransitionSystem
    # ReactiveTest/quadruped_maze/setup_graphs.py

    # Define the states of the system
    states = []
    for x in range(5):
        for y in range(5):
            states.append("({},{})".format(x, y))
    sys.states.add_from(states)
    sys.states.initial.add('(0,0)')    # start in state X0

    for x in range(5):
        for y in range(5):
            if x == 0:
                if y == 0:
                    sys.transitions.add_comb({'(0,0)'}, {'(1,0)', '(0,1)'})
                elif y == 4:
                    sys.transitions.add_comb({'(0,4)'}, {'(1,4)', '(0,3)'})
                else: 
                    sys.transitions.add_comb({'({},{})'.format(x,y)}, {'({},{})'.format(x+1,y), '({},{})'.format(x,y+1), '({},{})'.format(x,y-1)})
            elif x == 4:
                if y == 0:
                    sys.transitions.add_comb({'(4,0)'}, {'(3,0)', '(4,1)'})
                elif y == 4:
                    sys.transitions.add_comb({'(4,4)'}, {'(4,3)', '(3,4)'})
                else: 
                    sys.transitions.add_comb({'({},{})'.format(x,y)}, {'({},{})'.format(x-1,y), '({},{})'.format(x,y+1), '({},{})'.format(x,y-1)})
            elif y == 0:
                sys.transitions.add_comb({'({},{})'.format(x,y)}, {'({},{})'.format(x,y+1), '({},{})'.format(x+1,y), '({},{})'.format(x-1,y)})
            elif y == 4:
                sys.transitions.add_comb({'({},{})'.format(x,y)}, {'({},{})'.format(x,y-1), '({},{})'.format(x+1,y), '({},{})'.format(x-1,y)})
            else:
                sys.transitions.add_comb({'({},{})'.format(x,y)}, {'({},{})'.format(x,y-1), '({},{})'.format(x,y+1), '({},{})'.format(x+1,y), '({},{})'.format(x-1,y)})
            
    sys.atomic_propositions.add('goal')
    sys.states.add('(4,4)', ap={'goal'})

if __name__ == '__main__':
    experiment()