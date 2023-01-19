import cProfile
import pstats

import networkx as nx
from sirdmodel import model

def perf():
    G = nx.barabasi_albert_graph(1000,10)
    with cProfile.Profile() as pr:
                model(G,0.5,0.6)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')


if __name__ == '__main__':
    perf()