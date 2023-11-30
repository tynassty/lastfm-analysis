from datetime import timedelta, datetime
from typing import List

import graph_functions
from Scrobble import Scrobble
import lastfm_reader

scrobbles = lastfm_reader.read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

counts, occurrence_list = graph_functions.count_occurrences(scrobbles, attribute="artist")

# print(counts.most_common(10))

artists_to_analyze = []

for count in counts.most_common(1000):
    artists_to_analyze.append(count[0])

for artist in artists_to_analyze:
    datetimes = []
    artist_scrobbles = [scr for scr in scrobbles if scr.artist == artist]
    for scrobble in artist_scrobbles:
        datetimes.append(scrobble.datetime)

    # Calculate the sum of differences from a reference datetime
    reference_datetime = datetime(2000, 1, 1)  # Choose a reference datetime
    sum_of_differences = sum((dt - reference_datetime for dt in datetimes), timedelta())

    # Calculate the average
    average_datetime = reference_datetime + (sum_of_differences / len(datetimes))

    print(artist, average_datetime)



