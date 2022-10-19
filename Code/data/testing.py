from __future__ import barry_as_FLUFL
from betterdiameter import betterdiameter
from time import perf_counter
import networkx as nx


A = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500,10000]


for i in A:
    G = nx.barabasi_albert_graph(i,5)
    t = perf_counter()
    print(betterdiameter(G))
    print(f'{i=},time = {perf_counter() - t},')

