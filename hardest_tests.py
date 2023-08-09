import networkx as nx

def greedy_most_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.successors(env_node))
        if len(env_actions) == 0:
            transitions[env_node] = -1
            continue
        transitions[env_node] = [sys_node for sys_node in env_actions if 'color' in g[sys_node]]
        if len(transitions[env_node]) > 0:
            continue
        num_red = dict()
        for sys_node in env_actions:
            counter = 0
            for sys_action in list(g.successors(sys_node)):
                if 'color' in g.nodes[sys_action]:
                    counter += 1
            num_red[sys_node] = counter
        transitions[env_node] = [sys_node for sys_node in env_actions if num_red[sys_node] == max(num_red.values())]
    return transitions

def greedy_percent_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.successors(env_node))
        if len(env_actions) == 0:
            transitions[env_node] = -1
            continue
        transitions[env_node] = [sys_node for sys_node in env_actions if 'color' in g[sys_node]]
        if len(transitions[env_node]) > 0:
            continue
        percent_red = dict()
        for sys_node in env_actions:
            counter = 0
            sys_actions = list(g.successors(sys_node))
            for sys_action in sys_actions:
                if 'color' in g.nodes[sys_action]:
                    counter += 1
            percent_red[sys_node] = counter /len(sys_actions)
        transitions[env_node] = [sys_node for sys_node in env_actions if percent_red[sys_node] == max(percent_red.values())]
    return transitions

# Robustness: phi_r(s) is the length of the minimal path from s to any unsafe state
def _robustness(g):
    shortest_paths = dict(nx.all_pairs_shortest_path_length(g))
    sys_nodes = [node for node in g.nodes if 'box' in g.nodes[node]['shape']]
    red_nodes = [node for node in g.nodes if 'color' in g.nodes[node]]
    
    robustness = dict()
    total_nodes = len(g.nodes)
    for sys_node in sys_nodes:
        robustness[sys_node] = total_nodes
        for red_node in red_nodes:
            if red_node in shortest_paths[sys_node]:
                if (shortest_paths[sys_node])[red_node] < robustness[sys_node]:
                    robustness[sys_node] = (shortest_paths[sys_node])[red_node]
    return robustness

def greedy_min_robustness(g):
    # For each environment node, find its robustness
    # Choose transitions in this way
    # TODO: Probably have to code a liveness condition 
    robustness = _robustness(g)
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.successors(env_node))
        transitions[env_node] = []
        min_robustness = len(g.nodes)
        for env_action in env_actions:
            if robustness[env_action] == min_robustness:
                transitions[env_node].append(env_action)
            elif robustness[env_action] < min_robustness:
                min_robustness = robustness[env_action]
                transitions[env_node] = [env_action]
    return transitions

def BFS_most_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.successors(env_node))
        if len(env_actions) == 0:
            transitions[env_node] = -1
            continue
        num_red = dict()
        for sys_node in env_actions:
            bfs_edges = list(nx.bfs_edges(g, source=sys_node))
            bfs_nodes = [sys_node] + [v for _, v in bfs_edges]
            counter = 0
            for node in bfs_nodes:
                if 'color' in g.nodes[node]:
                    counter += 1
            num_red[sys_node] = counter
        transitions[env_node] = [sys_node for sys_node in env_actions if num_red[sys_node] == max(num_red.values())]
    return transitions

def BFS_percent_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.successors(env_node))
        if len(env_actions) == 0:
            transitions[env_node] = -1
            continue
        percent_red = dict()
        for sys_node in env_actions:
            bfs_edges = list(nx.bfs_edges(g, source=sys_node))
            bfs_nodes = [sys_node] + [v for _, v in bfs_edges]
            counter = 0
            for node in bfs_nodes:
                if 'color' in g.nodes[node]:
                    counter += 1
            percent_red[sys_node] = counter / len(bfs_nodes)
        transitions[env_node] = [sys_node for sys_node in env_actions if percent_red[sys_node] == max(percent_red.values())]
    return transitions
