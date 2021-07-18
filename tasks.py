class YT_Tasks():
    def __init__(self):
        super().__init__()

    def youtube_downloader(self):
        self.clear_screen()
        outputdir = os.path.join(self.outputdir_txt.text(), '')
        if len(str(self.info['artist'])) == 0 or len(str(self.info['url'])) == 0 or len(str(self.info['title'])) == 0:
            self.textarea_txt.setText()("URL, artist, and title must be filled out" + "\n")
            return
        outtmpl = self.info['filename'] + '.%(ext)s'
        if audio_chk.get():
            ext = ".mp3"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,
                'youtube_include_dash_manifest': False,
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                     'preferredquality': '192',
                     },
                    {'key': 'FFmpegMetadata'},
                ],
            }
        else:
            ydl_opts = {
                # 'format': 'bestvideo',
                'outtmpl': outtmpl,
                'youtube_include_dash_manifest': False
            }
        launch_btn.update_idletasks()
        with yt.YoutubeDL(ydl_opts) as ydl:
            # info_dict = ydl.extract_info(info['url'], download=False)
            dl_info = ydl.extract_info(self.info['url'], download=True)

        if audio_chk.get():
            mvoutput = make_mp3(ext, outputdir)


        else:
            if dl_info['extractor'] == "youtube":
                ext = ".mkv"
            else:
                ext = ".mp4"
            fullsourcefile = self.info['filename'] + ext
            filedest = outputdir + fullsourcefile
            mvoutput = shutil.move(fullsourcefile, filedest)

        self.textarea_txt.append("\n File saved to " + mvoutput + "\n")

    def make_mp3(self, ext, outputdir):
        # modify mp3 properties
        mp3 = modifymp3.Mp3Modify()
        mp3.modify_mp3_file(self.info['filename'] + ext, self.info)
        fp = file_perms.file_perms()
        sourcefile = self.info['title'] + ext
        filedest = outputdir + sourcefile
        itunesdest = itunesdir + sourcefile
        cpoutput = shutil.copyfile(sourcefile, itunesdest)
        mvoutput = shutil.move(sourcefile, filedest)
        self.textarea_txt.append(cpoutput)
        self.textarea_txt.append(mvoutput)
        fp.grantAccessToFile(filedest, "everyone")
        return mvoutput

    def updateytdl(self):
        title_entry.delete(0, tk.END)

        pipout = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)
        self.textarea_txt.setText()(tk.END, str(pipout) + "\n\n\n")
        ytout = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "youtube-dl"], capture_output=True)
        title_entry.delete(0, tk.END)
        self.textarea_txt.setText()(tk.END, str(ytout))
