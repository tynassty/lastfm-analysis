import datetime as dt
from typing import List
from matplotlib import pyplot as plt
import graph_functions
import lastfm_reader
from Scrobble import Scrobble
from lastfm_reader import read_scrobbles


class ScrobblesError(Exception):
    pass


def generate_graph(start: dt.datetime, end: dt.datetime, scrobbles: List[Scrobble], artists: List[str],
                   bin_width: dt.timedelta, mvg_avg_period: dt.timedelta = dt.timedelta(days=365),
                   graph_type="simple", plot_func=plt.plot, relative=False):
    bins = create_bins(start, end, bin_width)
    array = [{artist: 0 for artist in artists} for _ in range(len(bins))]
    bin_index = 0

    for scrobble in scrobbles:
        while scrobble.datetime > bins[bin_index]:
            bin_index += 1
        try:
            array[bin_index][scrobble.artist] += 1
        except KeyError:
            pass
        except IndexError:
            pass

    if not relative:
        x_axis = bins
    else:
        x_axis = []
        counter = 0
        for i in bins:
            x_axis.append(counter)
            counter += 1
    plt.figure(figsize=(10, 5))
    for artist in artists:
        y_axis = [array[i][artist] for i in range(len(bins))]
        if graph_type == "cumulative":
            y_axis = accumulate_array(y_axis)
        y_axis = moving_sum(y_axis, int(mvg_avg_period/bin_width))
        if relative:
            y_axis2 = []
            found_non_zero = False
            for num in y_axis:
                if num > 0:
                    found_non_zero = True
                if found_non_zero:
                    y_axis2.append(num)
            y_axis = y_axis2
        plot_func(x_axis[:len(y_axis)], y_axis, label=artist)
    if relative:
        plt.title('Cumulative sum of scrobbles relative to first listen')
    else:
        plt.title('Moving sum of scrobbles of top artists over time')
    plt.legend()
    plt.show()


def graph_from_scrobbles(scrobbles: List[Scrobble], k=10, bin_width=dt.timedelta(days=1), graph_type="simple",
                         plot_func=plt.step, mvg_avg_period: dt.timedelta = dt.timedelta(days=365), addtl_artists=None,
                         relative=False):
    if len(scrobbles) <= 0:
        raise ScrobblesError("No scrobbles passed to graph_from_scrobbles")
    if addtl_artists is None:
        addtl_artists = []
    addtl_artists = [lastfm_reader.clean_text(artist) for artist in addtl_artists]
    scrobbles = sorted(scrobbles)
    counts, _ = graph_functions.count_occurrences(scrobbles)
    artists = [artist_ct[0] for artist_ct in counts.most_common(k)]
    artists.extend(addtl_artists)
    generate_graph(min(scrobbles).datetime, max(scrobbles).datetime, scrobbles, artists, bin_width=bin_width,
                   graph_type=graph_type, plot_func=plot_func, mvg_avg_period=mvg_avg_period, relative=relative)


def create_bins(start: dt.datetime, end: dt.datetime, bin_width=dt.timedelta(days=1)):
    current = start
    bins = []
    while current < end:
        current += bin_width
        bins.append(current)
    return bins


def accumulate_array(array: List[int]):
    cumulative = []
    running_total = 0
    for count in array:
        running_total += count
        cumulative.append(running_total)
    return cumulative


def moving_sum(array: List[int], period: int = 3):
    moving = []
    for i in range(len(array)):
        start = max(0, i - period + 1)
        moving.append(sum(array[start:i + 1]))
    return moving


if __name__ == '__main__':
    # array_simple = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # array_avged = moving_average(array_simple, 1)

    scrobbles = read_scrobbles('scrobbles-tynassty.csv')
    days = (max(scrobbles).datetime - min(scrobbles).datetime).days
    graph_from_scrobbles(scrobbles, graph_type="simple", bin_width=dt.timedelta(days=1), plot_func=plt.plot,
                         mvg_avg_period=dt.timedelta(days=90), k=10, addtl_artists=[])

    # scrobbles = sorted(scrobbles)
    # s = dt.datetime.fromtimestamp(1503869636)
    # e = dt.datetime.fromtimestamp(1689577127)
    # generate_graph(s, e, scrobbles, ["Broods", "CHVRCHES"], 10000, graph_type="cumulative")
