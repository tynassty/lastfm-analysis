from datetime import datetime as dt


def int_to_weekday(n):
    weekdays = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    return weekdays.get(n)


def int_to_month(n):
    months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    return months.get(n)


class Scrobble:

    def __init__(self, uts: int, utc_time: str, artist: str, artist_mbid: str,
                 album: str, album_mbid: str, track: str, track_mbid: str):
        self.uts = uts
        self.utc_time = utc_time
        self.datetime = dt.fromtimestamp(uts)
        self.year = self.datetime.year
        self.month = int_to_month(self.datetime.month)
        self.day_of_week = int_to_weekday(self.datetime.weekday())
        self.artist = artist
        self.artist_mbid = artist_mbid
        self.album_solo = album
        self.album = album + " (" + artist + ")"
        self.album_mbid = album_mbid
        self.track_solo = track
        self.track = track + " (" + artist + ")"
        self.track_mbid = track_mbid

    def __str__(self):
        return f"Datetime: {self.datetime}, Artist: {self.artist}, Track: {self.track_solo}, Album: {self.album_solo}"

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

