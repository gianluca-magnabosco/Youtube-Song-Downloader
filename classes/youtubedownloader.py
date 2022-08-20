from pytube import Search
from datetime import timedelta
from tkinter import messagebox
import re
import os
import subprocess


class YoutubeDownloader():

    songStreams = []


    def sanitize(self, string):
        return re.sub("[\\\/\:\*\?\"\<\>\|]", "", string)


    def getVideoAttributes(self, query):
        try:
            search = Search(query)
            video = search.results[0]
        except:
            return None
        else:
            self.addVideoStream(video)
            return [self.sanitize(video.title), str(timedelta(seconds = video.length))]


    def addVideoStream(self, video):
        try:
            songName = video.title
            songName = self.sanitize(songName)
            songStream = video.streams.get_audio_only()
            songName += f".{songStream.mime_type[6:]}"
            self.songStreams.append({"file_name": songName, "stream": songStream})
        except:
            messagebox.showerror("Error", "Video not found or is unavailable")
        
    
    def downloadSongs(self):
        for song in self.songStreams:
            song["stream"].download(output_path = "sounds/", filename = song["file_name"])
            mp3file = song["file_name"][:-4] + ".mp3"
            subprocess.run(["ffmpeg", "-i", f"sounds/{song['file_name']}", f"sounds/{mp3file}"])
            os.remove(f"sounds/{song['file_name']}")
            
        self.songStreams = []
