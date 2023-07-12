class Scrobble:

    def __init__(self, uts: int, utc_time, artist, artist_mbid, album, album_mbid, track, track_mbid):
        self.uts = uts
        self.utc_time = utc_time
        self.artist = artist
        self.artist_mbid = artist_mbid
        self.album = album
        self.album_mbid = album_mbid
        self.track = track
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

