from classes.programGUI import ProgramGUI
from functions.aux_functions import createDesktopShortcut

def main():
    createDesktopShortcut()
    
    programGUI = ProgramGUI()
    programGUI.initGUI()


if __name__ == "__main__":
    main()



#
#
#
# python3 -m PyInstaller --noconsole --onedir --icon=img/icon.ico --name="Youtube Song Downloader" downloader.py
#
#
#