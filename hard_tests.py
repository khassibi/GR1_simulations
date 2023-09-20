import networkx as nx

# Finding the metrics
def num_red_successors(g):
    '''
    Taking in graph g and returning a dictionary of the number of unsafe actions
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

def percent_red_successors(g):
    '''
    Taking in graph g and returning a dictionary of the percent of unsafe 
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
    Taking in graph g and returning a dictionary of the minimum robustness of 
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
    Taking in graph g and returning a dictionary of the average robustness of 
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
def greedy_max_metric(g, sys_metric):
    '''
    Takes in a graph and a metric on the system nodes. 
    At each environment node, the environment transitions to the system
    successor node that has the largest metric value. 
    '''
    assert(type(sys_metric) == dict)
    transitions = dict()
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]

    for env_node in env_nodes:
        max = -1
        actions = []
        for sys_node in list(g.successors(env_node)):
            if sys_metric[sys_node] > max:
                max = sys_metric[sys_node]
                actions = [sys_node]
            elif sys_metric[sys_node] == max:
                actions.append(sys_node)
        transitions[env_node] = actions

    return transitions


