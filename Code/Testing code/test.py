import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pysnooper import snoop



def main():
    G = nx.barabasi_albert_graph(10,3)
    print(f'{nx.average_shortest_path_length(G)=}')
    #print(f'{nx.sigma(G)=}')
    print(f'{nx.degree_histogram(G)=}')
    A =  nx.degree_histogram(G)
    print(nx.to_numpy_array(G))
    print(dict(enumerate(A)))

    subax1 = plt.subplot(121)
    nx.draw(G,with_labels=True)

    plt.show()


main()