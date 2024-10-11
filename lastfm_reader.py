from unidecode import unidecode
from Scrobble import Scrobble


COMMA_ARTISTS = ["tyler, the creator", "now, now", "love, ecstasy and terror", "thank you, i'm sorry", "merci, mercy",
                 "slaughter beach, dog", "sincerely, me", "chunk! no, captain chunk!", "10,000 maniacs",
                 "earth, wind & fire", "crosby, stills, nash & young", "fuck yeah, dinosaurs!",
                 "black country, new road", "whatever, dad", "the army, the navy", "hey, nothing",
                 "two blinks, i love you", "lucie,too"]


def clean_text(text):
    return unidecode(text.strip().lower())


def read_scrobbles(scrobbles_file):
    scrobbles = []
    f = open(scrobbles_file, encoding="utf8")
    next(f)
    for line in f:
        line = line.split('",')
        artist = clean_text(line[2][1:])
        album = clean_text(line[4][1:])
        track = clean_text(line[6][1:])
        if artist not in COMMA_ARTISTS:
            artist = artist.split(",")[0]
        scrobbles.append(Scrobble(int(line[0][1:]), line[1][1:], artist, line[3][1:], album, line[5][1:], track,
                                  line[7][1:-1]))
    return scrobbles


if __name__ == '__main__':
    scrobbles = read_scrobbles("scrobbles-tynassty.csv")
    print(len(scrobbles))
