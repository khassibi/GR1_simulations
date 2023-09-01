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

if __name__ == '__main__':
    path = 'random_graphs/'
    n = random.randint(6, 50)
    p = random.rand(1)[0] / 2 + 0.1
    num_red = random.randint(n//10, n//1.5)
    G = generate_G(n, p, True)
    G = rand_red_graph(G, num_red)
    pd = nx.drawing.nx_pydot.to_pydot(G)
    [left, right] = str(p).split('.')
    p_str = left + "_" + right[:3]
    filename = path + 'n' + str(n) + 'p' + p_str + 'red' + str(num_red) + 'graph'
    with open(filename, "wb") as file:
        pickle.dump(G, file)
    pd.write_pdf(filename + '.pdf')