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
    path = 'patrolling_car_copy/'

    # Define the states of the system
    states = []
    for x in range(5):
        for y in range(5):
            states.append("c{}{}".format(x, y))
    
    # Variables
    env_vars = {'b': (0,4)}
    sys_vars = {'r': states,
                # 'fuel': (-1,8),
                'fuel': (-1,14),
                'move': 'boolean'
    }

    # Initialization
    # env_init = {'b=0'}
    env_init = {'b=2'}
    sys_init = {'r="c40"',
                # 'fuel=8',
                'fuel=14',
                '!move'
    }

    # Safety
    # # Blocker can self-loop
    # env_safe = {'(b=0) -> X((b=0) | (b=1))', 
    #             '(b=4) -> X((b=3) | (b=4))'}
    # for i in range(1,4):
    #     env_safe |= {'(b={0}) -> X((b={0}) | (b={1}) | (b={2}))'.format(i, i-1, i+1)}

    # Blocker cannot self-loop
    env_safe = {'(b=0) -> X(b=1)', 
                '(b=4) -> X(b=3)'}
    for i in range(1,4):
        env_safe |= {'(b={0}) -> X((b={1}) | (b={2}))'.format(i, i-1, i+1)}

    sys_safe = set()

    for x in range(1,4):
        sys_safe |= {'(r="c{}{}") -> (X(r="c{}{}") | (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move))'.format(x,0, x,0, x-1,0, x+1,0, x,1),
                    '(r="c{}{}") -> (X(r="c{}{}") | (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move))'.format(x,4,x,4, x-1,4, x+1,4, x,3),
                    '(r="c{}{}") -> (X(r="c{}{}") | (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move))'.format(0,x,0,x, 0,x+1, 0,x-1, 1,x),
                    '(r="c{}{}") -> (X(r="c{}{}") | (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move))'.format(4,x,4,x, 4,x+1, 4,x-1, 3,x)
        }
        for y in range(1,4):
            sys_safe |= {'(r="c{}{}") -> (X(r="c{}{}") | (X((r="c{}{}") | (r="c{}{}") | (r="c{}{}") | (r="c{}{}")) & X move))'.format(x,y,x,y, x+1,y, x-1,y, x,y+1, x,y-1)}

    # Corners
    sys_safe |= {'(r="c00") -> (X(r="c00") | (X((r="c10") | (r="c01")) & X move))',
                '(r="c40") -> (X(r="c40") | (X((r="c30") | (r="c41")) & X move))',
                '(r="c44") -> (X(r="c44") | (X((r="c34") | (r="c43")) & X move))',
                '(r="c04") -> (X(r="c04") | (X((r="c03") | (r="c14")) & X move))'
    }

    sys_safe |= {
                # 'X(r="c42") -> X(fuel = 8)', 
                'X(r="c42") -> X(fuel = 14)',
                #  '((r="c42") & move) -> X(fuel = (fuel - 1))',
                'X(fuel > -1)',
                # Decreasing fuel when moving
                '((X move) && (fuel=14) && !X(r="c42")) -> X(fuel = 13)',
                '((X move) && (fuel=13) && !X(r="c42")) -> X(fuel = 12)',
                '((X move) && (fuel=12) && !X(r="c42")) -> X(fuel = 11)',
                '((X move) && (fuel=11) && !X(r="c42")) -> X(fuel = 10)',
                '((X move) && (fuel=10) && !X(r="c42")) -> X(fuel = 9)',
                '((X move) && (fuel=9) && !X(r="c42")) -> X(fuel = 8)',
                '((X move) && (fuel=8) && !X(r="c42")) -> X(fuel = 7)',
                '((X move) && (fuel=7) && !X(r="c42")) -> X(fuel = 6)',
                '((X move) && (fuel=6) && !X(r="c42")) -> X(fuel = 5)',
                '((X move) && (fuel=5) && !X(r="c42")) -> X(fuel = 4)',
                '((X move) && (fuel=4) && !X(r="c42")) -> X(fuel = 3)',
                '((X move) && (fuel=3) && !X(r="c42")) -> X(fuel = 2)',
                '((X move) && (fuel=2) && !X(r="c42")) -> X(fuel = 1)',
                '(X (move) && (fuel=1) && !X(r="c42")) -> X(fuel = 0)',
                '(X (move) && (fuel=0) && !X(r="c42")) -> X(fuel = -1)',
                #  '(fuel=1) -> X(!move & fuel=1)',
                #  '(move && fuel<=2 && fuel<8 && !X(r="c42")) -> (X(fuel) = fuel - 1)',
                #  '(move && fuel=8 && !X(r="c42")) -> X(fuel = 7)'
                # Fuel staying the same when not moving
                '(!(X move) && (fuel=14)) -> X(fuel = 14)',
                '(!(X move) && (fuel=13)) -> X(fuel = 13)',
                '(!(X move) && (fuel=12)) -> X(fuel = 12)',
                '(!(X move) && (fuel=11)) -> X(fuel = 11)',
                '(!(X move) && (fuel=10)) -> X(fuel = 10)',
                '(!(X move) && (fuel=9)) -> X(fuel = 9)',
                '(!(X move) && (fuel=8)) -> X(fuel = 8)',
                '(!(X move) && (fuel=7)) -> X(fuel = 7)',
                '(!(X move) && (fuel=6)) -> X(fuel = 6)',
                '(!(X move) && (fuel=5)) -> X(fuel = 5)',
                '(!(X move) && (fuel=4)) -> X(fuel = 4)',
                '(!(X move) && (fuel=3)) -> X(fuel = 3)',
                '(!(X move) && (fuel=2)) -> X(fuel = 2)',
                '(!(X move) && (fuel=1)) -> X(fuel = 1)',
                '(!(X move) && (fuel=0)) -> X(fuel = 0)',
                '(!(X move) && (fuel=-1)) -> X(fuel = -1)'
        }
    for i in range(0,5):
        sys_safe |= {'!((r="c1{0}") & (b={0}))'.format(i),
                    '!((r="c1{0}") & X(b={0}))'.format(i)}
    # for i in range(1,4):
    #     sys_safe |= {'!((r="c1{}") & (b={}))'.format(i, i-1),
    #                  '!((r="c1{}") & (b={}))'.format(i, i+1)}
    # sys_safe |= {'!((r="c14") & (b=3))',
    #              '!((r="c10") & (b=1))'}
    
    # Progress
    # env_prog = set()
    env_prog = {'b=0'}
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

    print('made controller')

    # Graphing
    filename = path + "graph"
    attributes = ['color', 'shape']

    # Making a graph of the asynchronous GR(1) game with deadends.
    g0 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=False, append_non_visited=True, qinit=aut.qinit)
    print('got here')
    with open(filename, "wb") as file:
        pickle.dump(g0, file)
    print('dumped')
    h0 = gb._game_format_nx(g0, attributes)
    print('did h0')
    pd0 = nx.drawing.nx_pydot.to_pydot(h0)
    print('did pd0')
    pd0.write_pdf(path + 'game.pdf')
    print('wrote pd0')
    
    # # Making a graph of the asynchronous GR(1) game without deadends.
    # g1 = gb.game_graph(aut, env='env', sys='sys', remove_deadends=True, qinit=aut.qinit)
    # h1 = gb._game_format_nx(g1, attributes)
    # pd1 = nx.drawing.nx_pydot.to_pydot(h1)
    # pd1.write_pdf(path + 'game_no_deadends.pdf')

    # # Making a graph pf the state transitions of the environment and system
    # g2 = gb.state_graph(aut, env='env', sys='sys', qinit=aut.qinit)
    # h2, _ = gb._state_format_nx(g2, attributes)
    # pd2 = nx.drawing.nx_pydot.to_pydot(h2)
    # pd2.write_pdf(path + 'states.pdf')

if __name__ == '__main__':
    experiment()