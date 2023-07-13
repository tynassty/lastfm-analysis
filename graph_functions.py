from collections import Counter
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx


def count_occurrences(scrobbles, attribute='artist'):
    counts = Counter()
    occurrence_list = []

    for scrobble in scrobbles:
        counts[getattr(scrobble, attribute)] += 1
        occurrence_list.append(scrobble.artist)

    return counts, occurrence_list


def line_graph(file, count=10, attribute='artist'):
    scrobbles = read_scrobbles(file)
    counts, occurrence_list = count_occurrences(scrobbles, attribute=attribute)

    top_n_counts = counts.most_common(count)
    unique_occurrences = [artist_ct[0] for artist_ct in top_n_counts]

    occurrence_dictionary = {}

    for item in unique_occurrences:
        mention_count = []
        current_count = 0
        for scrobble in scrobbles:
            count = 1 if item == getattr(scrobble, attribute) else 0
            current_count += count
            mention_count.append(current_count)
        occurrence_dictionary[item] = mention_count

    x_axis = []
    for scrobble in scrobbles:
        x_axis.append(scrobble.uts)

    x = x_axis
    plt.figure(figsize=(10, 6))
    for item in occurrence_dictionary:
        plt.plot(x, occurrence_dictionary[item], label=item)
    plt.title('Scrobbles of top artists over time')
    plt.legend()
    plt.show()


def interaction_graph(file):
    scrobbles = read_scrobbles(file)

    counts, artist_list = count_occurrences(scrobbles)

    top_n_artists_cts = counts.most_common(10)
    top_artists = [artist_ct[0] for artist_ct in top_n_artists_cts]

    artist_tuples = {}
    prior = 'START'

    for artist in artist_list:
        tup = (prior, artist)
        if tup in artist_tuples:
            artist_tuples[tup] += 1
        else:
            artist_tuples[tup] = 1
        prior = artist

    G = nx.DiGraph()
    edge_thick = []
    vsum = 0

    for key, value in artist_tuples.items():
        if key[0] in top_artists and key[1] in top_artists and key[0] != key[1]:
            name1, name2 = key
            G.add_edge(name1, name2, weight=value)
            edge_thick.append(value)
            vsum += value

    edge_thick2 = [(value / vsum) * 50 for value in edge_thick]

    pos = nx.spring_layout(G, k=2)
    node_colors = range(len(G))
    M = G.number_of_edges()

    plt.figure(figsize=(10, 6), facecolor=None)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors, cmap=plt.cm.Reds)

    edges = nx.draw_networkx_edges(G, pos, arrowstyle='->',
                                   arrowsize=20,
                                   edge_color='black',
                                   width=edge_thick2,
                                   min_target_margin=15)

    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')

    ax = plt.gca()
    ax.set_axis_off()
    plt.title('graph test')

    plt.show()
