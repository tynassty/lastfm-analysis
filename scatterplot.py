from lastfm_reader import read_scrobbles
from matplotlib import pyplot as plt


FIG_WIDTH = 10
FIG_HEIGHT = 5

scrobbles = read_scrobbles('scrobbles-tynassty.csv')
scrobbles = sorted(scrobbles)

x = []
y = []

for scr in scrobbles:
    x.append(scr.datetime)
    y.append((scr.datetime.time().hour + (scr.datetime.time().minute/60) + (scr.datetime.time().second/3600)))


plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
plt.scatter(x, y, alpha=1, s=0.1)
plt.gca().invert_yaxis()
plt.show()
