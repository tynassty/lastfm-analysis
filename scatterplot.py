from lastfm_reader import read_scrobbles
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

FIG_WIDTH = 10
FIG_HEIGHT = 5

# read in scrobbles
scrobbles = read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

# filter scrobbles
# scrobbles = [scr for scr in scrobbles if scr.datetime.month >= 7]

# add data for each scrobble to axes
x = [scr.datetime.date() for scr in scrobbles]
y = [datetime.combine(datetime.today(), scr.datetime.time()) for scr in scrobbles]

plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
plt.scatter(x, y, alpha=.1, s=1)
plt.gca().invert_yaxis()

# add labels and title
plt.xlabel('Date')
plt.ylabel('Time of Day')
plt.title('Last.fm Scrobbles Over Time')

# format y axis
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()
