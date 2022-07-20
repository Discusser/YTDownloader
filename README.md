# YTDownloader
Simple python script to download videos from YouTube

# How to use
1. Install `PySimpleGUI` and `pytube`:
```
py -m pip install PySimpleGUI
py -m pip install pytube
```
2. Run the python script
3. Enter the URL of the video you want to download in the search bar

![image](https://user-images.githubusercontent.com/47938380/180030754-ce545e93-f00f-41bf-9e89-2136efee32b8.png)

4. Choose the settings (there might not be a video available with the specified settings)
5. Use whichever download button you need, the output file is:
```
Video only: video_title-VIDEO.file_extension
Audio only: video_title-AUDIO.file_extension
Video and audio: video_title.file_extension
```