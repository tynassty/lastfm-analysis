import datetime as dt
from typing import List
from matplotlib import pyplot as plt

import graph_functions
from Scrobble import Scrobble
from lastfm_reader import read_scrobbles


def generate_graph(start: dt.datetime, end: dt.datetime, scrobbles: List[Scrobble], artists: List[str], bin_count=100,
                   graph_type="simple", plot_func=plt.plot):
    bins = create_bins(start, end, bin_count=bin_count)
    array = [{artist: 0 for artist in artists} for _ in range(bin_count)]
    bin_index = 0

    for scrobble in scrobbles:
        if scrobble.datetime > bins[bin_index]:
            bin_index += 1
        try:
            array[bin_index][scrobble.artist] += 1
        except KeyError:
            pass

    x_axis = bins
    plt.figure(figsize=(10, 5))
    for artist in artists:
        y_axis = [array[i][artist] for i in range(len(bins))]
        if graph_type == "cumulative":
            y_axis = accumulate_array(y_axis)
        plot_func(x_axis, y_axis, label=artist)
    plt.title('Scrobbles of top artists over time')
    plt.legend()
    plt.show()


def create_bins(start: dt.datetime, end: dt.datetime, bin_count=100):
    delta = end - start
    bin_length = delta / bin_count

    current = start
    bins = []
    for i in range(bin_count):
        current += bin_length
        bins.append(current)
    return bins


def accumulate_array(array: List[int]):
    cumulative = []
    running_total = 0
    for count in array:
        running_total += count
        cumulative.append(running_total)
    return cumulative


def graph_from_scrobbles(scrobbles: List[Scrobble], k=10, bin_count=100, graph_type="simple", plot_func=plt.plot):
    scrobbles = sorted(scrobbles)
    counts, _ = graph_functions.count_occurrences(scrobbles)
    artists = [artist_ct[0] for artist_ct in counts.most_common(k)]
    generate_graph(min(scrobbles).datetime, max(scrobbles).datetime, scrobbles, artists, bin_count=bin_count,
                   graph_type=graph_type, plot_func=plot_func)


if __name__ == '__main__':
    scrobbles = read_scrobbles('scrobbles-tynassty.csv')
    graph_from_scrobbles(scrobbles, graph_type="cumulative", bin_count=1000, plot_func=plt.step)

    # scrobbles = sorted(scrobbles)
    # s = dt.datetime.fromtimestamp(1503869636)
    # e = dt.datetime.fromtimestamp(1689577127)
    # generate_graph(s, e, scrobbles, ["Broods", "CHVRCHES"], 10000, graph_type="cumulative")