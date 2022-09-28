import numpy as np
import networkx as nx
from time import perf_counter
import matplotlib.pyplot as plt



A = np.matrix('0 1 0 1 5;1 0 1 0 1;0 1 0 1 1;1 0 1 0 1;5 1 1 1 0')
G = nx.from_numpy_matrix(A)
mapping = {0:'A',1:'B',2:'C',3:'D',4:'E'}
G = nx.relabel_nodes(G,mapping)
F = nx.erdos_renyi_graph(5,0.9)
F = nx.relabel_nodes(F,mapping)
#time1 = perf_counter()
#nx.approximation.traveling_salesman_problem(G)
#time2 = perf_counter()
#total = time2 - time1
#print(f'{total=}')
##print(nx.approximation.christofides(G))
subax1 = plt.subplot(121)
nx.draw(F,with_labels=True)
#subax2 = plt.subplot(122)
#nx.draw_shell(G,with_labels=True)
plt.show()