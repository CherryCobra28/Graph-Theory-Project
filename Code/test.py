import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.barabasi_albert_graph(12,1)
print(f'{nx.average_shortest_path_length(G)=}')
print(f'{nx.sigma(G)=}')
print(f'{nx.degree_histogram(G)=}')
A =  nx.degree_histogram(G)
print(dict(enumerate(A)))

subax1 = plt.subplot(121)
nx.draw(G,with_labels=True)

plt.show()