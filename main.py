from collections import Counter
import graph_functions
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx

# graph_functions.line_graph('scrobbles-tynassty.csv', attribute='track', k=10)
# graph_functions.interaction_graph('scrobbles-tynassty.csv', k=25)
names = ["Lucy Dacus"]
graph_functions.line_graph_by_names('scrobbles-tynassty.csv', names, attribute='artist')

# scrobbles = read_scrobbles('scrobbles-tynassty.csv')
#
# for scrobble in scrobbles:
#     print(scrobble.track)
