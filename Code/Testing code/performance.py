import cProfile
import pstats

import networkx as nx

def perf():
    #G = nx.barabasi_albert_graph(10000,10)
    with cProfile.Profile() as pr:
                #betterdiameter.betterdiameter(G)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')


if __name__ == '__main__':
    perf()