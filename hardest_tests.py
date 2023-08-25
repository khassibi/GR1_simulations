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

def BFS_min_robustness(g):
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
    robustness = _robustness(g)
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

def average_robustness(g, ctrl):
    robustness = _robustness(g)
    sys_nodes = list(robustness.keys())
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]

    # Finding the nodes in which the liveness condition of left turn is satisfied
    liveness_nodes = []
    for (node, data) in g.nodes(data=True):
        if data['a9'] and data['shape'] == 'box':
            liveness_nodes.append(node)
    
    # Converting between ctrl and g nodes
    ctrl_to_g = dict()
    g_to_ctrl = dict()
    for (ctrl_node, ctrl_data) in ctrl.nodes(data=True):
        for sys_node in sys_nodes:
            sys_data = {k:v for k,v in g.nodes[sys_node].items() if k not in ['shape', 'color']}
            if sys_data == ctrl_data:
                ctrl_to_g[ctrl_node] = sys_node
                g_to_ctrl[sys_node] = ctrl_node
                break

    min_avg_robustness = len(g.nodes)
    hardest_test = None
    for liveness_node in liveness_nodes:
        if liveness_node not in g_to_ctrl:
            continue
        for path in list(nx.all_simple_paths(ctrl, 0, g_to_ctrl[liveness_node])):
            avg_robustness = 0
            for node in path:
                avg_robustness += robustness[ctrl_to_g[node]]
            avg_robustness /= len(path)
            if avg_robustness < min_avg_robustness:
                min_avg_robustness = avg_robustness
                hardest_test = path
    
    transitions = dict()
    transitions[0] = ctrl_to_g[hardest_test[0]]
    prev_env = 0
    for i in range(len(hardest_test) - 1):
        prev_env = ctrl_to_g[hardest_test[i]]

        env_node = ctrl_to_g[hardest_test[i + 1]]
        env_dict = {k:v for k,v in g.nodes[env_node].items() if k in ['vh', 'p', 'light']}
        
        sys_dict = {k:v for k,v in g.nodes[prev_env].items() if k not in ['vh', 'p', 'light']}
        sys_node_values = {**env_dict, **sys_dict}

        sys_node = None
        for node in g.successors(prev_env):
            if g.nodes[node] == sys_node_values:
                sys_node = node
                break
        transitions[sys_node] = env_node


        # env_dict = {k:v for k,v in g.nodes[prev_env].items() if k in ['vh', 'p', 'light', 'shape']}
        # sys_node = ctrl_to_g[hardest_test[i]]
        # sys_dict = {k:v for k,v in g.nodes[sys_node].items() if k not in ['vh', 'p', 'light', 'shape']}
        # env_node_values = {**env_dict, **sys_dict}
        # env_node = None
        # for node in env_nodes:
        #     if g.nodes[node] == env_node_values:
        #         env_node = node
        #         break
        # transitions[env_node] = sys_node
        # prev_env = env_node
    
    return transitions
