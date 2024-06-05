import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx

def experiment():
    path = 'runner_blocker/'

    # Variables
    env_vars = {}
    sys_vars = {}
    env_vars['b'] = (1,3)
    sys_vars['r'] = (1,4)

    # Initialization
    env_init = {'b=2'}
    sys_init = {'r=1'}


    # Blocker Transitions
    env_safe = {'b=1 -> X(b=2)',
                'b=2 -> X(b=1 || b=3)',
                'b=3 -> X(b=2)'
    }

    # Runner Transitions
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
    specs = tlp.spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                            env_safe, sys_safe, env_prog, sys_prog)
    specs.qinit = '\A \E'
    specs.moore = False # mealy controller
    specs.plus_one = False
    print(specs.pretty())

    # Turning the specifications into an automaton
    spec = tlp.synth._spec_plus_sys(specs, None, None, False, False)
    aut = omega_int._grspec_to_automaton(spec)

    # Synthesize the controller
    ctrl = tlp.synth.synthesize(specs)
    assert ctrl is not None, 'unrealizable'

if __name__ == "__main__":
    experiment()