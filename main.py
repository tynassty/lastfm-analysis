from collections import Counter
import graph_functions
from lastfm_reader import *
import matplotlib.pyplot as plt
import networkx as nx

graph_functions.line_graph('scrobbles-tynassty.csv', attribute='track')
