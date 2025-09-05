from mutagen.easyid3 import EasyID3
import pathlib
from os import path, replace
import tkinter as tk
from tkinter import filedialog
import re
import io


class Mp3Modify:
    def select_files(self):
        # ask for location of file(s)
        root = tk.Tk()
        root.withdraw()
        # open individual file
        # file_path = filedialog.askopenfilename()
        # open directory
        file_path = filedialog.askopenfiles(filetypes=(
            ("mp3 files", "*.mp3"), ("all files", "*.*")))
        root.destroy()
        self.get_files(file_path)

    def get_files(self, item_path):
        if isinstance(item_path, list):
            self.modify_mp3_file(item_path)
        elif path.isdir(item_path):
            for mp3file in pathlib.Path(item_path).glob('*.mp3'):
                self.modify_mp3_file(mp3file)
        else:
            self.modify_mp3_file(item_path)

    def modify_mp3_file(self, files, info):
        if isinstance(files, str):
            new_f = io.open(files, "r")
            new_filename = self.modemp3(new_f, info)
        else:
            for f in files:
                if isinstance(f, io.IOBase):
                    self.modemp3(f, info)
                else:
                    # check if file
                    if not f[-4:] == ".mp3":
                        return print(f + " is not an mp3")
                    new_f = io.open(f, "rw")
                    new_filename = self.modemp3(new_f, info)
        return new_filename

    def modemp3(self, mp3file, info):
        file = mp3file.name
        # check if mp3 extension
        if file.endswith('.mp3'):
            if '-' in file:
                print('Processing file: ' + file)
                # artist = path.basename(file).split('-', 1)[0]
                artist = info['artist']
                # artist = path.basename(file).rsplit('-', 1)[0]
                dirpath = pathlib.Path(file).parent
                newfilename = re.sub('^' + artist + '-',
                                     '', path.basename(file))
                newpath = str(dirpath) + '\\' + newfilename
                title = str(path.splitext(newfilename)[0])
                audio = EasyID3(file)
                audio['artist'] = artist
                audio['albumartist'] = artist
                audio['title'] = title
                audio['genre'] = info['genre']
                # audio['album'] = u"My album"
                # audio['composer'] = u""  # clear
                audio.save(v2_version=3)
                # close open file
                mp3file.close()
                replace(file, newpath)
                return newfilename
            else:
                print('hyphen (-) not in file name for ' + file)
        else:
            print(file + ' is not an MP3 file')
