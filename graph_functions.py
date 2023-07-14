from collections import Counter
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx
from typing import List


def count_occurrences(scrobbles: List[Scrobble], attribute='artist'):
    """
    Counts occurrences of a given attribute in a list of scrobbles.
    :param scrobbles: A list of scrobbles
    :param attribute: The attribute to count. Default is 'artist', other possibilities include 'album' and 'track'.
    :return: counts, a Counter object containing the counts of each attribute value, and occurrence_list, a list of the
    attributes in the order they appear
    """
    counts = Counter()
    occurrence_list = []

    for scrobble in scrobbles:
        counts[getattr(scrobble, attribute)] += 1
        occurrence_list.append(scrobble.artist)

    return counts, occurrence_list


def line_graph(file, k=10, attribute='artist'):
    """
    Generate a line graph that shows the scrobbles of the top k of an attribute over time.
    :param file: The address of the file containing scrobble data.
    :param k: The number of artists to graph.
    :param attribute: The attribute to graph. Default is 'artist', other possibilities include 'album' and 'track'.
    :return: None
    """
    scrobbles = read_scrobbles(file)
    scrobbles = sorted(scrobbles)
    counts, occurrence_list = count_occurrences(scrobbles, attribute=attribute)

    top_n_counts = counts.most_common(k)
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

    x_axis = [scrobble.datetime for scrobble in scrobbles]

    plt.figure(figsize=(10, 6))
    for i, item in enumerate(occurrence_dictionary):
        plt.plot(x_axis, occurrence_dictionary[item], label=item)
        i += 1
    plt.title('Scrobbles of top ' + str(k) + ' ' + attribute + 's over time')
    plt.legend()
    plt.show()


def line_graph_by_names(file, names: List[str], attribute='artist'):
    """
        Generate a line graph that shows the scrobbles of the top k of an attribute over time.
        :param file: The address of the file containing scrobble data.
        :param names: A list of names to graph.
        :param attribute: The attribute to graph. Default is 'artist', other possibilities include 'album' and 'track'.
        :return: None
        """
    scrobbles = read_scrobbles(file)
    scrobbles = sorted(scrobbles)

    occurrence_dictionary = {}

    for item in names:
        mention_count = []
        current_count = 0
        for scrobble in scrobbles:
            count = 1 if item == getattr(scrobble, attribute) else 0
            current_count += count
            mention_count.append(current_count)
        occurrence_dictionary[item] = mention_count

    x_axis = [scrobble.datetime for scrobble in scrobbles]

    plt.figure(figsize=(10, 6))
    for i, item in enumerate(occurrence_dictionary):
        plt.plot(x_axis, occurrence_dictionary[item], label=item)
        i += 1
    plt.title('Scrobbles of selected ' + attribute + 's over time')
    plt.legend()
    plt.show()


def interaction_graph(file, k=10):
    scrobbles = read_scrobbles(file)

    counts, occurrence_list = count_occurrences(scrobbles)

    top_n_cts = counts.most_common(k)
    unique_occurrences = [artist_ct[0] for artist_ct in top_n_cts]

    occurrence_tuples = {}
    prior = 'START'

    for item in occurrence_list:
        tup = (prior, item)
        if tup in occurrence_tuples:
            occurrence_tuples[tup] += 1
        else:
            occurrence_tuples[tup] = 1
        prior = item

    G = nx.DiGraph()
    edge_thick = []
    vsum = 0

    for key, value in occurrence_tuples.items():
        if key[0] in unique_occurrences and key[1] in unique_occurrences and key[0] != key[1]:
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
