from time import perf_counter
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

def betterdiameter(G):
    A = nx.to_numpy_matrix(G)

    dimensions = A.shape
    
    A += np.identity(dimensions[0],int)
    const_A = copy(A)
    t=1
    while True:

        x = np.count_nonzero(A)
        #print(A)
        
        if x == dimensions[0]**2:
            return t
            
        else:
            t += 1
            A = A*const_A
            

if __name__ == '__main__':
    K = nx.barabasi_albert_graph(10000,700)
    
    
    t = perf_counter()
    my = betterdiameter(K)
    print(f'My algoirthim took {perf_counter() - t},{my=}')
    
    t = perf_counter()
    network = nx.diameter(K)
    print(f'Netwrokx took {perf_counter()-t},{network=}')

