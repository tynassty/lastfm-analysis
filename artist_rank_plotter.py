import matplotlib.pyplot as plt
from matplotlib import ticker
import re

import lastfm_reader
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

    # Rank artists by cumulative scrobbles in each bin
    for i in range(len(bins)):
        scrs = [(a, cumul_dict[a][i]) for a in artists]
        sorted_scrs = sorted(scrs, key=lambda x: -x[1])
        for j in range(len(artists)):
            rank_dict[sorted_scrs[j][0]][i] = j + 1

    return bins, rank_dict, artists


# Pre-process scrobbles once and store the result
bins, rank_dict, artists = preprocess_scrobbles('scrobbles-tynassty.csv')


# Function to plot multiple artists' ranks
def plot_multiple_artists(artists, bins, rank_dict):
    valid_artists = []
    for artist in artists:
        if artist in rank_dict:
            plt.plot(bins, rank_dict[artist], label=artist)
            # plt.step(bins, rank_dict[artist], label=artist)
            valid_artists.append(artist)
        else:
            print(f"Artist '{artist}' not found in the data.")

    if valid_artists:
        plt.gca().invert_yaxis()  # Keep the ranking order (1 at the top)
        plt.yscale('log')  # Set y-axis to logarithmic scale
        plt.grid(True, which='major')  # Grid for major and minor ticks
        plt.legend()
        plt.show()
    else:
        print("No valid artists to plot.")


# Example usage with multiple artists:
current_artist_list = []

while True:
    # Input artists separated by commas
    artist_input = input("Enter artist names to plot (comma-separated, or 'exit' to quit): ")
    if artist_input.lower() == 'exit':
        break

    if artist_input and artist_input[0] == "+":
        artist_input = artist_input[1:]
    else:
        current_artist_list = []

    # Split input into a list of artists
    current_artist_list.extend([lastfm_reader.clean_text(artist) for artist in artist_input.split(',')])

    # Plot the selected artists
    plot_multiple_artists(current_artist_list, bins, rank_dict)
