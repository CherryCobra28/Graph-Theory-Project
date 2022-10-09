import cProfile
import pstats
from sirdbmodel import main, infection_graph, infect, random


def perf():
    with cProfile.Profile() as pr:
                main(10000,5,0.2,0.9,0.01,'False')
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')


if __name__ == '__main__':
    perf()