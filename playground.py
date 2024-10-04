import datetime as dt
from matplotlib import pyplot as plt
import time_graph
from lastfm_reader import read_scrobbles

scrobbles = read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

filtered_scrobbles = [scr for scr in scrobbles]

top_avg90 = ['snail mail', 'tove lo', 'vona vella', 'blondshell', 'ada lea', 'newdad', 'jackie hayes', 'the beths',
             'beach bunny', 'adult mom', 'kynsy', 'slow pulp', 'bully', 'mothica', 'the cranberries', 'destroy boys',
             'speedy ortiz', 'chvrches', 'suzi wu', 'charly bliss', 'frankie cosmos', 'soccer mommy', 'ciarra fragale',
             'broods', 'arlo parks', 'chastity belt', 'mannequin pussy', 'jacklen ro']

# addl = top_avg90

addl = ["jacklen ro"]

try:
    time_graph.graph_from_scrobbles(filtered_scrobbles, k=9, plot_func=plt.step,
                                    mvg_avg_period=dt.timedelta(days=365), relative=None, addtl_artists=addl)
except time_graph.ScrobblesError as e:
    print(f"Error: {e}")
