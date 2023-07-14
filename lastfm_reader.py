from Scrobble import Scrobble


def read_scrobbles(scrobbles_file):
    scrobbles = []
    f = open(scrobbles_file, encoding="utf8")
    next(f)
    for line in f:
        line = line.split('",')
        scrobbles.append(Scrobble(int(line[0][1:]), line[1][1:], line[2][1:], line[3][1:],
                                  line[4][1:], line[5][1:], line[6][1:], line[7][1:-1]))
    return scrobbles


if __name__ == '__main__':
    read_scrobbles("scrobbles-tynassty.csv")
