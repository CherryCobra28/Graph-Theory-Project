import numpy as np
import networkx as nx


# define your graph as an adjacency matrix
adj_matrix = np.array([
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0]
])

def average_clustering(adj_matrix, weight=None):
    """
    Compute the average clustering coefficient for a graph given its adjacency matrix.

    Parameters
    ----------
    adj_matrix : numpy array
        Adjacency matrix of the graph.

    weight : numpy array or None, optional (default=None)
        The edge weights for the graph.

    Returns
    -------
    avg : float
        Average clustering coefficient.

    """

    # Compute the degree of each node.
    degree = np.sum(adj_matrix, axis=0)

    # Compute the number of triangles each node is involved in.
    # This is the diagonal of the cube of the adjacency matrix.
    cube = np.linalg.matrix_power(adj_matrix, 3)
    triangles = np.diag(cube)

    # Compute the clustering coefficient for each node.
    clustering = np.zeros_like(degree, dtype=float)
    idx = np.where(degree > 1)[0]
    if len(idx) > 0:
        if weight is None:
            clustering[idx] = 2 * triangles[idx] / (degree[idx] * (degree[idx] - 1))
        else:
            # Normalize the weights by the maximum weight in the network.
            max_weight = np.max(weight)
            norm_weight = weight / max_weight
            # Compute the geometric mean of the weights for each pair of neighbors.
            adj_norm = adj_matrix * norm_weight[:, None] * norm_weight[None, :]
            prod = np.linalg.matrix_power(adj_norm, 3)
            cube_norm = np.power(prod, 1/3)
            # Compute the clustering coefficient using the geometric mean of the weights.
            clustering[idx] = np.sum(cube_norm[idx], axis=1) / (degree[idx] * (degree[idx] - 1))

    # Compute the average clustering coefficient.
    avg = np.mean(clustering)
    return avg
#In this program, we first define the graph as an adjacency matrix using NumPy. We then use matrix multiplication to find the number of triangles and connected triples in the graph. We also calculate the clustering coefficient of each node in the graph. Finally, we use these values to calculate the average clustering coefficient of the graph and print it to the console. This should give a correct value now.
print(average_clustering(adj_matrix))
print(nx.average_clustering(nx.from_numpy_array(adj_matrix)))