from time import perf_counter
import networkx as nx
import numpy as np
from copy import copy



def betterdiameter(G: nx.Graph) -> int:
    A = nx.to_numpy_array(G)
    dimensions = A.shape
    np.fill_diagonal(A,1)
    const_A = copy(A)
    t=1
    for _ in range(100):
        x = np.count_nonzero(A)
        if x == dimensions[0]**2:
            return t
        else:
            t += 1
            A = np.dot(A,const_A)
            A = (A>0).astype(np.uint8)
            

if __name__ == '__main__':
    K = nx.barabasi_albert_graph(10,7)
    
    
    t = perf_counter()
    my = betterdiameter(K)
    print(f'My algoirthim took {perf_counter() - t},{my=}')
    t = perf_counter()
    network = nx.diameter(K)
    print(f'Netwrokx took {perf_counter()-t},{network=}')

