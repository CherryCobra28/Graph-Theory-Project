import networkx
import itertools
def gnp_random_graph(n, p, seed=None):
    edges = itertools.combinations(range(n), 2)
    G = networkx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return networkx.complete_graph(n, create_using=G)

    for e in edges:
        if seed.random() < p:
            G.add_edge(*e)
    return G
