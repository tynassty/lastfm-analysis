class Scrobble:

    def __init__(self, uts: int, utc_time: str, artist: str, artist_mbid: str,
                 album: str, album_mbid: str, track: str, track_mbid: str):
        self.uts = uts
        self.utc_time = utc_time
        self.artist = artist
        self.artist_mbid = artist_mbid
        self.album = album + " (" + artist + ")"
        self.album_mbid = album_mbid
        self.track = track + " (" + artist + ")"
        self.track_mbid = track_mbid

    def __lt__(self, other):
        return self.uts < other.uts

    def __le__(self, other):
        return self.uts <= other.uts

    def __eq__(self, other):
        return self.uts == other.uts

    def __ne__(self, other):
        return self.uts != other.uts

    def __gt__(self, other):
        return self.uts > other.uts

    def __ge__(self, other):
        return self.uts >= other.uts

