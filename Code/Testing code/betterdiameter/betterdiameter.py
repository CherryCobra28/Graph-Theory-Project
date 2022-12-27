from time import perf_counter
import networkx as nx
import numpy as np


def betterdiameter(A: np.array) -> int:
    

    dimensions = A.shape
    
    A += np.identity(dimensions[0],int)
    const_A = A.copy()
    t=1
    for _ in range(100):

        x = np.count_nonzero(A)
        #print(A)
        
        if x == dimensions[0]**2:
            return t
            
        else:
            t += 1
            A = np.dot(A,const_A)
            A = (A>0).astype(np.uint8)
            #A = ne.evaluate('A>0').astype(np.uint8)

if __name__ == '__main__':
    K = nx.barabasi_albert_graph(10000,15)
    K = nx.to_numpy_array(K)
    
    t = perf_counter()
    my = betterdiameter(K)
    print(f'My algoirthim took {perf_counter() - t},{my=}')
    t = perf_counter()
    network = nx.diameter(K)
    print(f'Netwrokx took {perf_counter()-t},{network=}')

