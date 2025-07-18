from Scrobble import Scrobble
from lastfm_reader import read_scrobbles
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


def compute_transitions(artists):
    transitions = {}
    prior = 'START'

    for artist in artists:
        tup = (prior, artist)
        transitions[tup] = transitions.get(tup, 0) + 1
        prior = artist

    return Counter(transitions)


def print_top_transitions(transition_counter, top_n=10):
    for (a, b), count in transition_counter.most_common(top_n):
        print(f"{a} → {b}: {count}")


def get_following_artist_counts(artists, target_artist):
    following = []
    for i in range(len(artists) - 1):
        if artists[i] == target_artist:
            following.append(artists[i + 1])
    return Counter(following)


def draw_transition_graph(counter, top_n=20):
    G = nx.DiGraph()
    for (a, b), count in counter.most_common(top_n):
        G.add_edge(a, b, weight=count)

    pos = nx.spring_layout(G, k=0.8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Top Artist Transitions")
    plt.show()


def main():
    n = 50
    scrobbles = read_scrobbles("scrobbles-tynassty.csv")
    scrobbles = sorted(scrobbles)
    artists = [scrobble.artist for scrobble in scrobbles]

    artist_counter = Counter(artists)
    top_artists = artist_counter.most_common(n)

    print("Top Artists:")
    for artist, count in top_artists:
        print(f"{artist}: {count}")

    print("\nTop Transitions:")
    transition_counter = compute_transitions(artists)
    print_top_transitions(transition_counter)

    # target = "soccer mommy"
    # counts = get_following_artist_counts(artists, target)
    #
    # print(f"\nArtists most frequently played after '{target}':")
    # total_counts = 0
    # for artist, count in counts.most_common(n):
    #     total_counts += count
    #     print(f"{artist}: {count}")
    # print(f"others: {artist_counter[target] - total_counts}")


    print("\nPercentage of plays followed by same artist:")
    for artist in top_artists:
        target = artist[0]
        print(f"{target}: {transition_counter[(target, target)]/artist_counter[target]*100:.2f}%")
        # print(target, transition_counter[(target, target)]/artist_counter[target])


if __name__ == "__main__":
    main()
