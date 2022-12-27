from time import perf_counter
import networkx as nx
from betterdiameter import betterdiameter as betterdiameter
from betterdiameterJIT import betterdiameter as betterdiameterJIT
import numpy as np



if __name__ == '__main__':
    K1 = nx.barabasi_albert_graph(10000,56)
    K = nx.to_numpy_array(K1,dtype = np.float32)
    #t =perf_counter()
    #print(f'Networkx diameter result {nx.diameter(K1)} taking {perf_counter()-t} to complete')
    t = perf_counter()
    print(f'Base betterdiameter result {betterdiameter(K)} taking {perf_counter()-t} to complete')
    t = perf_counter()
    print(f'JIT betterdiameter result {betterdiameterJIT(K)} taking {perf_counter()-t} to complete')
    t = perf_counter()
    print(f'JIT betterdiameter result {betterdiameterJIT(K)} taking {perf_counter()-t} to complete')
    
    