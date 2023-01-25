from time import perf_counter
import networkx as nx
import numpy as np
from copy import copy



def betterdiameter(G: nx.Graph) -> int:
    """This function calculates the diameter of a graph using matrix multiplications.
    
    It does this by the following fact:
    Let A be the adjacency matrix of a graph
    It can be seen that A^k where k is an integer that if the entries of A are greater then 0 it is possible to reach that node in k steps
    Thus the smallest k s.t. all the entries of A are greater than 0 k is the diameter of the graph
    
    

    Args:
        G (nx.Graph): The graph we would like to test

    Returns:
        int: The diameter of the graph
    """    
    A = nx.to_numpy_array(G) #This is the adjancency matrix of G
    dimensions = A.shape #We take the dimensions of A
    np.fill_diagonal(A,1) #Here we add the identity matrix to A, we do this to add self loops to the graph, we do this to make sure that at odd number steps we can get back to the orginal node so the entry is not 0
    const_A = copy(A)#This is equal to A and will not change as we need this to raise A to successive powers
    t=1 #The miniumn diameter of a graph must be 1
    if not nx.is_connected(G) is True:# if the graph is disconncetd its diamter is infinite
        return np.inf #infinity
    
    for _ in range(1000): #We interate this for 1000 trials
        x = np.count_nonzero(A) #This counts how many non zeros are in the matrix
        if x == dimensions[0]**2: #If the number of nonzeros is equal to the size of the matrix, all values are non zero
            return t #retunr the diameter
        else:
            t += 1 #Increate t by 1
            A = A @ const_A #raise A to 1 higher power
            A = (A>0).astype(np.uint8)#for all entries greater than 0 make them size unint8 and set them to 1. as we only care if the entry is greater than 0 and the entries will get large in size we set them to 1 to make it quicker

if __name__ == '__main__':
    K = nx.barabasi_albert_graph(10,7)
    
    
    t = perf_counter()
    my = betterdiameter(K)
    print(f'My algoirthim took {perf_counter() - t},{my=}')
    t = perf_counter()
    network = nx.diameter(K)
    print(f'Netwrokx took {perf_counter()-t},{network=}')

