import networkx as nx
import random as rand
import matplotlib.pyplot as plt
from copy import deepcopy
def birth(graph,b_r):
    #r = rand.randrange(0,101)
    #if r < 100*b_r:
    nodes = list(nx.nodes(graph))
    new_node = len(nodes)
    T = True
    while T is True:
        parent_1, parent_2 = random(nodes)[0],random(nodes)[1]
        if parent_1 != parent_2:
            T = False
    connect = list(nx.neighbors(graph,parent_2))
    if parent_1 not in connect:
        graph.add_edge(parent_1,parent_2)


    graph.add_node(new_node) 
    graph.add_edge(parent_1,new_node)
    graph.add_edge(parent_2,new_node)
    return f'{new_node=},between {parent_1} and {parent_2}'
    

def random(node):
    r1 = rand.randrange(0,len(node))
    r2 = rand.randrange(0,len(node))
    return r1,r2





G = nx.barabasi_albert_graph(5,1)
cp_G = deepcopy(G)
print(birth(G,1))
print(birth(G,1))
print(birth(G,1))
print(birth(G,1))

f = plt.figure('Starting Graph')
subax1 = plt.subplot(121)
nx.draw(cp_G,with_labels=True)
f.show()
g = plt.figure('The Surviors')
subax1 = plt.subplot(121)
nx.draw(G,with_labels=True)
g.show()
input()




