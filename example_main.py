from caanalyzer.analyzer import Analyzer
from sys import argv
import caanalyzer.agg as agg
import numpy as np
import matplotlib.pyplot as plt


def main():
    the_thing = Analyzer(output_raw=False)
    repo_obj = the_thing.analyze(argv[1])
    aggregated_file_data = agg.scalek(repo_obj['file_objs'], 3)

    # now we have 3 of our most common files represented by
    # median length and corresponding line info.
    print(aggregated_file_data[0][:, 0])
    # plot file length vs line for 1st file cluster

    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis

    ax.yaxis.set_ticks(
        np.arange(0, aggregated_file_data[0].shape[0]//2, aggregated_file_data[0].shape[0] // 10))  # set y-ticks
    ax.yaxis.tick_left()
    plt.plot(aggregated_file_data[2][:, 3], aggregated_file_data[2][:, 0])

    plt.plot(aggregated_file_data[2][:, 1], aggregated_file_data[2][:, 0])

    plt.show()


if __name__ == "__main__":
    main()
