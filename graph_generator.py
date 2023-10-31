# make red nodes have no outgoing edges
# make non-red nodes have at least 1 outgoing edge
# have that not be a thing too
# X include the boxes and circles >> jk I don't need to. I can count a state as an env + a sys

import networkx as nx
import numpy as np
from numpy import random
from visualization import graph_builder as gb
import pickle

def generate_G(n,p, two_player=False):
    G=nx.DiGraph()
    for node in range(n):
        G.add_node(node)
        if two_player:
            if np.random.uniform() < np.random.uniform():
                G.nodes[node]['shape'] = 'box'
            else:
                G.nodes[node]['shape'] = 'oval'

    for i in range(n):
        for j in range(i+1, n):
            if two_player:
                if G.nodes[i]['shape'] == G.nodes[j]['shape']:
                    continue
            if np.random.uniform() < p:
                G.add_edge(i,j)

    return G

def rand_red_graph(G, num_red):
    red_nodes = random.choice(list(G.nodes), size=num_red, replace=False)
    for node in G.nodes:
        if node in red_nodes:
            G.nodes[node]['color'] = 'red'
    return G

def add_remove_edges(G):  
    for node in G.nodes:
        if 'color' in G.nodes[node] and G.nodes[node]['color'] == 'red':        
            # Removing all outgoing edges from node
            out_edges = [(u, v) for u, v in G.edges if u == node]
            G.remove_edges_from(out_edges)
        else:
            while G.out_degree(node) <= 0:
                neighbor = random.choice(list(G.nodes))
                if 'color' in G.nodes[neighbor] and G.nodes[neighbor]['color'] == 'red': 
                    continue
                else:
                    G.add_edge(node,neighbor)
    
    return G

def find_min_robustness(g):
    '''
    Taking in graph `g` and returning a dictionary of the minimum robustness of 
    each environment node.
    The minimum robustness of a node s is defined as the minimum distance from 
    state s to any unsafe state. 
    If there is no path from a node to any unsafe node, then this node will have
    a robustness of the number of nodes in g + 1.
    '''
    # env_nodes = [node for node in g.nodes if 'oval' in g.nodes[node]['shape']]
    robustness = dict()
    
    max_val = len(g.nodes) + 1
    nodes_to_visit = set()
    for node in g.nodes:
        if 'color' in g.nodes[node] and g.nodes[node]['color'] == 'red':
            nodes_to_visit.add(node)
        else:
            robustness[node] = max_val

    # Start at red nodes and look at their neighbors, so on and so forth
    visited = nodes_to_visit.copy()
    distance = 0
    while nodes_to_visit:
        new_nodes_to_visit = set()
        for node in nodes_to_visit:
            robustness[node] = distance
            for node_parent in list(g.predecessors(node)):
                if node_parent not in visited:
                    new_nodes_to_visit.add(node_parent)
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
    robustness = dict()
    
    max_val = len(g.nodes) + 1
    red_nodes = []
    non_red = []
    num_red = 0
    for node in g.nodes:
        if 'color' in g.nodes[node] and g.nodes[node]['color'] == 'red':
            robustness[node] = 0
            red_nodes.append(node)
            num_red += 1
        else:
            robustness[node] = max_val
            non_red.append(node)
    
    if num_red == 0:
        return robustness
    
    for node in non_red:
        sum = 0
        for red in red_nodes:
            if nx.has_path(g, node, red):
                sum += nx.shortest_path_length(g, source=node, target=red) / 2
        robustness[node] = sum / num_red
    
    return robustness

def equiv_robs(rob):
    sorted_min_rob_keys = sorted(rob, key=rob.get)
    val = rob[sorted_min_rob_keys[0]]
    outer_list = []
    inner_list = []
    for key in sorted_min_rob_keys:
        if rob[key] == val:
            inner_list.append(key)
        else:
            val = rob[key]
            outer_list.append(inner_list.copy())
            inner_list = []
    
    return outer_list
    
def check_equal(A, B):
    if len(A) != len(B):
        return False
    
    for idx in range(len(A)):
        if set(A[idx]) != set(B[idx]):
            return False
        
    return True


if __name__ == '__main__':
    num_iters = 100
    for __ in range(num_iters):
        path = 'random_graphs/'
        n = random.randint(6, 50)
        p = random.rand(1)[0] / 2 + 0.1
        num_red = random.randint(n//10, n//1.5)
        G = generate_G(n, p)
        G = rand_red_graph(G, num_red)
        G = add_remove_edges(G)
        min_rob = find_min_robustness(G)
        avg_rob = find_avg_robustness(G)
        equiv_min_rob = equiv_robs(min_rob)
        equiv_avg_rob = equiv_robs(avg_rob)
        if not check_equal(equiv_min_rob, equiv_avg_rob):
            pd = nx.drawing.nx_pydot.to_pydot(G)
            [left, right] = str(p).split('.')
            p_str = left + "_" + right[:3]
            filename = path + 'n' + str(n) + 'p' + p_str + 'red' + str(num_red) + 'graph'
            with open(filename, "wb") as file:
                pickle.dump(G, file)
            pd.write_pdf(filename + '.pdf')