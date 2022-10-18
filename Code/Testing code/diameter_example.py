from time import perf_counter
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def mydiameter(G):
    A = nx.to_numpy_matrix(G)

    dimensions = A.shape
    A += np.identity(dimensions[0],int)
    t=1
    while True:

        x = np.count_nonzero(A)
        print(A)
        
        if x == dimensions[0]**2:
            return t
            
        else:
            t += 1
            A = A*A
            

k = nx.complete_graph(2)
K = nx.barabasi_albert_graph(10,1,initial_graph = k)
#nx.draw(K)
#plt.show()
#input()
A = nx.to_numpy_matrix(K)
dimensions = A.shape
A += np.identity(dimensions[0],int)
V = nx.from_numpy_matrix(A)
#nx.draw(V)
#plt.show()
#input()

t = perf_counter()
my = mydiameter(K)
print(f'My algoirthim took {perf_counter() - t},{my=}')

t = perf_counter()
network = nx.diameter(K)
print(f'Netwrokx took {perf_counter()-t},{network=}')

