import datetime as dt
from matplotlib import pyplot as plt
import time_graph
from lastfm_reader import read_scrobbles

scrobbles = read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

filtered_scrobbles = [scr for scr in scrobbles]

addl = ["telenova"]

try:
    time_graph.graph_from_scrobbles(filtered_scrobbles, k=10, plot_func=plt.step,
                                    mvg_avg_period=dt.timedelta(days=365), relative=None, addtl_artists=addl)
except time_graph.ScrobblesError as e:
    print(f"Error: {e}")
