try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence
import copy
from itertools import chain
import logging

import networkx as nx

from omega.games import gr1

from omega.logic import syntax as stx
from omega.symbolic import prime as prm
from omega.symbolic import symbolic

from omega.games import enumeration as enum
from omega.symbolic import enumeration as sym_enum

log = logging.getLogger(__name__)  # TODO: see if this logger even works if I am calling enum functions too

def _init_search(g, aut, umap, keys, qinit):
    """Enumerate initial states according to `qinit`."""
    # danger of blowup due to sparsity
    # implement enumerated equivalent to compare
    if qinit == '\A \E':
        queue, visited = _forall_exist_init(g, aut, umap, keys)
    elif qinit == '\A \A':
        queue, visited = _forall_init(g, aut, umap, keys)
    elif qinit == '\E \E':
        queue, visited = _exist_init(g, aut, umap, keys)
    elif qinit == '\E \A':
        queue, visited = _exist_forall_init(g, aut, umap, keys)
    else:
        raise Exception('unknown qinit "{q}"'.format(q=qinit))
    log.info('{n} initial nodes'.format(n=len(queue)))
    return queue, visited

def _forall_exist_init(g, aut, umap, keys):
    r"""Enumerate initial states with \A env:  \E sys vars.

    Note that each initial "state" is a class of
    initial states in ZF set theory.
    """
    env_init = aut.init['env']
    sys_init = aut.init['sys']
    assert env_init != aut.false
    assert sys_init != aut.false
    # `env_init` should not depend on sys vars
    only_env_init = aut.exist(aut.varlist['sys'], env_init)
    env_iter = aut.pick_iter(
        only_env_init, care_vars=aut.varlist['env'])
    visited = aut.false
    queue = list()
    for env_0 in env_iter:
        u = aut.let(env_0, sys_init)
        sys_0 = aut.pick(u, care_vars=aut.varlist['sys'])
        d = dict(env_0)
        d.update(sys_0)
        # confirm `sys_0` picked properly
        u = aut.let(d, env_init)
        assert u == aut.true, u
        enum._add_new_node({**d, **{'shape': 'oval'}}, g, queue, umap, keys)
        visited = enum._add_to_visited(d, visited, aut)
    return queue, visited

def _forall_init(g, aut, umap, keys):
    r"""Enumerate initial states with \A \A vars."""
    env_init = aut.init['env']
    sys_init = aut.init['sys']  # to constrain only the
        # initial value of the internal memory variables
    assert env_init != aut.false
    care_vars = chain(aut.varlist['env'], aut.varlist['sys'])
    init_iter = aut.pick_iter(
        env_init & sys_init,
        care_vars=list(care_vars))
    visited = aut.false
    queue = list()
    for d in init_iter:
        enum._add_new_node({**d, **{'shape': 'oval'}}, g, queue, umap, keys)
        visited = enum._add_to_visited(d, visited, aut)
    return queue, visited

def _exist_init(g, aut, umap, keys):
    r"""Enumerate initial states with \E env, sys vars."""
    sys_init = aut.init['sys']
    assert sys_init != aut.false
    care_vars = chain(aut.varlist['env'], aut.varlist['sys'])
    d = aut.pick(
        sys_init,
        care_vars=list(care_vars))
    visited = aut.false
    queue = list()
    enum._add_new_node({**d, **{'shape': 'oval'}}, g, queue, umap, keys)
    visited = enum._add_to_visited(d, visited, aut)
    return queue, visited

def _exist_forall_init(g, aut, umap, keys):
    r"""Enumerate initial states with \E sys:  \A env vars."""
    # this function can be merged with `_forall_exist_init`
    # by constraining initial sys assignments,
    # then enumerating the same way
    env_init = aut.init['env']
    sys_init = aut.init['sys']
    assert env_init != aut.false
    assert sys_init != aut.false
    # pick `sys_0` so that it work for all
    # env assignments allowed by `env_init`
    u = aut.forall(aut.varlist['env'], sys_init)
    assert u != aut.false
    sys_0 = aut.pick(u, care_vars=aut.varlist['sys'])
    # iterate over env initial assignments
    # allow `EnvInit` that depends on sys vars (Mealy env)
    env_iter = aut.pick_iter(
        env_init, care_vars=aut.varlist['env'])
    visited = aut.false
    queue = list()
    for env_0 in env_iter:
        d = dict(env_0)
        d.update(sys_0)
        # confirm `sys_0` works for all `env_0`
        u = aut.let(d, env_init)
        assert u == aut.true, u
        enum._add_new_node({**d, **{'shape': 'oval'}}, g, queue, umap, keys)
        visited = enum._add_to_visited(d, visited, aut)
    return queue, visited

def game_graph(aut, env, sys, remove_deadends, append_non_visited=False, qinit='\A \A'):
    _aut = copy.copy(aut)
    _aut.moore = aut.moore
    _aut.plus_one = aut.plus_one
    _aut.varlist.update(
        env=aut.varlist[env],
        sys=aut.varlist[sys])
    _aut.init.update(
        env=aut.init[env],
        sys=aut.init[sys])
    _aut.action.update(
        env=aut.action[env],
        sys=aut.action[sys])
    _aut.prime_varlists()
    g = _game_graph(_aut, qinit, append_non_visited)
    if remove_deadends:
        return _remove_deadends(g)
    return g

def _game_graph(aut, qinit, append_non_visited):
    print('about to create game graph')
    winning_set, _, __ = gr1.solve_streett_game(aut)
    print('found winning set')

    assert aut.action['sys'] != aut.false
    primed_vars = enum._primed_vars_per_quantifier(aut.varlist)
    vrs = set(aut.varlist['env']).union(aut.varlist['sys'])
    unprime_vars = {stx.prime(var): var for var in vrs}
    # fix an order for tupling
    keys = list(vrs)
    keys.append('shape')
    umap = dict()  # map assignments -> node numbers
    g = nx.MultiDiGraph()
    queue, visited = _init_search(g, aut, umap, keys, qinit)
    g.initial_nodes = set(queue)
    varnames = set(vrs)
    symbolic._assert_support_moore(aut.action['sys'], aut)
    # search
    print('before queue')
    added_to_queue = set(queue)
    iter = 0
    while queue:
        iter += 1
        # print(len(added_to_queue), iter)
        node = queue.pop()
        values = {key: val for key, val in g.nodes[node].items() 
                  if key not in ['color', 'shape']}
        log.debug('at node: {d}'.format(d=values))
        assert set(values) == varnames, (values, varnames)
        check_bdd = aut.let(values, winning_set)
        if check_bdd == aut.false:
            g.nodes[node]['color'] = 'red'
            continue
        u = aut.action['env']
        u = aut.let(values, u)
        # apply Mealy controller function
        env_iter = aut.pick_iter(
            u, care_vars=primed_vars['env'])
        u = aut.action['sys']
        assert u != aut.false
        sys = aut.let(values, u)
        if sys == aut.false:
            g.nodes[node]['color'] = 'red'
            continue
        for next_env in env_iter:
            log.debug('next_env: {r}'.format(r=next_env))
            # no effect if `aut.moore`
            u = aut.let(next_env, sys)
            u = aut.let(unprime_vars, u)
            env_values = {unprime_vars[var]: value
                          for var, value in next_env.items()}
            v = aut.let(env_values, visited)
            # v, _ = _select_candidate_nodes(
            #     u, v, aut, visited=True)  # u is the next nodes and v is the visited nodes
            v, _ = _select_candidate_nodes(
                u, v, aut, visited=False)  # TODO: See how visited=True/False differ
            sys_iter = aut.pick_iter(
                v, care_vars=aut.varlist['sys'])

            # Adding node with next environment action
            # we want to take the system values from the node that pointed to this environment
            # BUT only if that node was from a system move
            d_env = dict(env_values)
            d_sys = dict((k, values[k]) for k in set(aut.varlist['sys']))
            d = {**d_env, **d_sys}
            # assert
            u = aut.let(d, visited)
            assert u == aut.true or u == aut.false
            # find or add node
            env_node, already_visited = _get_node({**d, **{'shape': 'box'}}, g, umap, keys)  # TODO: maybe I don't need to check to find the node
            check_bdd = aut.let(d, winning_set)
            # if check_bdd == aut.false:
            #     g.nodes[env_node]['color'] = 'red'
            #   TODO: if unnecessary, comment out the rest
            if not already_visited:
                visited = enum._add_to_visited(d, visited, aut)
            c = remove_redundant_propositions(d_env)
            g.add_edge(node, env_node, key="env", color='orange', label=c)
            
            log.debug((
                'next env: {e}\n'
                'current sys: {s}\n').format(
                e=env_values,
                s=d_sys))

            for next_sys in sys_iter:
                # Adding node with next system action
                d = {**d_env, **next_sys}
                # assert
                u = aut.let(d, visited)
                assert u == aut.true or u == aut.false
                # find or add node
                sys_node, already_visited = _get_node({**d, **{'shape': 'oval'}}, g, umap, keys)  # TODO: maybe I don't need to check to find the node
                check_bdd = aut.let(d, winning_set)
                if check_bdd == aut.false:
                    g.nodes[sys_node]['color'] = 'red'
                if not already_visited:
                    visited = enum._add_to_visited(d, visited, aut)
                    if append_non_visited:
                        queue.append(sys_node)
                        added_to_queue.add(sys_node)
                # Add a system node to the queue as long as the transition to it is unique
                if not g.has_edge(env_node, sys_node, key='sys'):
                    c = remove_redundant_propositions(next_sys)
                    g.add_edge(env_node, sys_node, key="sys", color='blue', label=c)
                    if not append_non_visited:
                        queue.append(sys_node)
                        added_to_queue.add(sys_node)

                log.debug((
                    'next env: {e}\n'
                    'next sys: {s}\n').format(
                    e=env_values,
                    s=next_sys))

    return g

def _select_candidate_nodes(
        next_nodes, visited_nodes, aut, visited=True):
    """Return set of next nodes to choose from, as BDD."""
    u = next_nodes
    v = visited_nodes
    # prefer already visited nodes ?
    if visited:
        v &= u
        if v == aut.false:
            log.info('cannot remain in visited nodes')
            v = u
            remain = False
        else:
            remain = True
    else:
        v = u & ~ v
        if v == aut.false:
            log.info('cannot visit new nodes')
            v = u
            remain = True
        else:
            remain = False
    # assert v != aut.false
    # TODO: see if I need this assertion
    return v, remain

def _remove_deadends(graph):
    dead_ends = [1]
    while dead_ends:
        dead_ends = [node for node in graph.nodes() if graph.out_degree(node) == 0]
        graph.remove_nodes_from(dead_ends)
    return graph


def state_graph(aut, env, sys, qinit='\A \A'):
    r"""Return enumerated graph with steps as edges.

    Only `aut.init['env']` considered.
    The predicate `aut.init['sys']` is ignored.

    `qinit` has different meaning that in `omega.games.gr1`.
    Nonetheless, for synthesized `aut.init['env']`,
    the meaning of `qinit` here yields the expected result.

    Enumeration is done based on `qinit`:

    - `'\A \A'`: pick all states that satisfy `aut.init[env] /\ aut.init[sys]`,
      where the conjunct `aut.init[sys]` is included for the internal variables

    - `'\E \E'`: pick one state that satisfies `aut.init[sys]`

    - `'\A \E'`: for each environment state `x` that satisfies
      `\E y:  aut.init[env]`,
      pick a system state `y` that satisfies `aut.init[sys]`

    - `'\E \A'`: pick a system state `y` that satisfies
      `\A x:  aut.init[sys]`,
      and enumerate all environment states `x` that satisfy `aut.init['env']`.
    """
    _aut = copy.copy(aut)
    _aut.moore = aut.moore
    _aut.plus_one = aut.plus_one
    _aut.varlist.update(
        env=aut.varlist[env],
        sys=aut.varlist[sys])
    _aut.init.update(
        env=aut.init[env],
        sys=aut.init[sys])
    _aut.action.update(
        env=aut.action[env],
        sys=aut.action[sys])
    _aut.prime_varlists()
    return _state_graph(_aut, qinit)

def _state_graph(aut, qinit):
    winning_set, _, __ = gr1.solve_streett_game(aut)

    assert aut.action['sys'] != aut.false
    primed_vars = enum._primed_vars_per_quantifier(aut.varlist)
    vrs = set(aut.varlist['env']).union(aut.varlist['sys'])
    unprime_vars = {stx.prime(var): var for var in vrs}
    # fix an order for tupling
    keys = list(vrs)
    umap = dict()  # map assignments -> node numbers
    g = nx.MultiDiGraph()
    queue, visited = enum._init_search(g, aut, umap, keys, qinit)
    g.initial_nodes = set(queue)
    varnames = set(keys)
    symbolic._assert_support_moore(aut.action['sys'], aut)
    # search
    while queue:  # TODO: check if omega combines all the states into one or if it skips some
        node = queue.pop()
        values = {key: val for key, val in g.nodes[node].items() 
                  if key not in ['color']}
        log.debug('at node: {d}'.format(d=values))
        assert set(values) == varnames, (values, varnames)
        check_bdd = aut.let(values, winning_set)
        if check_bdd == aut.false:
            g.nodes[node]['color'] = 'red'
            continue
        u = aut.action['env']
        u = aut.let(values, u)
        # apply Mealy controller function
        env_iter = aut.pick_iter(
            u, care_vars=primed_vars['env'])
        u = aut.action['sys']
        assert u != aut.false
        sys = aut.let(values, u)
        if sys == aut.false:
            g.nodes[node]['color'] = 'red'
            continue
        for next_env in env_iter:
            log.debug('next_env: {r}'.format(r=next_env))
            # no effect if `aut.moore`
            u = aut.let(next_env, sys)
            u = aut.let(unprime_vars, u)
            env_values = {unprime_vars[var]: value
                          for var, value in next_env.items()}
            v = aut.let(env_values, visited)
            v, _ = _select_candidate_nodes(
                u, v, aut, visited=True)  # u is the next nodes and v is the visited nodes
            sys_iter = aut.pick_iter(
                v, care_vars=aut.varlist['sys'])

            # Adding node with next environment action
            # we want to take the system values from the node that pointed to this environment
            # BUT only if that node was from a system move
            d_env = dict(env_values)
            d_sys = dict((k, values[k]) for k in set(aut.varlist['sys']))
            d = {**d_env, **d_sys}
            # assert
            u = aut.let(d, visited)
            assert u == aut.true or u == aut.false
            # find or add node
            env_node, already_visited = _get_node(d, g, umap, keys)
            check_bdd = aut.let(d, winning_set)
            # if check_bdd == aut.false:
                # g.nodes[env_node]['color'] = 'red'
                # TODO: If I realize I don't need this, delete the code above that is unnecessary
            if not already_visited:
                visited = enum._add_to_visited(d, visited, aut)
            c = remove_redundant_propositions(d_env)
            g.add_edge(node, env_node, key="env", color='orange', label=c)
            
            log.debug((
                'next env: {e}\n'
                'current sys: {s}\n').format(
                e=env_values,
                s=d_sys))

            for next_sys in sys_iter:
                # Adding node with next system action
                d = {**d_env, **next_sys}
                # assert
                u = aut.let(d, visited)
                assert u == aut.true or u == aut.false
                # find or add node
                sys_node, already_visited = _get_node(d, g, umap, keys)
                check_bdd = aut.let(d, winning_set)
                if check_bdd == aut.false:
                    g.nodes[sys_node]['color'] = 'red'
                if not already_visited:
                    visited = enum._add_to_visited(d, visited, aut)
                # Add a system node to the queue as long as the transition to it is unique
                if not g.has_edge(env_node, sys_node, key='sys'):
                    c = remove_redundant_propositions(next_sys)
                    g.add_edge(env_node, sys_node, key="sys", color='blue', label=c)
                    queue.append(sys_node)

                log.debug((
                    'next env: {e}\n'
                    'next sys: {s}\n').format(
                    e=env_values,
                    s=next_sys))

    return g

def _get_node(d, g, umap, keys):
    """Add node to or find node in graph `g` for the assignment `d`."""
    assert isinstance(keys, Sequence), keys
    key = enum._node_tuple(d, keys)
    if key in umap:
        return umap[key], True
    u = len(g)
    assert u not in g, u
    g.add_node(u, **d)
    umap[key] = u
    log.debug(d)
    return u, False

def remove_redundant_propositions(dict):
    """Remove redundant propositions from `dict`
    and return a list of strings of the non-redundant variable assignments.

    @type dict: `dict`
    """
    c = []
    for k, v in dict.items():
        if type(v) == bool:
            if v:
                c.append(str(k))
        elif k not in ['color', 'loc', 'eloc', 'shape']:
            c.append('{var}={val}'.format(var=k, val=v))
    return c

def _game_format_nx(g, attributes=[]):
    """Return game graph ready to be dumped.

    Nodes with same label over `keys` are identified.
    Edge attributes are copied.

    @type g: `networkx.MultiDiGraph`
    @param keys: `list` of keys in node attributes `dict` to
        show as label, in the given order.
        Attributes outside `keys` remain attributes.
        By default all keys are shown.
    @rtype: `pydot.Graph`
    """
    h = nx.MultiDiGraph()
    for u, d in g.nodes(data=True):
        c = remove_redundant_propositions(d)
        s = sym_enum._square_conj(c)
        attr = {k: v for k, v in d.items() if k in attributes}
        attr.update(label=s)
        h.add_node(u, **attr)
    for u, v, attr in g.edges(data=True):
        h.add_edge(u, v, **attr)
    assert len(g) == len(h), (g.nodes, h.nodes, len(g), len(h))
    return h

def _state_format_nx(g, attributes=[]):
    """Return graph ready to be dumped, where each state is a unique node.

    Nodes with same label over `keys` are identified.
    Edge attributes are copied.

    @type g: `networkx.MultiDiGraph`
    @param keys: `list` of keys in node attributes `dict` to
        show as label, in the given order.
        Attributes outside `keys` remain attributes.
        By default all keys are shown.
    @rtype: `pydot.Graph`
    """
    h = nx.MultiDiGraph()
    umap = dict()
    for u, d in g.nodes(data=True):
        c = remove_redundant_propositions(d)
        s = sym_enum._square_conj(c)
        attr = {k: v for k, v in d.items() if k in attributes}
        h.add_node(s, **attr)
        umap[u] = s
    for u, v, attr in g.edges(data=True):
        us = umap[u]
        vs = umap[v]
        h.add_edge(us, vs, **attr)
    assert len(g) >= len(h), (g.nodes, h.nodes)
    assert len(g) == len(umap), (g.nodes, umap)
    return h, umap

