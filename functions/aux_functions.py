import os
import winshell
from win32com.client import Dispatch

def createDesktopShortcut():
    local_path = os.getcwd()
    desktop = winshell.desktop()
    shortcutPath = os.path.join(desktop, "Youtube Song Downloader.lnk")
    target = os.path.join(local_path, "Youtube Song Downloader.exe")
    iconPath = os.path.join(local_path, "img/icon.ico")

    if not os.path.exists(shortcutPath):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcutPath)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = local_path
        shortcut.IconLocation = iconPath
        shortcut.save()