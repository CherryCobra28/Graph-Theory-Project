import networkx as nx
import numpy as np
from numba import jit

@jit
def average_shortest_path(G: nx.Graph) -> float:
    # Convert the graph to a NumPy array
    A = nx.to_numpy_array(G)
    # Initialize the distance matrix with the graph adjacency matrix
    D = A.copy()
    # Set the distance between nodes connected by an edge to 1
    D[D > 0] = 1
    # Set the distance between a node and itself to 0
    np.fill_diagonal(D, 0)
    # Get the number of nodes in the graph
    n = D.shape[0]
    # Initialize a path count matrix with zeros
    P = np.zeros((n, n))
    # Fill the path count matrix with the number of paths between nodes
    for i in range(n):
        for j in range(n):
            if D[i, j] != np.inf:
                P[i, j] = 1
    # Use the Floyd-Warshall algorithm to find the shortest paths
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i, j] > D[i, k] + D[k, j]:
                    D[i, j] = D[i, k] + D[k, j]
                    P[i, j] = P[i, k] + P[k, j]
    # Calculate the average shortest path length
    total_length = np.sum(D)
    total_paths = np.sum(P)
    return total_length / total_paths
