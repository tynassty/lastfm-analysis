import matplotlib.pyplot as plt
import time_graph
from time_graph import create_bins
from lastfm_reader import read_scrobbles

# read in scrobbles
scrobbles = read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

start = scrobbles[0].datetime
end = scrobbles[-1].datetime

bins = create_bins(start, end)
bin_index = 0

artists = set()

for scrobble in scrobbles:
    artists.add(scrobble.artist)

# create dictionary with each artist as keys and empty lists to represent scrobbles
scr_dict = {artist: [0] * len(bins) for artist in artists}
rank_dict = {artist: [0] * len(bins) for artist in artists}
cumul_dict = {}
avg_dict = {}

for scrobble in scrobbles:
    while scrobble.datetime > bins[bin_index]:
        bin_index += 1
    scr_dict[scrobble.artist][bin_index] += 1

for artist in scr_dict.keys():
    cumul_dict[artist] = time_graph.accumulate_array(scr_dict[artist])
    # avg_dict[artist] = time_graph.moving_sum(scr_dict[artist], 90)

for i in range(len(bins)):
    scrs = [(a, cumul_dict[a][i]) for a in artists]
    sorted_scrs = sorted(scrs, key=lambda x: -x[1])
    # print(sorted_scrs)
    for j in range(len(artists)):
        rank_dict[sorted_scrs[j][0]][i] = j+1


artists_to_graph = set()

# for artist in rank_dict.keys():
#     if any(n <= 5 for n in rank_dict[artist][365:]):
#         artists_to_graph.add(artist)

artists_to_graph.add("charly bliss")

print(artists_to_graph)

for artist in artists_to_graph:
    plt.step(bins, rank_dict[artist], label=artist)
plt.gca().invert_yaxis()
# plt.title("hiya")
plt.grid(True)
plt.legend()
plt.show()
