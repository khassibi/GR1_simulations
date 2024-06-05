import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines
from GR1_defaults import settings

from tulip import dumpsmach
import pickle

from omega.games import enumeration as enum

path = 'Tgame/'

# System definition
sys = tlp.transys.FTS()

sys.atomic_propositions.add_from({'a0', 'a1', 'a2', 'a3'})
sys.states.add('c0', ap={'a0'})
sys.states.add('c1', ap={'a1'})
sys.states.add('c2', ap={'a2'})
sys.states.add('c3', ap={'a3'})
# System initialization
sys.states.initial.add('c0')    # start in state c0

# System safety conditions (transitions)
sys.transitions.add_comb({'c0'}, {'c0', 'c1'})
sys.transitions.add_comb({'c1'}, {'c1', 'c2'})
# sys.transitions.add_comb({'c1'}, {'c0', 'c1', 'c2'})
sys.transitions.add_comb({'c2'}, {'c2', 'c3'})
# sys.transitions.add_comb({'c2'}, {'c1', 'c2', 'c3'})
sys.transitions.add_comb({'c3'}, {'c3'})
# sys.transitions.add_comb({'c3'}, {'c2', 'c3'})

# Variables
env_vars = {'b': (0, 4)}
sys_vars = {}

# Initialization
env_init = {'b = 0'}
sys_init = {}

# Safety
env_safe = {
    # Movement
    'b = 0 -> next(b) = 0 | next(b) = 1',
    'b = 1 -> next(b) = 1 | next(b) = 0 | next(b) = 2',
    'b = 2 -> next(b) = 2 | next(b) = 1 | next(b) = 3',
    'b = 3 -> next(b) = 3 | next(b) = 2 | next(b) = 4',
    'b = 4 -> next(b) = 4 | next(b) = 3',
}
sys_safe = {
    # No collision
    '!(a2 & b = 2)',
    # No being collided into
    # Commenting this out means that we are considering the game as having simultaneous updates
    '!(a2 & X(b = 2))'
}

# Progress
env_prog = {'b = 4'}
sys_prog = {'a3'}
    

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