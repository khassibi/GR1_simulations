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
    path = 'var_inc/'

    # Variables
    env_vars = {'env_bool': 'boolean'}
    sys_vars = {'num': (0, 1)}

    increment = False

    # Initialization
    env_init = {'env_bool=true'}
    if increment:
        sys_init = {'num=0'}
    else:
        sys_init = {'num=1'}

    # Safety
    env_safe = {'env_bool!=false'}
    if increment:
        sys_safe = {'(num=0) -> (X(num)=num+1)',
                    '(num=1) -> (X(num)=1)'}
    else:
        sys_safe = {'(num=1) -> (X(num)=num-1)',
                    '(num=0) -> (X(num)=0)'}

    # Progress
    env_prog = set()
    if increment:
        sys_prog = {'num=1'}
    else:
        sys_prog = {'num=0'}

    specs = settings.set_specs(env_vars, sys_vars, env_init, sys_init,
                               env_safe, sys_safe, env_prog, sys_prog)

    spec = tlp.synth._spec_plus_sys(specs, None, None, False, False)

    # Automaton class found in omega/omega/symbolic/temporal.py
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesizing system controller
    ctrl = tlp.synth.synthesize(specs)
    assert ctrl is not None, 'unrealizable'

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


if __name__ == "__main__":
    experiment()
