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

    # Define the states of the system
    states = []
    for x in range(5):
        for y in range(5):
            states.append("c{}{}".format(x, y))
    
    # Variables
    env_vars = {'b': (0,4)}
    sys_vars = {'r': states,
                'fuel': (0,8)
    }

    # Initialization
    env_init = {'b=0'}
    sys_init = {'r="c40"',
                'fuel=8'
    }

    # Safety
    env_safe = {'(b=0) -> X(b=1)', '(b=4) -> X(b=3)'}
    for i in range(1,4):
        env_safe |= {'(b={0}) -> X((b={1}) | (b={2}))'.format(i, i-1, i+1)}

    sys_safe = set()

    for x in range(1,4):
        sys_safe |= {'(r="c{}{}") -> X((r="c{}{}") | (r="c{}{}") | (r="c{}{}"))'.format(x,0, x-1,0, x+1,0, x,1),
                    '(r="c{}{}") -> X((r="c{}{}") | (r="c{}{}") | (r="c{}{}"))'.format(x,4, x-1,4, x+1,4, x,3),
                    '(r="c{}{}") -> X((r="c{}{}") | (r="c{}{}") | (r="c{}{}"))'.format(0,x, 0,x+1, 0,x-1, 1,x),
                    '(r="c{}{}") -> X((r="c{}{}") | (r="c{}{}") | (r="c{}{}"))'.format(4,x, 4,x+1, 4,x-1, 3,x)
        }
        for y in range(1,4):
            sys_safe |= {'(r="c{}{}") -> X((r="c{}{}") | (r="c{}{}") | (r="c{}{}") | (r="c{}{}"))'.format(x,y, x+1,y, x-1,y, x,y+1, x,y-1)}

    # Corners
    sys_safe |= {'(r="c00") -> X((r="c10") | (r="c01"))',
                '(r="c40") -> X((r="c30") | (r="c41"))',
                '(r="c44") -> X((r="c34") | (r="c43"))',
                '(r="c04") -> X((r="c03") | (r="c14"))'
    }

    sys_safe |= {'!(fuel = 0)',
                '(r="c42") -> X(fuel = 8)', # TODO: make sure this works
                '(!(r="c42") & (fuel=8)) -> X(fuel=7)',
                '(!(r="c42") & (fuel=7)) -> X(fuel=6)',
                '(!(r="c42") & (fuel=6)) -> X(fuel=5)',
                '(!(r="c42") & (fuel=5)) -> X(fuel=4)',
                '(!(r="c42") & (fuel=4)) -> X(fuel=3)',
                '(!(r="c42") & (fuel=3)) -> X(fuel=2)',
                '(!(r="c42") & (fuel=2)) -> X(fuel=1)',
                '(!(r="c42") & (fuel=1)) -> X(fuel=0)',
                '(!(r="c42") & (fuel=0)) -> X(fuel=0)'
    }
    for i in range(0,5):
        sys_safe |= {'!((r="c1{0}") & (b={0}))'.format(i),
                    '!((r="c1{0}") & X(b={0}))'.format(i)}
    
    # Progress
    env_prog = set()
    sys_prog = {'r="c04"'}

    # Settings for the specifications
    specs = settings.set_specs(env_vars, sys_vars, env_init, sys_init,
                               env_safe, sys_safe, env_prog, sys_prog)
    print(specs.pretty())

    # Turning the specifications into an automaton
    # spec = tlp.synth._spec_plus_sys(specs, sys, None, False, False)
    spec = tlp.synth._spec_plus_sys(specs, None, None, False, False)
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesize the controller
    # ctrl = tlp.synth.synthesize(specs, sys=sys)
    ctrl = tlp.synth.synthesize(specs)
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