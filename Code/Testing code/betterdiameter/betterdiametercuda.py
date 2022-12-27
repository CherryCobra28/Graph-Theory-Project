import networkx as nx
import numpy as np
from copy import copy
from numba import cuda

@cuda.jit
def betterdiameter_kernel(A, const_A, t):
    i = cuda.grid(1)
    if i < A.shape[0]:
        x = cuda.atomic.add(t, 1)
        if np.count_nonzero(A) == A.shape[0]**2:
            t[0] = x
        else:
            A[i, :] = A[i, :] @ const_A[:, :]
            A[i, :] = (A[i, :] > 0).astype(np.uint8)

def betterdiameter(G: nx.Graph) -> int:
    A = nx.to_numpy_array(G)
    dimensions = A.shape
    A += np.identity(dimensions[0], int)
    const_A = A.copy()
    t = np.array([0], dtype=np.int32)
    threadsperblock = 256
    blockspergrid = (A.shape[0] + (threadsperblock - 1)) // threadsperblock
    betterdiameter_kernel[blockspergrid, threadsperblock](A, const_A, t)
    return t[0]



