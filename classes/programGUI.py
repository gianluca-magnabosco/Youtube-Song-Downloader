import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import CENTER, W, NO, END
import re
import sys
import os
from classes.youtubedownloader import YoutubeDownloader
from threading import Thread
import random
import string
import time


class ProgramGUI(YoutubeDownloader):

    songID = 0
    threadQueue = []

    def centerWindow(self, width, height, window):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    

    def onCloseRoot(self):
        close = messagebox.askokcancel("Confirmation", "Are you sure you want to close the program?")
        if close:
            self.root.destroy()
            sys.exit()
    

    def initGUI(self):
        self.root = tk.Tk()
        self.centerWindow(860, 640, self.root)
        self.root.title("Youtube Song Downloader")
        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        iconFile = "img/icon.ico"
        self.root.iconbitmap(default = iconFile)
        self.root.resizable(False, False)

        self.initLabels()
        self.initEntry()
        self.initButtons()
        self.initTreeView()

        self.root.mainloop()
    

    def returnHandler(self, e):
        self.addToTreeView()


    def initLabels(self):
        self.insertLabel = tk.Label(text = "Link: ", wraplength = 200, font = ("", 12, "bold"))
        self.insertLabel.pack()
        self.insertLabel.place(relx = 0.16, rely = 0.03)


    def initEntry(self):
        self.insertVariable = tk.StringVar()
        self.insertEntry = ttk.Entry(self.root, textvariable = self.insertVariable, width = 80)
        self.insertEntry.place(relx = 0.5, rely = 0.048, anchor = CENTER)
        self.insertEntry.bind("<Return>", self.returnHandler)


    def initButtons(self):
        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("W.TButton", background = "white", foreground = "black", font = ("Open Sans", 11))
        
        self.insertTopButton = ttk.Button(self.root, style = "W.TButton", text = "Add", command = self.addToTreeView, width = 5)
        self.insertTopButton.pack()
        self.insertTopButton.place(relx = 0.796, rely = 0.029)

        self.insertBottomButton = ttk.Button(self.root, style = "W.TButton", text = "Add", command = self.addToTreeView)
        self.insertBottomButton.pack()
        self.insertBottomButton.place(relx = 0.28, rely = 0.76)

        self.removeButton = ttk.Button(self.root, style = "W.TButton", text = "Remove", command = self.removeFromTreeView)
        self.removeButton.pack()
        self.removeButton.place(relx = 0.6, rely = 0.76)

        self.downloadButton = ttk.Button(self.root, style = "W.TButton", text  = "Download", command = self.download)
        self.downloadButton.pack()
        self.downloadButton.place(relx = 0.44, rely = 0.85)

        self.openFolderButton = ttk.Button(self.root, style = "W.TButton", text = "", command = self.openFolder)
        image = tk.PhotoImage(file="img/folder.png")
        self.openFolderButton.config(image = image)
        self.openFolderButton.image = image
        self.openFolderButton.pack()
        self.openFolderButton.place(relx = 0.85, rely = 0.85)


    def initTreeView(self):
        self.treeView = ttk.Treeview(self.root, height = 20)
        
        self.treeView["columns"] = ("ID", "Name", "Duration")
        self.treeView.column("#0", width = 0, stretch = NO)
        self.treeView.column("ID", anchor = CENTER, width = 40)
        self.treeView.column("Name", anchor = W, width = 500)
        self.treeView.column("Duration", anchor = CENTER, width = 120)
        
        self.treeView.heading("ID", text = "ID", anchor = CENTER)
        self.treeView.heading("Name", text = "Name", anchor = CENTER)
        self.treeView.heading("Duration", text = "Duration", anchor = CENTER)
        

        self.treeView.bind("<Motion>", "break")
        self.treeView.pack(pady = 50)

        self.scrollBar = ttk.Scrollbar(self.root, orient = tk.VERTICAL, command = self.treeView.yview)
        self.treeView.configure(yscrollcommand = self.scrollBar.set)


    def on_after(self):
        self.addLabel.destroy()


    def showAddingLabel(self):
        try:
            self.addLabel.destroy()
        except:
            pass
        self.addLabel = tk.Label(text = "Adding...", wraplength = 200, font = ("", 14, "bold"), fg = "green")
        self.addLabel.pack()
        self.addLabel.place(relx = 0.45, rely = 0.76)
        self.addLabel.after(5000, self.on_after)


    def showAddedLabel(self):
        try:
            self.addLabel.destroy()
        except:
            pass
        self.addLabel = tk.Label(text = "Added!", wraplength = 200, font = ("", 14, "bold"), fg = "green")
        self.addLabel.pack()
        self.addLabel.place(relx = 0.45, rely = 0.76)
        self.addLabel.after(5000, self.on_after)


    def addToTreeView(self):
        Thread(target = self.insertThread).start()


    def insertThread(self):
        currentEntry = self.insertEntry.get()
        self.insertEntry.delete(0, END)
        self.insertEntry.focus()

        if re.match("^\s+$", currentEntry) or currentEntry == "":
            messagebox.showwarning(title = "Error", message = "Invalid value")
            return


        threadHash = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.threadQueue.append(threadHash)

        while self.threadQueue[0] != threadHash:
            time.sleep(1)

        self.showAddingLabel()

        videoAttributes = self.getVideoAttributes(currentEntry)
        if videoAttributes is None:
            messagebox.showerror("Error", "Video not found or is unavailable")
            return

        self.songID += 1
        self.treeView.insert("", "end", values = (self.songID, videoAttributes[0], videoAttributes[1]))

        self.threadQueue.pop(0)
        self.showAddedLabel()


    def removeFromTreeView(self):
        try:
            selectedItem = self.treeView.selection()[0]
        except:
            messagebox.showerror(title = "Error", message = "Select at least one row to delete!")
            return
        else:
            for selectedItem in self.treeView.selection():
                for i, song in enumerate(self.songStreams):
                    if (self.treeView.item(selectedItem)["values"][1] == song["file_name"][:-4]):
                        self.songStreams.pop(i)
                        break

                self.treeView.delete(selectedItem)
                

    def download(self):
        if len(self.threadQueue) > 0:
            messagebox.showwarning("Atention!", "Wait for all the videos to be added")
            return

        self.songID = 0
        self.downloadSongs()

        i = 0
        for video in self.treeView.get_children():
            self.treeView.delete(video)
            i += 1
        
        if i == 0:
            messagebox.showerror("Error", "There are no videos on the list!")
            return

        messagebox.showinfo("Success!", "All the videos were downloaded successfully!")
    

    def openFolder(self):
        localPath = os.getcwd()
        os.startfile(os.path.join(localPath, "sounds"))
