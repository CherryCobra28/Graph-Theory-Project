import networkx as nx
from betterdiameter import betterdiameter
import math
G = nx.fast_gnp_random_graph(10,0.5)

G = nx.barabasi_albert_graph(1500,5,initial_graph = G)


N = len(G.nodes())

approx = math.log(N)/math.log(math.log(N))
diameter = betterdiameter(G)
print(f'{diameter=},av_path = {nx.average_shortest_path_length(G)},{approx=}')



