import csv
from Scrobble import Scrobble
from lastfm_reader import read_scrobbles
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx


def ngrams(values, n=2):
    return [tuple(values[i:i+n]) for i in range(len(values) - n + 1)]


def compute_transitions(artists):
    transitions = Counter()
    prior = 'START'

    for artist in artists:
        transitions[(prior, artist)] += 1
        prior = artist

    return transitions


def print_top_transitions(transition_counter, top_n=10):
    for (a, b), count in transition_counter.most_common(top_n):
        print(f"{a} → {b}: {count}")


def get_following_artist_counts(artists, target_artist):
    following = []
    for i in range(len(artists) - 1):
        if artists[i] == target_artist:
            following.append(artists[i + 1])
    return Counter(following)


def draw_transition_graph(counter, min_connections=20):
    G = nx.DiGraph()
    for (a, b), count in counter.most_common(len(counter)):
        if count >= min_connections and a != b:
            G.add_edge(a, b, weight=count)

    pos = nx.spring_layout(G, k=2, seed=1)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.planar_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=8, arrowsize=10)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title("Top Artist Transitions")
    plt.show()


def export_transitions_to_csv(counter, min_connections=20, filename="transitions.csv", ignore_self_links=True,
                              directed=True):
    written = set()

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        # Write header row
        writer.writerow(["Source", "Target", "Weight"])

        # Write each edge if it meets the min_connections threshold
        for (a, b), count in counter.most_common():
            if not ignore_self_links and count < min_connections:
                continue
            if ignore_self_links and a == b:
                continue

            if not directed:
                key = frozenset([a, b])
                if key in written:
                    continue  # already wrote this unordered pair
                reverse_count = counter.get((b, a), 0)
                total = count + reverse_count if a != b else count
                if total < min_connections:
                    continue
                writer.writerow(sorted([a, b]) + [total])
                written.add(key)
            else:
                if count >= min_connections:
                    writer.writerow([a, b, count])

    print(f"\nTransitions saved to {filename}")


def main():
    n = 10
    scrobbles = read_scrobbles("scrobbles-tynassty.csv")
    scrobbles = sorted(scrobbles)
    artists = [scrobble.artist for scrobble in scrobbles]
    # artists = [scrobble.track for scrobble in scrobbles]
    # artists = [scrobble.hour for scrobble in scrobbles]

    # artists = ngrams(artists, 2)

    artist_counter = Counter(artists)
    top_artists = artist_counter.most_common(n)

    print("Top Artists:")
    for artist, count in top_artists:
        print(f"{artist}: {count}")

    print("\nTop Transitions:")
    transition_counter = compute_transitions(artists)
    print_top_transitions(transition_counter, top_n=n)


    # target = "coeur d'alene (work wife)"
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

    export_transitions_to_csv(transition_counter, min_connections=15, directed=False, ignore_self_links=True)


if __name__ == "__main__":
    main()
