# yt-downloader
## Pip package requirements
* yt-dlp
* pywin32
* mutagen
* PyQt5
* future

## External package dependencies
* ffmpeg
  * see the following article on how to get the Windows version
  * (dead site linked) - https://stackoverflow.com/a/41822439/6044564
  * See https://github.com/BtbN/FFmpeg-Builds for up-to-date builds
  * Place the Windows binaries (3) in either of the following
    * \<virtual environment\>/Scripts
    * A location in path (or add location to the user/system path)

## Description
Download videos using yt-dlp through a basic UI

This can download either videos and/or audio. Audio is automatically converted to mp3

Copies audio files to 2 locations if `itunesdir` value in the `default_locations.txt` file is set to anything other than null.<br>
Set the value to `null` (default) to skip copying the file to a second location.
