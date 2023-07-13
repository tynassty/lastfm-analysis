from collections import Counter
import graph_functions
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx

graph_functions.line_graph('scrobbles-tynassty.csv', attribute='month', k=12)
# graph_functions.interaction_graph('scrobbles-tynassty.csv', k=25)

# scrobbles = read_scrobbles('scrobbles-tynassty.csv')
#
# for scrobble in scrobbles:
#     print(scrobble)
