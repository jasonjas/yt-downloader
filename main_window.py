#!/usr/bin/python
import contextlib
import io
import os
import shutil
import file_perms
import modifymp3
import manage_files
import yt_dlp as yt
from yt_dlp.utils import download_range_func
import sys
import re
import subprocess
from typing import Dict
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication, QLineEdit, QLabel, QTextEdit, QMainWindow, QFileDialog,
                             QCheckBox, QComboBox, QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusbar()

    def statusbar(self):
        self.statusBar().showMessage('ready')


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        defaults = manage_files.DefaultLocations()
        dvars = defaults.load_vars()
        self.outputdir_initial = dvars['outputdir_initial']
        self.itunesdir = dvars['itunesdir']
        self.historyfile = dvars['historyfile']
        self.genres_file = dvars['genres_file']

        # text boxes
        self.url_txt = QLineEdit()
        self.artist_txt = QLineEdit()
        self.title_txt = QLineEdit()
        self.outputdir_txt = QLineEdit()
        self.textarea_txt = QTextEdit()
        self.start_time_txt = QLineEdit()
        self.end_time_txt = QLineEdit()
        # buttons
        self.selectdir_btn = QPushButton('select directory')
        self.listformats_btn = QPushButton('list formats')
        self.gettitle_btn = QPushButton('get title')
        self.getmetadata_btn = QPushButton('get metadata')
        self.updateyoutube_btn = QPushButton('update YT')
        self.editgenres_btn = QPushButton('list genres')
        self.savegenres_btn = QPushButton('save genres')
        self.close_btn = QPushButton('close', self)
        self.clearlog_btn = QPushButton('clear log')
        self.reset_btn = QPushButton('reset')
        self.download_btn = QPushButton('download')
        self.allhistory_btn = QPushButton('all history')
        self.somehistory_btn = QPushButton('history(5)')
        self.help_btn = QPushButton('Help')

        # drop-down
        self.genre_btn = QComboBox()

        # checkbox
        self.audio_chk_box = QCheckBox("audio only")

        # self.statusbar()
        self.initUI()
        self.yt_events()

    def yt_events(self):
        self.close_btn.clicked.connect(QApplication.instance().quit)
        self.reset_btn.clicked.connect(lambda: self.reset())
        self.selectdir_btn.clicked.connect(lambda: self.getdirectory())
        self.getmetadata_btn.clicked.connect(lambda: self.getmetadata())
        self.gettitle_btn.clicked.connect(lambda: self.gettitle())
        self.clearlog_btn.clicked.connect(lambda: self.clear_screen())
        self.editgenres_btn.clicked.connect(lambda: self.edit_genre("list"))
        self.savegenres_btn.clicked.connect(lambda: self.edit_genre("save"))
        self.allhistory_btn.clicked.connect(lambda: self.get_history())
        self.somehistory_btn.clicked.connect(lambda: self.get_history(5))
        self.help_btn.clicked.connect(lambda: self.help_text())

        # self.editgenres_btn.clicked.connect(lambda: self.test_history())
        self.listformats_btn.clicked.connect(lambda: self.getformats())
        self.updateyoutube_btn.clicked.connect(lambda: self.updateytdl())
        self.download_btn.clicked.connect(lambda: self.youtube_downloader())

    def statusbar(self):
        mw = self.MainWindow()
        mw.statusbar()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        url_label = QLabel('URL')
        artist_label = QLabel('Artist')
        title_label = QLabel('Title')
        outputdir_label = QLabel('Output Dir')
        start_time_label = QLabel('Start Time')
        end_time_label = QLabel('End Time')

        names = [url_label, self.url_txt, artist_label, self.artist_txt,
                 title_label, self.title_txt, outputdir_label, self.outputdir_txt,
                 self.selectdir_btn, self.listformats_btn, self.gettitle_btn, self.getmetadata_btn,
                 self.updateyoutube_btn,
                 self.editgenres_btn, self.savegenres_btn, self.allhistory_btn, self.audio_chk_box, self.genre_btn,
                 self.close_btn, self.clearlog_btn, self.somehistory_btn, self.reset_btn, self.download_btn, 
                 start_time_label, self.start_time_txt, end_time_label, self.end_time_txt, self.help_btn]

        # set row, col, and count vars
        x = 0
        count = 0
        col_buttons = 5
        row_buttons = 4
        col_text = 2
        row_text = 4

        # Text labels
        positions = [(i, j) for i in range(row_text) for j in range(col_text)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            grid.addWidget(name, *position, 1, col_buttons)
            count = count + 1
            x = position[0] + 1

        # buttons
        # start at next row (x)
        positions2 = [(h, k) for h in range(x, x + row_buttons)
                      for k in range(col_buttons)]
        for position2, name2 in zip(positions2, names[count:]):
            if name2 == '':
                continue
            grid.addWidget(name2, *position2)
            x = x + 1

        grid.addWidget(self.textarea_txt, x, 0, 10, 10)
        self.url_txt.setFocus()

        # self.move(300, 150)
        self.setWindowTitle('Youtube Download')
        self.reset()
        # self.show()

    def help_text(self):
        """
        Display help text in the textarea box
        """
        with open('help.txt', 'r') as ht:
            help_text = ht.read()
        self.textarea_txt.setText(help_text)

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
                self.textarea_txt.setText(s)

    def getmetadata(self):
        self.clear_screen()
        info = self.getinfo()
        if not self.check_url(str(info['url'])):
            return
        else:
            with yt.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(info['url'], download=False)
            self.textarea_txt.setText(str(info_dict))

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
            self.textarea_txt.setText("URL must be filled out \n")
        else:
            # returns true of false
            if not re.match(regex, _string):
                self.textarea_txt.setText("URL must be a valid URL \n")
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
                    self.textarea_txt.setText(str(e))
                    return
                except yt.utils.DownloadError as e:
                    self.textarea_txt.setText(str(e.exc_info))
                    return
                except:
                    e = sys.exc_info()[0]
                    self.textarea_txt.setText(str(e.url))
                    return
            # strip out non-standard characters
            if 'title' not in info_dict:
                self.textarea_txt.setText("title not in results, stopping")
                return
            title = info_dict['title']
            char_list = [title[j] for j in range(
                len(title)) if ord(title[j]) in range(65536)]
            info_dict['title'] = ''
            for c in char_list:
                info_dict['title'] = info_dict['title'] + c

            if info_dict['extractor'] == "youtube" and 'alt_tile' in info_dict:
                self.textarea_txt.append(
                    info_dict['title'] + "\n" + info_dict['alt_title'])
                self.title_txt.setText(info_dict['alt_title'])
            else:
                self.textarea_txt.append(info_dict['title'])
                self.title_txt.setText(info_dict['title'])

    def getdirectory(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        self.outputdir_txt.setText(dlg.getExistingDirectory())

    def reset_output_dir(self):
        self.outputdir_txt.setText(self.outputdir_initial)

    def clear_screen(self):
        self.textarea_txt.clear()

    def reset(self):
        self.clear_screen()
        self.reset_output_dir()
        self.url_txt.clear()
        self.artist_txt.clear()
        self.title_txt.clear()
        self.set_start_end_time()
        self.populate_genre_dropdown()
        self.url_txt.setFocus()

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
        url = self.url_txt.text().split('&')[0]
        artist = self.artist_txt.text().replace("'", "")
        title = self.title_txt.text().replace("'", "")
        genre = self.genre_btn.itemText(self.genre_btn.currentIndex())

        ret['url'] = url
        ret['artist'] = artist
        ret['title'] = title
        ret['filename'] = self.replace_invalid_characters(artist + "-" + title)
        ret['genre'] = genre
        return ret
    
    def set_start_end_time(self):
        # type: () -> None
        self.start_time_txt.setText('0:00')
        self.end_time_txt.setText('inf')

    def get_sec(self, time_str):
        # type: (str) -> int
        """Get seconds from time string like 1:30
        https://stackoverflow.com/a/6402934
        """
        secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))
        return secs

    def get_start_end_time(self, start_or_end):
        # type: (str) -> str
        if start_or_end == 'start':
            default_value = "0"
            time_data = self.start_time_txt.text()
        if start_or_end == 'end':
            default_value = "inf"
            time_data = self.end_time_txt.text()
        try:
            time_data = self.get_sec(time_data)
        except:
            # return default value if error getting seconds
            time_data = default_value
        return time_data

    def populate_genre_dropdown(self):
        # genre dropdown
        g = manage_files.EditGenre(self.genres_file)
        genres = g.get_genre()
        self.genre_btn.clear()
        for x in genres:
            self.genre_btn.addItem(x)

    def edit_genre(self, action="list"):
        g = manage_files.EditGenre(self.genres_file)
        if action == "list":
            genres = g.get_genre()
            self.textarea_txt.setText(''.join(genres))
        elif action == "save":
            genres = g.save_genre(self.textarea_txt.toPlainText())
            self.populate_genre_dropdown()
        else:
            msgbox = QMessageBox
            msgbox.warning(self, "Edit Genre Action", "Action " +
                           action + " is not defined", QMessageBox.Yes)
            msgbox.exec_()

    def get_history(self, max_history=0):
        h = manage_files.History(self.historyfile)
        self.textarea_txt.setText(str(h.read_history(max_history)))

    def test_history(self):
        self.save_history("first_line", "test-file")

    def save_history(self, url, saved_file):
        h = manage_files.History(self.historyfile)
        h.save_history(url, saved_file)

    def youtube_downloader(self):
        info = self.getinfo()
        ext = ''
        self.clear_screen()
        outputdir = os.path.join(self.outputdir_txt.text(), '')
        if len(str(info['artist'])) == 0 or len(str(info['url'])) == 0 or len(str(info['title'])) == 0:
            self.textarea_txt.setText(
                "URL, artist, and title must be filled out" + "\n")
            return
        elif not self.check_url(str(info['url'])):
            return
        outtmpl = info['filename'] + '.%(ext)s'
        if self.audio_chk_box.isChecked():
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
                'download_ranges': download_range_func(None, [(self.get_start_end_time('start'), self.get_start_end_time('end'))]),
                'force_keyframes_at_cuts': True
            }
        else:
            ydl_opts = {
                # 'format': 'bestvideo',
                'outtmpl': outtmpl,
                'youtube_include_dash_manifest': False
            }
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
                self.textarea_txt.setText(str(e))
                return
            except Exception as e:
                self.textarea_txt.setText(str(e))
                return

        if self.audio_chk_box.isChecked():
            mvoutput = self.make_mp3(ext, outputdir)

        else:
            ext = "." + dl_info['ext']
            fullsourcefile = info['filename'] + ext
            filedest = outputdir + fullsourcefile
            mvoutput = shutil.move(fullsourcefile, filedest)

        self.textarea_txt.append("\n File saved to " + mvoutput + "\n")
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
            self.textarea_txt.append(cpoutput)
        mvoutput = shutil.move(sourcefile, filedest)
        self.textarea_txt.append(mvoutput)
        fp.grantAccessToFile(filedest, "everyone")
        return mvoutput

    def updateytdl(self):
        self.title_txt.clear()
        pipout = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)
        self.textarea_txt.setText(str(pipout) + "\n\n\n")
        ytout = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], capture_output=True)
        self.textarea_txt.append(str(ytout))


def main():
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())
