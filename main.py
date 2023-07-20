from collections import Counter
from datetime import datetime
import graph_functions
import time_graph
from Scrobble import filter_by_key
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx
import time

scrobbles = read_scrobbles('scrobbles-tynassty.csv')
# time_graph.graph(scrobbles[0].datetime)

# graph_functions.line_graph(scrobbles, attribute='month', k=12)

# graph_functions.interaction_graph('scrobbles-tynassty.csv', k=25)
# names = ["Sleater-Kinney, Courtney Barnett", "Sleater-Kinney", "Courtney Barnett"]
# graph_functions.line_graph_by_names(scrobbles, names, attribute='artist')

# scrobbles = [scr for scr in scrobbles if scr.datetime.hour == 1]
# counts, occurrence_list = graph_functions.count_occurrences(scrobbles)
# for count in counts.most_common(10):
#     print(count[0])

# for i in range(2017, 2024):
#     for j in range(12):
#         scrs = [scr for scr in scrobbles if scr.datetime.year == i and scr.datetime.month == j]
#         counts, _ = graph_functions.count_occurrences(scrs)
#         print(i, j)
#         for ct in counts.most_common(1):
#             print(ct[0])
#         print()

# for scrobble in scrobbles:
#     print(scrobble.year)
#
# counts, occurrence_list = graph_functions.count_occurrences(scrobbles, attribute='year')
# print(counts)
