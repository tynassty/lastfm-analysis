import matplotlib.pyplot as plt
from matplotlib import ticker
import re

import lastfm_reader
import time_graph
from time_graph import create_bins, accumulate_array
from lastfm_reader import read_scrobbles


# Function to preprocess data and store results
def preprocess_scrobbles(file_path):
    # Read and sort scrobbles
    scrobbles = read_scrobbles(file_path)
    scrobbles = sorted(scrobbles)

    # Determine the time range and create time bins
    start = scrobbles[0].datetime
    end = scrobbles[-1].datetime
    bins = create_bins(start, end)

    # Initialize tracking data structures
    artists = {scrobble.artist for scrobble in scrobbles}
    scr_dict = {artist: [0] * len(bins) for artist in artists}
    rank_dict = {artist: [0] * len(bins) for artist in artists}
    cumul_dict = {}

    # Bin scrobbles by time and artist
    bin_index = 0
    for scrobble in scrobbles:
        while scrobble.datetime > bins[bin_index]:
            bin_index += 1
        scr_dict[scrobble.artist][bin_index] += 1

    # Calculate cumulative scrobbles
    for artist in scr_dict.keys():
        cumul_dict[artist] = accumulate_array(scr_dict[artist])

    # for artist in scr_dict.keys():
    #     cumul_dict[artist] = time_graph.moving_sum(scr_dict[artist], 365)

    # Rank artists by cumulative scrobbles in each bin
    for i in range(len(bins)):
        scrs = [(a, cumul_dict[a][i]) for a in artists]
        sorted_scrs = sorted(scrs, key=lambda x: -x[1])
        for j in range(len(artists)):
            rank_dict[sorted_scrs[j][0]][i] = j + 1

    return bins, rank_dict, artists


# Pre-process scrobbles once and store the result
bins, rank_dict, artists = preprocess_scrobbles('scrobbles-tynassty.csv')

# for artist in artists:
#     if rank_dict[artist][-1] == min(rank_dict[artist]):
#         print(rank_dict[artist][-1], artist)

for artist in artists:
    if min(rank_dict[artist]) <= 2:
        print(artist)
