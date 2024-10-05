import networkx as nx
from random import sample


def get_difference(A: nx.Graph, B: nx.Graph):
    return (A.number_of_edges() - B.number_of_edges())

def edge_rm(A: nx.Graph,n: int):
    if n<0:
        raise ValueError
    K = A.copy()
    edges_to_remove = sample(list(nx.edges(K)),n)
    if None in edges_to_remove:
        print('wha')
    for i in edges_to_remove:
        K.remove_edge(*i)
    if nx.is_connected(K) == False:
        return edge_rm(A,n)
    else:
        if K is None:
            return edge_rm(A,n)
        return K



if __name__ == '__main__':
    seed = nx.fast_gnp_random_graph(10,0.5)
    barabasi = nx.barabasi_albert_graph(100,5, initial_graph = seed)
    random_graph = nx.fast_gnp_random_graph(100,0.5)
    diff = get_difference(random_graph,barabasi)
    #print(get_difference(barabasi,random_graph))
    done = edge_rm(random_graph, 0)
    print(f'Barabasi edges {barabasi.number_of_edges()} Orginal random graph edges {random_graph.number_of_edges()} finished number of edges {done.number_of_edges()}')