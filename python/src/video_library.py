"""A video library class."""

from .video import Video
from .video_playlist import Playlist
from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        self._playlists = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.
        Args:
            video_id: The video url.
        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)

    def get_all_playlists(self):
        """Returns all available playlists from the video library."""
        return list(self._playlists.values())

    def get_playlist(self, playlist_name):
        """Returns the playlist object
        Args:
            playlist_name: The playlist name.
        Returns:
            The video_playlist object for the requested playlist_name. None if the playlist
            does not exist.
        """
        return self._playlists.get(playlist_name.upper(), None)

    def add_playlist(self, playlist_name):
        if playlist_name.upper() in self._playlists:
            return 0
        else:
            self._playlists[playlist_name.upper()] = Playlist(playlist_name)
            return 1

    def remove_playlist(self, playlist_name):
        if playlist_name.upper() not in self._playlists:
            return 0
        else:
            del self._playlists[playlist_name.upper()]
            return 1