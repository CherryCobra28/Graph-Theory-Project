import networkx as nx
from time import perf_counter



def test(x):
    t = perf_counter()
    g = nx.erdos_renyi_graph(int(x/2),0.5)
    print(f'time: {perf_counter()-t}')
    t = perf_counter()
    f = nx.fast_gnp_random_graph(int(x/2),0.5)
    print(f'time: {perf_counter()-t}')
    
    
    
if __name__ == '__main__':
    test(1000)
