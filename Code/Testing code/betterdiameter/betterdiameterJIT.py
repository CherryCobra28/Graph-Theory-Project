import networkx as nx
import numpy as np
from numba import njit

#def betterdiameter(G:nx.Graph):
#    A: int32[:,:] = nx.to_numpy_array(G)
#    return worker(A)

@njit
def betterdiameter(A) -> int:
    dimensions = A.shape
    #A += np.eye(dimensions[0],dtype=np.float)
    np.fill_diagonal(A,1)
    const_A = A.copy()
    t = 1
    for _ in range(100):
        x = np.count_nonzero(A)
        if x == dimensions[0]**2:
            return t
        else:
            t += 1
            A = np.dot(A, const_A)
            A = (A > 0).astype(np.float32)


if __name__ =='__main__':
    K = nx.barabasi_albert_graph(100,20)
    K = nx.to_numpy_array(K,dtype = np.float32)
    print(betterdiameter(K))