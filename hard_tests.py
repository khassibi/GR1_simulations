import networkx as nx

# Finding the metrics
def find_num_red_successors(g):
    '''
    Taking in graph `g` and returning a dictionary of the number of unsafe actions
    that each system node has.
    For system nodes that are red, they get a default value of the number of 
    nodes in g + 1. However, there should not be any red system nodes, so this 
    case should never happen. 
    '''
    sys_nodes = [node for node in g.nodes if 'box' in g.nodes[node]['shape']]
    value = dict()
    max_val = len(g.nodes) + 1

    for sys_node in sys_nodes:
        if 'color' in g.nodes[sys_node] and g.nodes[sys_node]['color'] == 'red':
            value[sys_node] = max_val
        else:
            count = 0
            for sys_action in list(g.successors(sys_node)):
                if 'color' in g.nodes[sys_action] and g.nodes[sys_action]['color'] == 'red':
                    count += 1
            value[sys_node] = count
    
    return value

def find_percent_red_successors(g):
    '''
    Taking in graph `g` and returning a dictionary of the percent of unsafe 
    actions that each system node has.
    For system nodes that are red, they get a default value of 1. However, there
    should not be any red system nodes, so this case should never happen. 
    '''
    sys_nodes = [node for node in g.nodes if 'box' in g.nodes[node]['shape']]
    value = dict()
    max_val = 1

    for sys_node in sys_nodes:
        if 'color' in g.nodes[sys_node] and g.nodes[sys_node]['color'] == 'red':
            value[sys_node] = max_val
        else:
            count = 0
            sys_actions = list(g.successors(sys_node))
            for sys_action in sys_actions:
                if 'color' in g.nodes[sys_action] and g.nodes[sys_action]['color'] == 'red':
                    count += 1
            value[sys_node] = count / len(sys_actions)
    
    return value

def find_min_robustness(g):
    '''
    Taking in graph `g` and returning a dictionary of the minimum robustness of 
    each environment node.
    The minimum robustness of a node s is defined as the minimum distance from 
    state s to any unsafe state. 
    If there is no path from a node to any unsafe node, then this node will have
    a robustness of the number of nodes in g + 1.
    '''
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    robustness = dict()
    
    max_val = len(g.nodes) + 1
    nodes_to_visit = set()
    for env_node in env_nodes:
        if 'color' in g.nodes[env_node] and g.nodes[env_node]['color'] == 'red':
            nodes_to_visit.add(env_node)
        else:
            robustness[env_node] = max_val

    # Start at red nodes and look at their neighbors, so on and so forth
    visited = nodes_to_visit.copy()
    distance = 0
    while nodes_to_visit:
        new_nodes_to_visit = set()
        for env_node in nodes_to_visit:
            robustness[env_node] = distance
            for sys_parent in list(g.predecessors(env_node)):
                for env_parent in list(g.predecessors(sys_parent)):
                    if env_parent not in visited:
                        new_nodes_to_visit.add(env_parent)
        visited.update(new_nodes_to_visit)
        nodes_to_visit = new_nodes_to_visit.copy()
        distance += 1
    
    return robustness

def find_avg_robustness(g):
    '''
    Taking in graph `g` and returning a dictionary of the average robustness of 
    each environment node.
    The minimum robustness of a node s is defined as the minimum distance from 
    state s to any unsafe state. 
    If there is no path from a node to any unsafe node, then this node will have
    a robustness of the number of nodes in g + 1.
    Nodes that are red will not be given an average robustness but will instead 
    have a robustness of 0. 
    '''
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    robustness = dict()
    
    max_val = len(g.nodes) + 1
    red_nodes = []
    non_red = []
    num_red = 0
    for env_node in env_nodes:
        if 'color' in g.nodes[env_node] and g.nodes[env_node]['color'] == 'red':
            robustness[env_node] = 0
            red_nodes.append(env_node)
            num_red += 1
        else:
            robustness[env_node] = max_val
            non_red.append(env_node)
    
    for node in non_red:
        sum = 0
        for red in red_nodes:
            if nx.has_path(g, node, red):
                sum += nx.shortest_path_length(g, source=node, target=red) / 2
        robustness[node] = sum / num_red
    
    return robustness
            


# Creating the tests
def memoryless_max_metric(g, sys_metric):
    '''
    Takes in a graph `g` and a metric on the system nodes `sys_metric`. 
    At each environment node, the environment transitions to the system
    successor node that has the largest metric value. 
    '''
    assert(type(sys_metric) == dict)
    transitions = dict()
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]

    for env_node in env_nodes:
        max_val = -1
        actions = []
        for sys_node in list(g.successors(env_node)):
            if sys_metric[sys_node] > max_val:
                max_val = sys_metric[sys_node]
                actions = [sys_node]
            elif sys_metric[sys_node] == max_val:
                actions.append(sys_node)
        transitions[env_node] = actions

    return transitions

def memoryless_robustness_minimization(g, env_robustness):
    '''
    Takes in a graph `g` and a robustness measure on the environment nodes 
    `env_robustness`.
    Starting at an environment node, the environment transitions to the 
    successor system node in which the maximum robustness value among 
    all of its successors is the smallest. 
    '''
    assert(type(env_robustness) == dict)
    transitions = dict()
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]

    infinity_ish = len(g.nodes) + 1
    for env_node in env_nodes:
        min_rob = infinity_ish
        actions = []
        max_rob = -1 # I am pretty sure I need to initialize max_rob here because of scope
        for sys_suc in list(g.successors(env_node)):
            max_rob = -1
            for env_suc in list(g.successors(sys_suc)):
                max_rob = max(max_rob, env_robustness[env_suc])
            # I tabbed the below one to the right
            if max_rob < min_rob:
                min_rob = max_rob
                actions = [sys_suc]
            elif max_rob == min_rob:
                actions.append(sys_suc)
        transitions[env_node] = actions
    
    return transitions
            
def memoryless_robustness_averaging(g, env_robustness):
    '''
    Takes in a graph `g` and a robustness measure on the environment nodes 
    `env_robustness`.
    Starting at an environment node, the environment transitions to the 
    successor system node in which the average robustness value among 
    all of its successors is the smallest. 
    '''
    assert(type(env_robustness) == dict)
    transitions = dict()
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]

    infinity_ish = len(g.nodes) + 1
    for env_node in env_nodes:
        min_rob = infinity_ish
        actions = []
        avg = 0
        for sys_suc in list(g.successors(env_node)):
            sum = 0
            env_successors = list(g.successors(sys_suc))
            for env_suc in env_successors:
                sum += env_robustness[env_suc]
            avg = sum / len(env_successors)
        if avg < min_rob:
            min_rob = avg
            actions = [sys_suc]
        elif sum == min_rob:
            actions.append(sys_suc)
        transitions[env_node] = actions
    
    return transitions