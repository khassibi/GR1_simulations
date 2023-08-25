import tulip as tlp
from tulip.interfaces import omega as omega_int
from tulip import transys, abstract, spec, synth
from visualization import graph_builder as gb
import networkx as nx
from tulip.transys import machines

from tulip import dumpsmach
import pickle

def experiment():
    path = 'electric_power/'
    # System definition
    sys = tlp.transys.FTS()

    # System variables
    sys_vars = {'C1': (0,1),
                'C2': (0,1),
                'C5': (0,1),
                'C6': (0,1),
                'til_C1': (0,1),
                'til_C2': (0,1),
                'til_C5': (0,1),
                'til_C6': (0,1),
                'B1': (0,1),
                'B2': (0,1),
                'B3': (0,1),
                'B4': (0,1)}
    # sys_vars.update({'C3': ["-1", "0", "1"]})
    # sys_vars.update({'C4': ["-1", "0", "1"]})
    # sys_vars.update({'C7': ["-1", "0", "1"]})
    # sys_vars.update({'til_C3': ["-1", "0", "1"]})
    # sys_vars.update({'til_C4': ["-1", "0", "1"]})
    # sys_vars.update({'til_C7': ["-1", "0", "1"]})
    sys_vars.update({'C3': (-1,1),
                    'C4': (-1,1),
                    'C7': (-1,1),
                    'til_C3': (-1,1),
                    'til_C4': (-1,1),
                    'til_C7': (-1,1)})
    sys_vars.update({'t1': (0,5),
                    't2': (0,5),
                    't3': (0,5),
                    't4': (0,5)})
    
    # Time considerations
    sys_safe = {'next(C1) = til_C1',
                'next(C2) = til_C2',
                'next(C3) = til_C3',
                'next(C4) = til_C4',
                'next(C5) = til_C5',
                'next(C6) = til_C6',
                'next(C7) = til_C7'}
    
    # Environment variables
    env_vars = {'GL': (0,1),
                'GR': (0,1),
                'AL': (0,1),
                'AR': (0,1)}
    
    # Environment Assumption
    env_safe = {'(GL = 1) | (AL = 1) | (GR = 1) | (AR = 1)'}

    # Power Status of Buses
    sys_safe.update({ # B1
                '((C1 = 1) & (GL = 1)) -> (B1 = 1)',
                '((B2 = 1) & (C3 = -1)) -> (B1 = 1)',
                '( !((C1 = 1) & (GL = 1)) & !((B2 = 1) & (C3 = -1)) ) -> (B1 = 0)',
                # B2
                '((C2 = 1) & (AL = 1)) -> (B2 = 1)',
                '((B1 = 1) & (C3 = 1)) -> (B2 = 1)',
                '((B3 = 1) & (C4 = -1)) -> (B2 = 1)',
                '( !((C2 = 1) & (AL = 1)) & !((B1 = 1) & (C3 = 1)) & !((B3 = 1) & (C4 = -1)) ) -> (B2 = 0)',
                # B3
                '((C5 = 1) & (AR = 1)) -> (B3 = 1)',
                '((B2 = 1) & (C4 = 1)) -> (B3 = 1)',
                '((B4 = 1) & (C7 = -1)) -> (B3 = 1)',
                '( !((C5 = 1) & (AR = 1)) & !((B2 = 1) & (C4 = 1)) & !((B4 = 1) & (C7 = -1)) ) -> (B3 = 0)',
                # B4
                '((C6 = 1) & (GR = 1)) -> (B4 = 1)',
                '((B3 = 1) & (C7 = 1)) -> (B4 = 1)',
                '( !((C6 = 1) & (GR = 1)) & !((B3 = 1) & (C7 = 1)) ) -> (B4 = 0)'
    })

    # No Paralleling of AC Sources
    # NOTE: I am doing this extensively because the paper specifications do not make sense to me
    sys_safe.update({'!( (C1 != 0) & (C3 != 0) & (C2 != 0) )',
                    '!( (C1 != 0) & (C3 != 0) & (C4 != 0) & (C5 != 0) )',
                    '!( (C1 != 0) & (C3 != 0) & (C4 != 0) & (C7 != 0) & (C6 != 0) )',
                    '!( (C2 != 0) & (C4 != 0) & (C5 != 0) )',
                    '!( (C2 != 0) & (C4 != 0) & (C7 != 0) & (C6 != 0) )',
                    '!( (C5 != 0) & (C7 != 0) & (C6 != 0) )'})
    
    # Safety-Critical Buses
    # B1
    sys_safe.update({'(B1 = 0) -> (next(t1) = (t1 + 1))',
                    '(B1 = 1) -> (next(t1) = 0)',
                    't1 <= 5'})
    # B2
    sys_safe.update({'(B2 = 0) -> (next(t2) = (t2 + 1))',
                    '(B2 = 1) -> (next(t2) = 0)',
                    't2 <= 5'})
    # B3
    sys_safe.update({'(B3 = 0) -> (next(t3) = (t3 + 1))',
                    '(B3 = 1) -> (next(t3) = 0)',
                    't3 <= 5'})
    # B4
    sys_safe.update({'(B4 = 0) -> (next(t4) = (t4 + 1))',
                    '(B4 = 1) -> (next(t4) = 0)',
                    't4 <= 5'})
    
    # Unhealthy Sources
    sys_safe.update({'(GL = 0) -> (til_C1 = 0)',
                    '(AL = 0) -> (til_C2 = 0)',
                    '(AR = 0) -> (til_C5 = 0)',
                    '(GR = 0) -> (til_C6 = 0)'})
    
    # Prioritization
    sys_safe.update({'(GL = 1) -> (til_C1 = 1)',
                    '(GR = 1) -> (til_C6 = 1)'})
    sys_safe.update({'((GL = 0) & (AL = 1)) -> (til_C2 = 1)',
                    '((GR = 0) & (AR = 1)) -> (til_C5 = 1)'})
    
    # Other system specifications
    sys_init = {'(C1 = 1) & (C2 = 0) & (C5 = 0) & (C6 = 1) & (C3 = 1) & (C4 = 0) & (C7 = -1) & (til_C1 = 1) & (til_C2 = 0) & (til_C5 = 0) & (til_C6 = 1) & (til_C3 = 1) & (til_C4 = 0) & (til_C7 = -1) & (t1 = 0) & (t2 = 0) & (t3 = 0) & (t4 = 0) & (B1 = 1) & (B2 = 1) & (B3 = 1) & (B4 = 1)'}
    sys_prog = {}

    # Other environment specifications
    env_init = {'(GL = 1) & (GR = 1) & (AL = 1) & (AR = 1)'}
    env_prog = {}

    specs = tlp.spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                            env_safe, sys_safe, env_prog, sys_prog)
    # specs.qinit = '\A \E'
    specs.qinit = '\E \A'
    specs.moore = False
    # specs.moore = True
    print(specs.pretty())

    # spec = tlp.synth._spec_plus_sys(specs, None, sys, False, False)
    spec = tlp.synth._spec_plus_sys(specs, None, None, False, False)
    # Automaton class found in omega/omega/symbolic/temporal.py
    aut = omega_int._grspec_to_automaton(spec)

    # Graphing
    filename = path + "graph"
    attributes = ['color', 'shape']

    # Synthesize the controller
    # ctrl = tlp.synth.synthesize(specs, sys=sys)
    ctrl = tlp.synth.synthesize(specs)
    assert ctrl is not None, 'unrealizable'
    with open(path + "/ctrl", "wb") as file:
        pickle.dump(ctrl, file)

    dumpsmach.write_python_case(path + 'controller.py', ctrl, classname="sys_ctrl")
