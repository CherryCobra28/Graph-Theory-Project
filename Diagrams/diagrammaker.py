import networkx as nx
import matplotlib.pyplot as plt
import pickle
import pathlib as path


colours = ['blue', 'blue', 'blue','blue','red']
G = nx.complete_graph(3)
nx.draw(G)
plt.show()

G.add_node(3)    
G.add_edge(1,3)
G.add_edge(2,3)
nx.draw(G)
plt.show()
G.add_node(4)
G.add_edge(0,4)
G.add_edge(2,4)
nx.draw(G,node_color=colours)
plt.show()
#print(nx.average_shortest_path_length(G))
#G_Degree = dict(nx.degree(G))
#colours = []
#for key in G_Degree:
#    if G_Degree[key] < 5:
#        colours.append('blue')
#    else:
#        colours.append('green')        





#plt.subplot(111)
