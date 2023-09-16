import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines
from GR1_defaults import settings

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
    sys_safe = {'!(fuel = 0)',
                'refueling -> X(fuel = 8)', # TODO: make sure this works
                '(!refueling) -> X(fuel) = fuel - 1'
    }
    for i in range(0,5):
        sys_safe |= {'!(r{0} & (b={0}))'.format(i),
                    '!(r{0} & X(b={0}))'.format(i)}
    
    # Progress
    env_prog = set()
    sys_prog = {'goal'}

    # Settings for the specifications
    specs = settings.set_specs(env_vars, sys_vars, env_init, sys_init,
                               env_safe, sys_safe, env_prog, sys_prog)
    print(specs.pretty())

    # Turning the specifications into an automaton
    spec = tlp.synth._spec_plus_sys(specs, sys, None, False, False)
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesize the controller
    ctrl = tlp.synth.synthesize(specs, sys=sys)
    assert ctrl is not None, 'unrealizable'
    with open(path + "ctrl", "wb") as file:
        pickle.dump(ctrl, file)

    dumpsmach.write_python_case(path + 'controller.py', ctrl, classname="sys_ctrl")

    # Graphing
    filename = path + "graph"
    attributes = ['color', 'shape']

    # Making a graph of the asynchronous GR(1) game with deadends.
    g0 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=False, qinit=aut.qinit)
    h0 = gb._game_format_nx(g0, attributes)
    pd0 = nx.drawing.nx_pydot.to_pydot(h0)
    pd0.write_pdf(path + 'game.pdf')
    with open(filename, "wb") as file:
        pickle.dump(g0, file)
    
    # Making a graph of the asynchronous GR(1) game without deadends.
    g1 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=True, qinit=aut.qinit)
    h1 = gb._game_format_nx(g1, attributes)
    pd1 = nx.drawing.nx_pydot.to_pydot(h1)
    pd1.write_pdf(path + 'game_no_deadends.pdf')

    # Making a graph pf the state transitions of the environment and system
    g2 = gb.state_graph(aut, env='env', sys='sys', qinit=aut.qinit)
    h2, _ = gb._state_format_nx(g2, attributes)
    pd2 = nx.drawing.nx_pydot.to_pydot(h2)
    pd2.write_pdf(path + 'states.pdf')

if __name__ == '__main__':
    experiment()