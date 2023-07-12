from collections import Counter
import graph_functions
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx

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

# scrobbles = read_scrobbles('scrobbles-tynassty-1688968485.csv')
# counts = Counter()
# artist_list = []
#
# for scrobble in scrobbles:
#     counts[scrobble.artist] += 1
#     artist_list.append(scrobble.artist)
#
# top_n_artists_cts = counts.most_common(5)
# unique_artists = [artist_ct[0] for artist_ct in top_n_artists_cts]
# # unique_artists = set(counts)
#
# artist_dictionary = {}
#
# for artist in unique_artists:
#     mention_count = []
#     current_count = 0
#     for scrobble in scrobbles:
#         if artist == scrobble.artist:
#             count = 1
#         else:
#             count = 0
#         current_count += count
#         mention_count.append(current_count)
#     artist_dictionary[artist] = mention_count
#
# x_axis = []
# for scrobble in scrobbles:
#     x_axis.append(scrobble.uts)
#
# x = x_axis
# plt.figure(figsize=(10, 6))
# for artist in artist_dictionary:
#     plt.plot(x, artist_dictionary[artist], label=artist)
# plt.title('Scrobbles of top artists over time')
# plt.legend()
# # plt.show()
#
# # print(artist_list)
# artist_tuples = {}
# prior = 'START'
#
# for artist in artist_list:
#     tup = (prior, artist)
#     if tup in artist_tuples:
#         artist_tuples[tup] += 1
#     else:
#         artist_tuples[tup] = 1
#     prior = artist
#
# G = nx.DiGraph()
# edge_thick = []
# vsum = 0
#
# unique = []
#
# for key, value in artist_tuples.items():
#     if key[0] in unique_artists and key[1] in unique_artists and key[0] != key[1]:
#         name1, name2 = key
#         unique.append(name1)
#         G.add_edge(name1, name2, weight=1)
#         edge_thick.append(value)
#         vsum += value
#
# edge_thick2 = [(value/vsum)*50 for value in edge_thick]
#
# pos = nx.spring_layout(G, k=2)
# node_colors = range(len(G))
# M = G.number_of_edges()
#
# plt.figure(figsize=(10, 6), facecolor=None)
# nodes = nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors, cmap=plt.cm.Reds)
#
# edges = nx.draw_networkx_edges(G, pos, arrowstyle='->',
#                                arrowsize=50,
#                                edge_color='black',
#                                width=edge_thick2)
#
# nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
#
# ax = plt.gca()
# ax.set_axis_off()
# plt.title('graph test')
#
# plt.show()

graph_functions.line_graph('scrobbles-tynassty-1688968485.csv')
