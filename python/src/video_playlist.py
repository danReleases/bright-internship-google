"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name):
        self._videos = []
        self._playlist_name = name

    def add_video(self, video):
        if video in self._videos:
            return 0
        else:
            self._videos.append(video)
            return 1

    def remove_video(self, video):
        if video not in self._videos:
            return 0
        else:
            self._videos.remove(video)
            return 1

    def clear_all(self):
        self._videos.clear()

    @property
    def name(self) -> str:
        """Returns the title of a playlist."""
        return self._playlist_name

    @property
    def videos(self):
        return self._videos