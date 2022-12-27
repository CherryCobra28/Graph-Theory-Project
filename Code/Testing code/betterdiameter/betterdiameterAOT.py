import networkx as nx
import numpy as np
from numba.pycc import CC


cc =CC('betterdiameterAOT')
#def betterdiameter(G:nx.Graph):
#    A: int32[:,:] = nx.to_numpy_array(G)
#    return worker(A)

@cc.export('betterdiameterAOT','i4(f4[:,:])')
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
    cc.compile()