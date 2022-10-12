import cProfile
import pstats
import sirdmodel


def perf():
    with cProfile.Profile() as pr:
                sirdmodel.main(100,5,0.2,0.9,'False')
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')


if __name__ == '__main__':
    perf()