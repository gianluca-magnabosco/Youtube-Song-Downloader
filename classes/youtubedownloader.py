import os
import random
import string
import subprocess
from threading import Thread
import time
from pytube import Search
from datetime import timedelta
from tkinter import messagebox
import re


class YoutubeDownloader():

    songStreams = []
    convert = None
    downloadSongsThreadQueue = []


    def sanitize(self, string):
        return re.sub("[\\\/\:\*\?\"\<\>\|]", "", string)


    def getVideoAttributes(self, query):
        try:
            search = Search(query)
            video = search.results[0]
        except:
            return None

        if self.addVideoStream(video):
            return [self.sanitize(video.title), str(timedelta(seconds = video.length))]
        else:
            return None


    def addVideoStream(self, video):
        try:
            songName = video.title
            songName = self.sanitize(songName)
            songStream = video.streams.get_audio_only()
            songName += f".{songStream.mime_type[6:]}"
            self.songStreams.append({"file_name": songName, "stream": songStream})
        except:
            return False
        else:
            return True
        
    
    def downloadSongs(self, convert):
        if convert is True:
            self.convert = True
        else:
            self.convert = False

        Thread(target = self.downloadSongsThread).start()


    def downloadSongsThread(self):
        threadHash = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.downloadSongsThreadQueue.append(threadHash)
        
        while self.downloadSongsThreadQueue[0] != threadHash:
            time.sleep(1)
            
        i = 0
        for song in self.songStreams:
            song["stream"].download(output_path = "sounds/", filename = song["file_name"])
            
            if self.convert is True:
                self.convertSongToMP3(song)
            
            i += 1
            
        self.songStreams = []
        self.downloadSongsThreadQueue.pop(0)

        if i > 0 and len(self.downloadSongsThreadQueue) == 0:
            messagebox.showinfo("Success!", "All the videos were downloaded successfully!")
        


    def convertSongToMP3(self, song):
        mp3file = song["file_name"][:-4] + ".mp3"
        subprocess.run(["ffmpeg", "-y", "-i", f"sounds/{song['file_name']}", f"sounds/{mp3file}"])
        os.remove(f"sounds/{song['file_name']}")
