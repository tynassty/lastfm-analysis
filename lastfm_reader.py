from Scrobble import Scrobble
from unidecode import unidecode
import csv


def clean_text(text):
    return unidecode(text.strip().lower())


COMMA_ARTISTS = [clean_text(a) for a in ["tyler, the creator", "now, now", "love, ecstasy and terror",
                                         "thank you, i'm sorry", "merci, mercy", "slaughter beach, dog",
                                         "sincerely, me", "chunk! no, captain chunk!", "10,000 maniacs",
                                         "earth, wind & fire", "crosby, stills, nash & young", "fuck yeah, dinosaurs!",
                                         "black country, new road", "whatever, dad", "the army, the navy",
                                         "hey, nothing", "two blinks, i love you", "lucie,too"]]


def read_scrobbles(scrobbles_file):
    scrobbles = []
    with open(scrobbles_file, encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            artist = clean_text(row[2])
            album = clean_text(row[4])
            track = clean_text(row[6])
            if artist not in COMMA_ARTISTS:
                artist = artist.split(",")[0]
            scrobbles.append(Scrobble(int(row[0]), row[1], artist, row[3], album, row[5], track, row[7]))
    return scrobbles


if __name__ == '__main__':
    scrobbles = read_scrobbles("scrobbles-tynassty.csv")
    print(len(scrobbles))
