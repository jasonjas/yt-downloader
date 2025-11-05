#!/usr/bin/python
import contextlib
import io
import os
import shutil
import file_perms
import modifymp3
import manage_files
import yt_dlp as yt
import sys
import re
import subprocess
from typing import Dict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.statusbar()

    def statusbar(self):
        self.statusBar().showMessage('ready')


class MainWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        defaults = manage_files.DefaultLocations()
        dvars = defaults.load_vars()
        self.outputdir_initial = dvars['outputdir_initial']
        self.itunesdir = dvars['itunesdir']
        self.historyfile = dvars['historyfile']
        self.genres_file = dvars['genres_file']

        # text boxes
        self.url_txt = tk.Entry(self, width=40)
        self.artist_txt = tk.Entry(self, width=40)
        self.title_txt = tk.Entry(self, width=40)
        self.outputdir_txt = tk.Entry(self, width=40)
        self.textarea_txt = tk.Text(self, width=80, height=20)
        # buttons
        self.selectdir_btn = tk.Button(
            self, text="select directory", command=self.getdirectory)
        self.listformats_btn = self.listformats_btn = tk.Button(
            self, text="list formats", command=self.getformats)
        self.gettitle_btn = tk.Button(
            self, text="get title", command=self.gettitle)
        self.getmetadata_btn = tk.Button(
            self, text="get metadata", command=self.getmetadata)
        self.updateyoutube_btn = tk.Button(
            self, text="update YT", command=self.updateytdl)
        self.editgenres_btn = tk.Button(
            self, text="list genres", command=lambda: self.edit_genre("list"))
        self.savegenres_btn = tk.Button(
            self, text="save genres", command=lambda: self.edit_genre("save"))
        self.close_btn = tk.Button(self, text="close", command=self.quit)
        self.clearlog_btn = tk.Button(
            self, text="clear log", command=self.clear_screen)
        self.reset_btn = tk.Button(self, text="reset", command=self.reset)
        self.download_btn = tk.Button(
            self, text="download", command=self.youtube_downloader)
        self.allhistory_btn = tk.Button(
            self, text="all history", command=self.get_history)
        self.somehistory_btn = tk.Button(
            self, text="history(5)", command=lambda: self.get_history(5))

        # dropdown
        self.genre_btn = ttk.Combobox(self, width=30)

        # checkbox
        self.audio_chk_box_var = tk.BooleanVar()
        self.audio_chk_box = tk.Checkbutton(
            self, text="audio only", variable=self.audio_chk_box_var)

        # Layout
        self.initUI()
        self.reset()

    def statusbar(self):
        mw = self.MainWindow()
        mw.statusbar()

    def initUI(self):
        labels = ["URL", "Artist", "Title", "Output Dir"]
        entries = [self.url_txt, self.artist_txt,
                   self.title_txt, self.outputdir_txt]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="w")
            entry.grid(row=i, column=1, columnspan=3, sticky="we")

        # Buttons row
        btns = [self.selectdir_btn, self.listformats_btn, self.gettitle_btn, self.getmetadata_btn,
                self.updateyoutube_btn, self.editgenres_btn, self.savegenres_btn, self.allhistory_btn,
                self.audio_chk_box, self.genre_btn, self.close_btn, self.clearlog_btn,
                self.somehistory_btn, self.reset_btn, self.download_btn]

        for idx, b in enumerate(btns):
            b.grid(row=4 + idx // 5, column=idx %
                   5, sticky="we", padx=2, pady=2)

        # Text area
        self.textarea_txt.grid(
            row=10, column=0, columnspan=5, sticky="nsew", pady=5)

    def getformats(self):
        info = self.getinfo()
        if not self.check_url(str(info['url'])):
            return
        else:
            f = io.StringIO()
            # getformats_btn.update_idletasks()
            with contextlib.redirect_stdout(f):
                with yt.YoutubeDL() as ydl:
                    info_dict = ydl.extract_info(info['url'], download=False)
                    formats = ydl.list_formats(info_dict)
                # getformats_btn.update_idletasks()
                s = f.getvalue()
                self.textarea_txt.insert("1.0", s)

    def getmetadata(self):
        self.clear_screen()
        info = self.getinfo()
        if not self.check_url(str(info['url'])):
            return
        else:
            with yt.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(info['url'], download=False)
            self.textarea_txt.insert("1.0", str(info_dict))

    def check_url(self, _string):
        # check if string is a url
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if len(_string) == 0 or not _string:
            self.textarea_txt.insert("1.0", "URL must be filled out \n")
        else:
            # returns true of false
            if not re.match(regex, _string):
                self.textarea_txt.insert("1.0", "URL must be a valid URL \n")
        return re.match(regex, _string)

    def gettitle(self):
        info = self.getinfo()
        if not self.check_url(str(info['url'])):
            return
        else:
            with yt.YoutubeDL() as ydl:
                try:
                    info_dict = ydl.extract_info(info['url'], download=False)
                except yt.utils.UnsupportedError as e:
                    self.textarea_txt.insert("1.0", str(e))
                    return
                except yt.utils.DownloadError as e:
                    self.textarea_txt.insert("1.0", str(e.exc_info))
                    return
                except:
                    e = sys.exc_info()[0]
                    self.textarea_txt.insert("1.0", str(e.url))
                    return
                
            # strip out non-standard characters
            if 'title' not in info_dict:
                self.textarea_txt.insert(
                    "1.0", "title not in results, stopping")
                return
            title = info_dict['title']
            char_list = [title[j] for j in range(
                len(title)) if ord(title[j]) in range(65536)]
            info_dict['title'] = ''
            for c in char_list:
                info_dict['title'] = info_dict['title'] + c

            if info_dict['extractor'] == "youtube" and 'alt_tile' in info_dict:
                self.textarea_txt.insert(tk.END,
                                         info_dict['title'] + "\n" + info_dict['alt_title'])
                self.title_txt.insert(1, info_dict['alt_title'])
            else:
                self.textarea_txt.insert(tk.END, info_dict['title'])
                self.title_txt.insert(1, info_dict['title'])

    def getdirectory(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.outputdir_txt.delete(0, tk.END)
            self.outputdir_txt.insert(0, dirname)

    def reset_output_dir(self):
        self.outputdir_txt.delete(0, tk.END)
        self.outputdir_txt.insert(0, self.outputdir_initial)

    def clear_screen(self):
        self.textarea_txt.delete("1.0", tk.END)

    def reset(self):
        self.clear_screen()
        self.reset_output_dir()
        self.url_txt.delete(0, tk.END)
        self.artist_txt.delete(0, tk.END)
        self.title_txt.delete(0, tk.END)
        self.populate_genre_dropdown()

    def replace_invalid_characters(self, string):
        # type: (str) -> str
        invalid = '<>:"/\\|?*#'
        filename = string
        for char in invalid:
            if char in string:
                filename = string.replace(char, '')
        return filename

    def getinfo(self):
        # type: () -> Dict
        ret = {}
        url = self.url_txt.get().split('&')[0]
        artist = self.artist_txt.get().replace("'", "")
        title = self.title_txt.get().replace("'", "")
        # genre = self.genre_btn.itemText(self.genre_btn.currentIndex())
        genre = self.genre_btn.get()

        ret['url'] = url
        ret['artist'] = artist
        ret['title'] = title
        ret['filename'] = self.replace_invalid_characters(artist + "-" + title)
        ret['genre'] = genre
        return ret

    def populate_genre_dropdown(self):
        g = manage_files.EditGenre(self.genres_file)
        genres = g.get_genre()
        self.genre_btn["values"] = genres
        if genres:
            self.genre_btn.current(0)

    def edit_genre(self, action="list"):
        g = manage_files.EditGenre(self.genres_file)
        if action == "list":
            genres = g.get_genre()
            # self.textarea_txt.insert("1.0", ''.join(genres))
            self.textarea_txt.insert("1.0", ''.join(genres))
        elif action == "save":
            genres = g.save_genre(self.textarea_txt.get("1.0", tk.END))
            self.populate_genre_dropdown()
        else:
            msgbox = messagebox.askyesno("Edit Genre Action", f"Action {action} is not defined")
            # msgbox.warning(self, "Edit Genre Action", "Action " +
            #                action + " is not defined", tk.Message.)
            # msgbox.exec_()

    def get_history(self, max_history=0):
        h = manage_files.History(self.historyfile)
        self.textarea_txt.insert("1.0", str(h.read_history(max_history)))

    def test_history(self):
        self.save_history("first_line", "test-file")

    def save_history(self, url, saved_file):
        h = manage_files.History(self.historyfile)
        h.save_history(url, saved_file)

    def youtube_downloader(self):
        info = self.getinfo()
        ext = ''
        self.clear_screen()
        outputdir = os.path.join(self.outputdir_txt.get(), '')
        if len(str(info['artist'])) == 0 or len(str(info['url'])) == 0 or len(str(info['title'])) == 0:
            self.textarea_txt.insert("1.0",
                "URL, artist, and title must be filled out" + "\n")
            return
        elif not self.check_url(str(info['url'])):
            return
        outtmpl = info['filename'] + '.%(ext)s'
        if self.audio_chk_box_var.get() == 1:
            ext = ".mp3"
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': outtmpl,
                'youtube_include_dash_manifest': False,
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                     'preferredquality': '192',
                     },
                    {'key': 'FFmpegMetadata'},
                ],
            }
            self.textarea_txt.insert("1.0", "Downloading audio...")
            self.textarea_txt.update()
        else:
            ydl_opts = {
                # 'format': 'bestvideo',
                'outtmpl': outtmpl,
                'youtube_include_dash_manifest': False
            }
            self.textarea_txt.insert("1.0", "Downloading video...")
            self.textarea_txt.update()
        with yt.YoutubeDL(ydl_opts) as ydl:
            try:
                # info_dict = ydl.extract_info(info['url'], download=False)
                dl_info = ydl.extract_info(info['url'], download=True)
                # self.file_location = dl_info['requested_downloads'][0]['filepath']

                # output_filename = os.path.splitext(os.path.basename(dl_info['requested_downloads'][0]['filepath']))
                output_filename = dl_info['requested_downloads'][0]['filepath']
                new_path = os.path.join(os.path.split(output_filename)[0],
                                        info['filename'] + os.path.splitext(output_filename)[1])
                # rename to new filename
                os.replace(output_filename, new_path)

            except yt.utils.UnsupportedError as e:
                self.textarea_txt.insert("1.0", str(e))
                return
            except Exception as e:
                self.textarea_txt.insert("1.0", str(e))
                return

        if self.audio_chk_box_var.get() == 1:
            self.textarea_txt.insert(tk.END, "\nConverting to MP3")
            self.textarea_txt.update()
            mvoutput = self.make_mp3(ext, outputdir)

        else:
            ext = "." + dl_info['ext']
            fullsourcefile = info['filename'] + ext
            filedest = outputdir + fullsourcefile
            mvoutput = shutil.move(fullsourcefile, filedest)

        self.textarea_txt.insert(tk.END, "\nFile saved to " + mvoutput + "\n")
        self.save_history(info['url'], info['filename'])

    def make_mp3(self, ext, outputdir):
        info = self.getinfo()
        # modify mp3 properties
        mp3 = modifymp3.Mp3Modify()
        sourcefile = mp3.modify_mp3_file(info['filename'] + ext, info)
        fp = file_perms.file_perms()
        # sourcefile = info['filename'] + ext
        filedest = outputdir + sourcefile
        if self.itunesdir != "null":
            itunesdest = self.itunesdir + sourcefile
            cpoutput = shutil.copyfile(sourcefile, itunesdest)
            self.textarea_txt.insert(tk.END, f"\ncpoutput")
        mvoutput = shutil.move(sourcefile, filedest)
        self.textarea_txt.insert(tk.END, mvoutput)
        fp.grantAccessToFile(filedest, "everyone")
        return mvoutput

    def updateytdl(self):
        self.title_txt.delete(0, tk.END)
        self.textarea_txt.insert(tk.END, "Updating yt-dlp...")
        # force textarea to display text
        self.textarea_txt.update()
        # pipout = subprocess.run(
        #     [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)
        # self.textarea_txt.insert("1.0", str(pipout) + "\n\n\n")
        ytout = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], capture_output=True)
        self.textarea_txt.insert(tk.END, f"\n{str(ytout)}")


if __name__ == "__main__":
    app = MainWidget()
    app.mainloop()
