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

![image](https://user-images.githubusercontent.com/47938380/180036367-753a27cd-6f7f-489c-a5b7-d0e5cff86aed.png)

4. Choose the settings (there might not be a video available with the specified settings)
5. Use whichever download button you need. The output file is in the current working directory if it is not specified and is named:
```
Video only: video_title-VIDEO.file_extension
Audio only: video_title-AUDIO.file_extension
Video and audio: video_title.file_extension
```
Note: The full video is produced by merging the video file and audio file together, so you might see the audio and video files, don't try deleting them, they are removed when the job is done.