import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines

from tulip import dumpsmach
import pickle

def experiment():
    path = 'runner_blocker/'
    # You can find the explainations of the states at GR1_simulations/RunnerBlockerStatesExplained.jpeg

    # System definition
    # Making a finite transition system
    sys = tlp.transys.FTS()

    sys.states.add_from(['c1', 'c2', 'c3', 'c4'])
    sys.states.initial.add('c1')  # start in state c1

    sys.transitions.add_comb({'c1'}, {'c2', 'c3'})
    sys.transitions.add_comb({'c2'}, {'c4'})
    sys.transitions.add_comb({'c3'}, {'c4'})
    sys.transitions.add_comb({'c4'}, {'c4'})

    sys.atomic_propositions.add_from({'a1', 'a2', 'a3', 'a4'})
    sys.states.add('c1', ap={'a1'})
    sys.states.add('c2', ap={'a2'})
    sys.states.add('c3', ap={'a3'})
    sys.states.add('c4', ap={'a4'})

    # Specifications for the environment

    # Blocker dynamics
    env_vars = {'b': (1, 3)}
    env_init = {'b = 2'}
    env_safe = {
        'b = 2 -> next(b) = 1 | next(b) = 3',
        'b = 1 -> next(b) = 2',
        'b = 3 -> next(b) = 2'
    }
    env_prog = {}

    # System variables and requirements
    sys_vars = {}
    sys_init = {'a1'}
    sys_prog = {'a4'}
    sys_safe = {
        '!(a2 & b = 1)',
        '!(a3 & b = 3)'
        # '!(a2 & next(b) = 1)',
        # '!(a3 & next(b) = 3)',
        # 'b=1 -> !a2',
        # 'b=3 -> !a3'
    }

    # Function found in tulip-control/tulip/spec/form.py
    specs = tlp.spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                            env_safe, sys_safe, env_prog, sys_prog)
    specs.qinit = '\A \E'
    specs.moore = False
    print(specs.pretty())

    # Turning the specifications into an automaton
    spec = tlp.synth._spec_plus_sys(specs, None, sys, False, False)
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesize the controller
    ctrl = tlp.synth.synthesize(specs, sys=sys)
    assert ctrl is not None, 'unrealizable'
    with open(path + "/ctrl", "wb") as file:
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

    # machines.random_run(ctrl, N=10)

if __name__ == "__main__":
    experiment()
