import networkx as nx

def greedy_most_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.neighbors(env_node))
        num_red = (env_actions[0], 0)
        for sys_node in env_actions:
            if 'color' in g[sys_node]:
                transitions[env_node] = sys_node
                break
            counter = 0
            for sys_action in list(g.neighbors(sys_node)):
                if 'color' in g.nodes[sys_action]:
                    counter += 1
            if counter > num_red[1]:
                num_red = (sys_node, counter)
        transitions[env_node] = num_red[0]
    return transitions

def greedy_percent_red(g):
    env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    transitions = dict()
    for env_node in env_nodes:
        env_actions = list(g.neighbors(env_node))
        percent_red = (env_actions[0], 0)
        for sys_node in env_actions:
            if 'color' in g[sys_node]:
                transitions[env_node] = sys_node
                break
            counter = 0
            sys_actions = list(g.neighbors(sys_node))
            for sys_action in sys_actions:
                if 'color' in g.nodes[sys_action]:
                    counter += 1
            if counter/len(sys_actions) > percent_red[1]:
                percent_red = (sys_node, counter/len(sys_actions))
        transitions[env_node] = percent_red[0]
    return transitions