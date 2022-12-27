import networkx as nx
import numpy as np
from time import perf_counter
def average_shortest_path_length(G: nx.Graph):
    adj_matrix = nx.to_numpy_array(G)
    n = adj_matrix.shape[0]
    D = np.full((n, n), np.inf)
    np.fill_diagonal(D, 0)
    D[adj_matrix != 0] = adj_matrix[adj_matrix != 0]
    for k in range(n):
        D = np.minimum(D, D[:,k,None] + D[None,k,:])
    total_length = np.sum(D[np.triu_indices(n, 1)])
    num_pairs = n * (n - 1) / 2
    return total_length / num_pairs


if __name__ == '__main__':
    K = nx.barabasi_albert_graph(1000,56)
    t = perf_counter()
    print(f'{nx.average_shortest_path_length(K)} {perf_counter()-t}')
    t = perf_counter()
    print(f'{average_shortest_path_length(K)} {perf_counter()-t}')
    """This Python code implements the same algorithm as the previous examples, but using NumPy for efficient matrix manipulation. 
    The average_shortest_path_length function takes an adjacency matrix as input and returns the average shortest path length of the graph represented by the matrix. 
    The function initializes a distance matrix D with all elements set to infinity, except for the diagonal elements, which are set to 0. 
    It then sets the non-zero elements of D to the corresponding elements of the adjacency matrix. 
    Finally, it iterates over the rows and columns of the distance matrix D, setting each element to the minimum of its current value and 
    the sum of the corresponding element in the ith row and kth column and the kth row and jth column. It then calculates the average shortest path length by 
    dividing the sum of the upper triangle of D (excluding the diagonal) by the number of pairs of nodes in the graph.
"""