import csv

import matplotlib.pyplot as plt
from matplotlib import ticker
import re

import lastfm_reader
from time_graph import create_bins, accumulate_array
from lastfm_reader import read_scrobbles


# Function to preprocess data and store results
def preprocess_scrobbles(scrobbles):
    """
    Preprocesses scrobble data for analysis by binning scrobbles by time,
    calculating cumulative scrobbles, and ranking artists based on their cumulative
    scrobbles in each time bin.

    :param scrobbles: List of scrobble objects. Each scrobble should have:
                      - `datetime`: A timestamp of when the scrobble occurred.
                      - `artist`: The name of the artist associated with the scrobble.
    :return: A tuple containing:
             - bins: List of time bin boundaries.
             - rank_dict: Dictionary mapping each artist to a list of ranks
                          (one per bin) based on their cumulative scrobbles.
             - artists: Set of unique artist names from the scrobbles.
    """
    # Sort scrobbles by datetime
    scrobbles = sorted(scrobbles)

    # Determine the time range and create time bins
    earliest_scr = scrobbles[0].datetime  # Earliest scrobble
    latest_scr = scrobbles[-1].datetime  # Latest scrobble
    bins = create_bins(earliest_scr, latest_scr)  # Function to create time bins based on earliest_scr and latest_scr

    # Initialize tracking data structures
    artists = {scrobble.artist for scrobble in scrobbles}  # Unique set of artists
    scr_dict = {artist: [0] * len(bins) for artist in artists}  # Unique set of artists
    rank_dict = {artist: [0] * len(bins) for artist in artists}  # Artist ranks per bin
    cumul_dict = {}  # Cumulative scrobbles for each artist

    # Bin scrobbles by time and artist
    bin_index = 0
    for scrobble in scrobbles:
        # Move to the correct bin for the current scrobble
        while scrobble.datetime > bins[bin_index]:
            bin_index += 1
        scr_dict[scrobble.artist][bin_index] += 1  # Increment scrobble count in the bin

    # Calculate cumulative scrobbles
    for artist in scr_dict.keys():
        cumul_dict[artist] = accumulate_array(scr_dict[artist])  # Helper to compute cumulative sums

    # Rank artists by cumulative scrobbles in each bin
    for i in range(len(bins)):
        # Collect cumulative scrobbles for this bin
        scrs = [(a, cumul_dict[a][i]) for a in artists]
        # Sort artists by cumulative scrobbles in descending order
        sorted_scrs = sorted(scrs, key=lambda x: -x[1])
        # Assign ranks based on sorted order
        rank = 1
        for j in range(len(sorted_scrs)):
            if j > 0 and sorted_scrs[j][1] == sorted_scrs[j - 1][1]:
                # If tied with the previous artist, assign the same rank
                rank_dict[sorted_scrs[j][0]][i] = rank
            else:
                # Update rank for non-tied scrobbles
                rank = j + 1
                rank_dict[sorted_scrs[j][0]][i] = rank

    return bins, rank_dict, artists


# Pre-process scrobbles once and store the result
scrobbles = read_scrobbles('scrobbles-tynassty.csv')
bins, rank_dict, artists = preprocess_scrobbles(scrobbles)


# Function to plot multiple artists' ranks
def plot_multiple_artists(artists, bins, rank_dict):
    valid_artists = []
    for artist in artists:
        if artist in rank_dict:
            plt.plot(bins, rank_dict[artist], label=artist)
            valid_artists.append(artist)
        else:
            print(f"Artist '{artist}' not found in the data.")

    if valid_artists:
        # Find the worst ranking per bin (highest rank)
        worst_ranks_per_bin = [max(rank_dict[artist][i] for artist in rank_dict) for i in range(len(bins))]

        # Find the worst ranking across all bins
        worst_ranking_overall = max(worst_ranks_per_bin)

        worst_ranks_per_bin[-1] = worst_ranking_overall

        # Plot the filled area between the top and bottom borders
        plt.fill_between(bins, worst_ranks_per_bin, worst_ranking_overall, color='black', alpha=1)

        # Set plot properties
        plt.gca().invert_yaxis()  # Ensure the ranking goes upwards (1 at the top)
        plt.yscale('log')  # You can keep the y-axis logarithmic if you want
        plt.grid(True, which='major')
        plt.title("Artist Ranks Over Time with Worst Rank Shape")
        plt.xlabel("Time")
        plt.ylabel("Rank (Lower is Better)")
        plt.legend()
        plt.show()
    else:
        print("No valid artists to plot.")


def parse_csv_with_commas(input_string):
    # Use csv.reader to correctly handle commas within quotes
    csv_reader = csv.reader([input_string], quotechar='"', delimiter=',', skipinitialspace=True)
    return next(csv_reader)  # Return the first row as a list

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
    # current_artist_list.extend([lastfm_reader.clean_text(artist) for artist in artist_input.split(',')])
    current_artist_list.extend(parse_csv_with_commas(artist_input))

    # Plot the selected artists
    plot_multiple_artists(current_artist_list, bins, rank_dict)
