from collections import Counter
from lastfm_reader import *
import networkx as nx
import matplotlib.pyplot as plt

# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()

# previous = 'NULL'
# edges = {}
#
# with open('dummy_data.txt', 'rt') as f:
#     for line in f:
#         line = line[:-1]
#         edge = (previous, line)
#         g = edges.get(edge)
#         if g is None:
#             edges.update({edge: 1})
#         else:
#             edges.update({edge: g+1})
#         previous = line
#
# # print(edges)
#
# G = nx.Graph()
# print(G)
#
# for edge in edges:
#     G.add_weighted_edges_from([(edge[0], edge[1], edges.get(edge))])
#
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show()

scrobbles = read_scrobbles('scrobbles-tynassty-1688968485.csv')
counts = Counter()
for scrobble in scrobbles:
    if scrobble.uts >= 0:
        counts[scrobble.artist] += 1
print(counts.most_common(10))
