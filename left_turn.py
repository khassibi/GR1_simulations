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
    path = 'left_turn/'

    # System definition
    sys = tlp.transys.FTS()

    sys.atomic_propositions.add_from({'a4', 'a7', 'a8', 'a9'})
    sys.states.add('c4', ap={'a4'})
    sys.states.add('c7', ap={'a7'})
    sys.states.add('c8', ap={'a8'})
    sys.states.add('c9', ap={'a9'})
    sys.states.initial.add('c7')    # start in state c7

    sys.transitions.add_comb({'c7'}, {'c7', 'c8'})
    sys.transitions.add_comb({'c8'}, {'c8', 'c4'})
    sys.transitions.add_comb({'c4'}, {'c4', 'c9'})
    sys.transitions.add_comb({'c9'}, {'c9'})

    # Variables
    env_vars = {'vh': (2, 6), 
                'light': ["g1", "g2", "g3", "y1", "y2", "r"]}
    sys_vars = {}

    # Initialization
    env_init = {'vh = 2',
                'light = "g1"'}
    sys_init = {}
    
    # Safety
    env_safe = {
        # Human vehicle movement
        'vh = 2 -> next(vh) = 2 | next(vh) = 3',
        'vh = 3 -> next(vh) = 3 | next(vh) = 4',
        'vh = 4 -> next(vh) = 4 | next(vh) = 5',
        'vh = 5 -> next(vh) = 5 | next(vh) = 6',
        'vh = 6 -> next(vh) = 6',
        # Traffic light
        'light = "g1" -> next(light = "g2")',
        'light = "g2" -> next(light = "g3")',
        'light = "g3" -> next(light = "y1")',
        'light = "y1" -> next(light = "y2")',
        'light = "y2" -> next(light = "r")',
        'light = "r" -> next(light = "r") | next(light = "g1")',
        # Human vehicle does not run a red
        '!(light = "r" & (vh = 4 | vh = 5))'
    }
    sys_safe = {
        # No collision with human vehicle
        '!(a4 & vh = 4)',
        # No running a red
        '!(light="r" & (a4 || a8))' #,
        # No being collided into by the human vehicle
        # Commenting this out means that we are considering the game as having simultaneous updates
        # '!(a4 & X(vh = 4))'
    }

    # Progress
    env_prog = {'vh = 6',
                'light = "g1"'}
    sys_prog = {'a9'}
        

    specs = settings.set_specs(env_vars, sys_vars, env_init, sys_init,
                            env_safe, sys_safe, env_prog, sys_prog)
    print(specs.pretty())

    spec = tlp.synth._spec_plus_sys(specs, None, sys, False, False)
    # Automaton class found in omega/omega/symbolic/temporal.py
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
    g0 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=False, append_non_visited=False, qinit=aut.qinit)
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
    g1 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=True, append_non_visited=False, qinit=aut.qinit)
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

if __name__ == "__main__":
    experiment()
