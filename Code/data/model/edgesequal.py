import networkx as nx
import random

def edge_rm(G: nx.Graph,edge: tuple):
    K = G.copy()
    K.remove_edge(*edge)
    if nx.is_connected(K):
        return K
    else:
        return None

def set_edges(rgraph: nx.Graph,bgraph: nx.Graph) -> int:
    #assumes rgraph has more edges then bgraph
    rgraph_edges = rgraph.number_of_edges()
    bgraph_edges = bgraph.number_of_edges()
    if rgraph_edges == bgraph_edges:
        return 0
    no_edges_to_rm = rgraph_edges - bgraph_edges
    edges_to_rm = random.sample(sorted(bgraph.edges()), no_edges_to_rm)
    A = bgraph.copy()
    for i in edges_to_rm:
        
        A = edge_rm(A,i)
        if A is None:
            set_edges(rgraph,bgraph)
    return A
    

g = nx.barabasi_albert_graph(20,5)
l = nx.gnp_random_graph(20,0.5)
k = set_edges(l,g)
print(k.number_of_edges())
print(g.number_of_edges(),l.number_of_edges())