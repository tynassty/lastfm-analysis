from collections import Counter
import datetime as dt
import graph_functions
import time_graph
from Scrobble import filter_by_key
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx
import time


def top_chart_maker(scrobbles, k=10, attribute='artist', fancy=False):
    counts, occurrence_list = graph_functions.count_occurrences(scrobbles, attribute=attribute)
    to_return = ""
    max_len = ""
    if fancy:
        max_len = max([len(s[0]) for s in counts.most_common(k)])
    for count in counts.most_common(k):
        if fancy:
            to_return += "{1:>{max_len}}: {0:6,d}\n".format(count[1], count[0], max_len=max_len)
        else:
            to_return += count[0] + "\n"

    return to_return[:-1]


def top_chart_by_first_letter():
    """
    a function that will calculate the top artist starting with each letter of the alphabet and each number 0-9
    prints results to console
    :return: none
    """
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
               "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    to_print = ""
    for letter in letters:
        scrobbles_letter = [scr for scr in scrobbles if scr.artist[0] == letter]
        to_print = to_print + top_chart_maker(scrobbles_letter, k=1) + "\n"
    print(to_print)


if __name__ == "__main__":
    scrobbles = read_scrobbles('scrobbles-tynassty.csv')
    scrobbles = sorted(scrobbles)

    scrobbles = [scr for scr in scrobbles if scr.datetime.year == 2024]
    # scrobbles = [scr for scr in scrobbles if scr.datetime.month == 9]
    # scrobbles = [scr for scr in scrobbles if scr.datetime.weekday() == 6]
    # scrobbles = [scr for scr in scrobbles if scr.datetime.hour == 23]

    top_chart = top_chart_maker(scrobbles, 20, attribute="track", fancy=False)
    print(top_chart)

