"""A video player class."""

from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video = None
        self.playing = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        video_data = self._video_library.get_all_videos()
        video_data_sorted = sorted(video_data, key=lambda k: k.title)
        print("Here's a list of all available videos:")
        for video in video_data_sorted:
            temp_str = video.info_str
            if video.flag != "":
                temp_str = temp_str + " - FLAGGED (reason: {})".format(video.flag)
            print(temp_str)

    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot play video: Video does not exist")
        elif video.flag != "":
            print("Cannot play video: Video is currently flagged (reason: {})".format(video.flag))
        else:
            if self.current_video is not None:
                print("Stopping video: " + self.current_video.title)

            self.current_video = video
            self.playing = True
            print("Playing video: " + self.current_video.title)

    def stop_video(self):
        """Stops the current video."""
        if self.current_video is not None:
            print("Stopping video: " + self.current_video.title)
            self.current_video = None
            self.playing = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        video_data = self._video_library.get_all_videos()
        video_data = [v for v in video_data if v.flag == ""]
        if len(video_data) == 0:
            print("No videos available")
        else:
            if self.current_video is not None:
                self.stop_video()
            self.play_video(random.choice(video_data).video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.current_video is None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self.playing is False:
                print("Video already paused: " + self.current_video.title)
            else:
                self.playing = False
                print("Pausing video: " + self.current_video.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.current_video is None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.playing is True:
                print("Cannot continue video: Video is not paused")
            else:
                self.playing = True
                print("Continuing video: " + self.current_video.title)

    def show_playing(self):
        """Displays video currently playing."""
        if self.current_video is None:
            print("No video is currently playing")
        else:
            temp_str = "Currently playing: " + self.current_video.info_str
            if self.playing is False:
                temp_str = temp_str + " - PAUSED"
            print(temp_str)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """

        success = self._video_library.add_playlist(playlist_name)
        if success == 0:
            print("Cannot create playlist: A playlist with the same name already exists")
        elif success == 1:
            print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self._video_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist is None:
            print("Cannot add video to {}: Playlist does not exist".format(playlist_name))

            # Extra feature - create playlist (commented out as it will fail the pre-made test modules).

            '''print("Create playlist with video? Press 1.")
            do_create = input()
            try:
                do_create = int(do_create)
                if do_create == 1:
                    self.create_playlist(playlist_name)
                    self.add_to_playlist(playlist_name, video_id)
            except ValueError:
                pass'''

            # End extra

        elif video is None:
            print("Cannot add video to {}: Video does not exist".format(playlist_name))
        elif video.flag != "":
            print("Cannot add video to my_playlist: Video is currently flagged (reason: {})".format(video.flag))
        else:
            success = playlist.add_video(video)
            if success == 0:
                print("Cannot add video to {}: Video already added".format(playlist_name))
            elif success == 1:
                print("Added video to {}: ".format(playlist_name) + video.title)

    def show_all_playlists(self):
        """Display all playlists."""
        playlist_data = self._video_library.get_all_playlists()
        if len(playlist_data) == 0:
            print("No playlists exist yet")
        else:
            playlist_data_sorted = sorted(playlist_data, key=lambda k: k.name)
            print("Showing all playlists:")
            for playlist in playlist_data_sorted:
                print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None:
            print("Cannot show playlist {}: Playlist does not exist".format(playlist_name))
        else:
            playlist_videos = playlist.videos
            print("Showing playlist: {}".format(playlist_name))
            if not playlist_videos:
                print("No videos here yet")
            else:
                # Extra
                # print("Found {} video(s).".format(len(playlist_videos)))

                for video in playlist_videos:
                    temp_str = video.info_str
                    if video.flag != "":
                        temp_str = temp_str + " - FLAGGED (reason: {})".format(video.flag)
                    print(temp_str)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self._video_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist is None:
            print("Cannot remove video from {}: Playlist does not exist".format(playlist_name))
        elif video is None:
            print("Cannot remove video from {}: Video does not exist".format(playlist_name))
        else:
            success = playlist.remove_video(video)
            if success == 0:
                print("Cannot remove video from {}: Video is not in playlist".format(playlist_name))
            elif success == 1:
                print("Removed video from {}: {}".format(playlist_name, video.title))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        playlist = self._video_library.get_playlist(playlist_name)
        if playlist is None:
            print("Cannot clear playlist {}: Playlist does not exist".format(playlist_name))
        else:
            playlist.clear_all()
            print("Successfully removed all videos from {}".format(playlist_name))

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        success = self._video_library.remove_playlist(playlist_name)
        if success == 0:
            print("Cannot delete playlist {}: Playlist does not exist".format(playlist_name))
        elif success == 1:
            print("Deleted playlist: " + playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.
        Args:
            search_term: The query to be used in search.
        """
        video_data = self._video_library.get_all_videos()
        video_data = [v for v in video_data if v.flag == ""]
        video_data_sorted = sorted(video_data, key=lambda k: k.title)
        matched_videos = [v for v in video_data_sorted if search_term.lower() in v.title.lower()]

        if len(matched_videos) == 0:
            print("No search results for " + search_term)
        else:
            print("Here are the results for {}:".format(search_term))
            for i in range(0, len(matched_videos)):
                print("{}) {}".format(i + 1, matched_videos[i].info_str))

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            play_num = input()
            try:
                play_num = int(play_num)
                if 1 <= play_num <= len(matched_videos):
                    self.play_video(matched_videos[play_num - 1].video_id)
            except ValueError:
                pass

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.
        Args:
            video_tag: The video tag to be used in search.
        """
        if not video_tag.startswith('#'):
            print("No search results for " + video_tag)
        else:
            video_data = self._video_library.get_all_videos()
            video_data = [v for v in video_data if v.flag == ""]
            video_data_sorted = sorted(video_data, key=lambda k: k.title)
            matched_videos = [v for v in video_data_sorted if video_tag.lower() in [t.lower() for t in list(v.tags)]]

            if len(matched_videos) == 0:
                print("No search results for " + video_tag)
            else:
                print("Here are the results for {}:".format(video_tag))
                for i in range(0, len(matched_videos)):
                    print("{}) {}".format(i + 1, matched_videos[i].info_str))

                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")
                play_num = input()
                try:
                    play_num = int(play_num)
                    if 1 <= play_num <= len(matched_videos):
                        self.play_video(matched_videos[play_num - 1].video_id)
                except ValueError:
                    pass

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.
        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot flag video: Video does not exist")
        else:
            if video.flag != "":
                print("Cannot flag video: Video is already flagged")
            else:
                video.flag = "Not supplied" if flag_reason == "" else flag_reason
                if self.current_video == video:
                    self.stop_video()
                print("Successfully flagged video: {} (reason: {})".format(video.title, video.flag))

    def allow_video(self, video_id):
        """Removes a flag from a video.
        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if video.flag == "":
                print("Cannot remove flag from video: Video is not flagged")
            else:
                video.flag = ""
                print("Successfully removed flag from video: " + video.title)
