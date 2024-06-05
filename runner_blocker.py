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
    path = 'runner_blocker/'
    # You can find the explainations of the states at GR1_simulations/RunnerBlockerStatesExplained.jpeg

    # # System definition
    # # Making a finite transition system
    # sys = tlp.transys.FTS()

    # Variables
    env_vars = {}
    sys_vars = {}
    env_vars['b'] = (1,3)
    sys_vars['r'] = (1,4)

    # Initialization
    env_init = {'b=2'}
    sys_init = {'r=1'}


    # Blocker Safety
    env_safe = {'b=1 -> X(b=2)',
                'b=2 -> X(b=1 || b=3)',
                'b=3 -> X(b=2)'
    }

    # Runner Safety
    sys_safe = {'r = 1 -> X(r=2 || r=3)',
                'r = 2 -> X(r=4)',
                'r = 3 -> X(r=4)',
                'r = 4 -> X(r=4)'
    }

    # Avoid collision:
    sys_safe |= {'(b=1 -> !(r=2))',
                 '(b=3 -> !(r=3))',
                 '(!(r=2 & X(b=1)))',
                 '(!(r=3 & X(b=3)))'
    }

    # Progress
    env_prog = {}
    sys_prog = {'r=4'}

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
    
    new_g0 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=False, append_non_visited=True, qinit=aut.qinit)
    new_h0 = gb._game_format_nx(new_g0, attributes)
    new_pd0 = nx.drawing.nx_pydot.to_pydot(new_h0)
    new_pd0.write_pdf(path + 'new_game.pdf')

    if nx.is_isomorphic(g0, new_g0):
        print('g0 ismorphic to new_g0')
    else:
        print("g0.number_of_edges():", g0.number_of_edges())
        print("new_g0.number_of_edges():", new_g0.number_of_edges())
        print("g0.number_of_nodes():", g0.number_of_nodes())
        print("new_g0.number_of_nodes():", new_g0.number_of_nodes())
    
    # Making a graph of the asynchronous GR(1) game without deadends.
    g1 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=True, qinit=aut.qinit)
    h1 = gb._game_format_nx(g1, attributes)
    pd1 = nx.drawing.nx_pydot.to_pydot(h1)
    pd1.write_pdf(path + 'game_no_deadends.pdf')

    new_g1 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=True, append_non_visited=True, qinit=aut.qinit)
    new_h1 = gb._game_format_nx(new_g1, attributes)
    new_pd1 = nx.drawing.nx_pydot.to_pydot(new_h1)
    new_pd1.write_pdf(path + 'new_game_no_deadends.pdf')

    if nx.is_isomorphic(g1, new_g1):
        print('g1 ismorphic to new_g1')
    else:
        print("g1.number_of_edges():", g1.number_of_edges())
        print("new_g1.number_of_edges():", new_g1.number_of_edges())
        print("g1.number_of_nodes():", g1.number_of_nodes())
        print("new_g1.number_of_nodes():", new_g1.number_of_nodes())

    # Making a graph pf the state transitions of the environment and system
    g2 = gb.state_graph(aut, env='env', sys='sys', qinit=aut.qinit)
    h2, _ = gb._state_format_nx(g2, attributes)
    pd2 = nx.drawing.nx_pydot.to_pydot(h2)
    pd2.write_pdf(path + 'states.pdf')

    # machines.random_run(ctrl, N=10)

if __name__ == "__main__":
    experiment()
