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
    path = 'left_turn_copy/'

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
        '!(X(vh=4) & (a=4))',
        # No running reds
        '!(light = "r" & (a=4 || a=8))'
    }

    # Progress
    env_prog = {'vh = 6'}
    sys_prog = {'a = 9'}

    specs = settings.set_specs(env_vars, sys_vars, env_init, sys_init,
                               env_safe, sys_safe, env_prog, sys_prog)
    print(specs.pretty())

    spec = tlp.synth._spec_plus_sys(specs, None, None, False, False)
    # Automaton class found in omega/omega/symbolic/temporal.py
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesize the controller
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

if __name__ == "__main__":
    experiment()
