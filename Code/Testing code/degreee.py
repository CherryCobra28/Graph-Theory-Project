import networkx as nx
import pandas as pd


A = nx.fast_gnp_random_graph(10,0.5)

B = nx.barabasi_albert_graph(1000000,5,initial_graph =A)
L = nx.degree_histogram(B)
data = pd.Series(L)
data.to_csv('degree.csv')
