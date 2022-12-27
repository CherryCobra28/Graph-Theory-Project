import networkx as nx
import numpy as np
from copy import copy
from numba import jit

@jit
def betterdiameter(G: nx.Graph) -> int:
    A = nx.to_numpy_array(G)
    dimensions = A.shape
    A += np.identity(dimensions[0], int)
    const_A = A.copy()
    t = 1
    for _ in range(100):
        x = np.count_nonzero(A)
        if x == dimensions[0]**2:
            return t
        else:
            t += 1
            A = np.dot(A, const_A)
            A = (A > 0).astype(np.uint8)
