import datetime as dt
from typing import List
from matplotlib import pyplot as plt
import graph_functions
import lastfm_reader
from Scrobble import Scrobble
from lastfm_reader import read_scrobbles

FIG_WIDTH = 10
FIG_HEIGHT = 5


class ScrobblesError(Exception):
    """
    Custon exception class for errors related to scrobbles.
    Raised when invalid or insufficient scrobbles are passed to a function.
    """
    pass


def generate_graph(start: dt.datetime, end: dt.datetime, scrobbles: List[Scrobble], artists: List[str],
                   bin_width: dt.timedelta, mvg_avg_period: dt.timedelta = dt.timedelta(days=365),
                   graph_type="simple", plot_func=plt.plot, relative=None):
    """
    Generates and displays a graph of scrobbles for selected artists over time.

    :param start: The start date and time for the graph.
    :param end: The end date and time for the graph.
    :param scrobbles: A list of Scrobble objects, representing listening history.
    :param artists: A list of artist names to include in the graph.
    :param bin_width: The width of each time bin (e.g., daily, weekly) as a timedelta.
    :param mvg_avg_period: Period for moving average calculation, default is 365 days.
    :param graph_type: Type of graph: "simple" (default) or "cumulative".
    :param plot_func: Plotting function from matplotlib (e.g., plt.plot, plt.step).
    :param relative: If specified, plots relative to the nth scrobble.
    :return: None. Displays the graph.
    """
    bins = create_bins(start, end, bin_width)
    array = [{artist: 0 for artist in artists} for _ in range(len(bins))]
    bin_index = 0

    for scrobble in scrobbles:
        while scrobble.datetime > bins[bin_index]:
            bin_index += 1
        if scrobble.artist in array[bin_index]:
            array[bin_index][scrobble.artist] += 1

    if relative is None:
        x_axis = bins
    else:
        x_axis = []
        counter = 0
        for _ in bins:
            x_axis.append(counter)
            counter += 1
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    for artist in artists:
        y_axis = [array[i][artist] for i in range(len(bins))]
        if graph_type == "cumulative":
            y_axis = accumulate_array(y_axis)
        y_axis = moving_sum(y_axis, int(mvg_avg_period/bin_width))
        if relative is not None:
            # Find the index where the artist reaches the relative count
            threshold_index = next((i for i, v in enumerate(y_axis) if v >= relative), None)
            if threshold_index is None:
                continue  # skip artist if they never reach the threshold

            x_axis_shifted = [i - threshold_index for i in range(len(y_axis))]
            plot_func(x_axis_shifted, y_axis, label=artist)
        else:
            plot_func(x_axis[:len(y_axis)], y_axis, label=artist)

    if relative is not None and relative > 0:
        plt.title('Cumulative sum of scrobbles relative to ' + ordinal(relative) + ' scrobble')
        plt.xlabel('Days since ' + ordinal(relative) + ' scrobble')
    elif mvg_avg_period.days < len(bins):
        plt.title('Moving sum ({} days) of scrobbles of select artists over time'.format(mvg_avg_period.days))
    else:
        plt.title('Cumulative sum of scrobbles of select artists over time')
    plt.legend()
    plt.grid(True, linewidth=0.2)
    plt.show()


def graph_from_scrobbles(scrobbles: List[Scrobble], k=10, bin_width=dt.timedelta(days=1), graph_type="simple",
                         plot_func=plt.step, mvg_avg_period: dt.timedelta = dt.timedelta(days=365), addtl_artists=None,
                         relative=None):
    """
    Creates a graph from scrobbles, showing the listening frequency of top artists.

    :param scrobbles: List of Scrobble objects representing listening history.
    :param k: Number of top artists to include in the graph (default is 10).
    :param bin_width: Width of each time bin as a timedelta (e.g., 1 day).
    :param graph_type: Type of graph to display: "simple" or "cumulative".
    :param plot_func: Matplotlib plotting function to use (default is plt.step).
    :param mvg_avg_period: Period for moving average calculation, default is 365 days.
    :param addtl_artists: Additional artist names to include beyond the top k.
    :param relative: If specified, plots relative to the nth scrobble.
    :raises ScrobblesError: If no scrobbles are provided.
    :return: None. Displays the graph.
    """
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
    """
    Creates time bins between a start and end date, spaced by a specified width.

    :param start: Start date and time.
    :param end: End date and time.
    :param bin_width: Width of each bin as a timedelta.
    :return: A list of datetime objects representing the bin edges.
    """
    current = start
    bins = [start]
    while current < end:
        current += bin_width
        bins.append(current)
    return bins


def accumulate_array(array: List[int]):
    """
    Generates a cumulative sum of values from an input list.

    :param array: List of integers.
    :return: List of integers representing the cumulative sum.
    """
    cumulative = []
    running_total = 0
    for count in array:
        running_total += count
        cumulative.append(running_total)
    return cumulative


def moving_sum(array: List[int], period: int = 3):
    """
    Computes a moving sum over a list of integers with a specified period.

    :param array: List of integers.
    :param period: Number of elements to sum in each window (default is 3).
    :return: List of integers representing the moving sum.
    """
    moving = []
    for i in range(len(array)):
        start = max(0, i - period + 1)
        moving.append(sum(array[start:i + 1]))
    return moving


def ordinal(n: int):
    """
    Converts an integer to its ordinal string representation (e.g., 1 -> 1st, 2 -> 2nd).

    :param n: Integer value.
    :return: Ordinal representation of the integer as a string.
    """
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


if __name__ == '__main__':
    # array_simple = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # array_avged = moving_average(array_simple, 1)

    scrobbles = read_scrobbles('scrobbles-tynassty.csv')
    days = (max(scrobbles).datetime - min(scrobbles).datetime).days
    artists = []
    # artists.extend(["jacklen ro"])
    # artists.extend(["work wife"])
    graph_from_scrobbles(scrobbles, graph_type="simple", bin_width=dt.timedelta(days=1), plot_func=plt.step,
                         mvg_avg_period=dt.timedelta(days=365), k=10, addtl_artists=artists, relative=None)

    scrobbles = sorted(scrobbles)
    # s = dt.datetime.fromtimestamp(1503869636)
    # e = dt.datetime.fromtimestamp(1689577127)
    # generate_graph(s, e, scrobbles, ["Broods", "CHVRCHES"], 10000, graph_type="cumulative")
