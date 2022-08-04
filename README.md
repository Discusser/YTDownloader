# YTDownloader
Simple python script to download videos from YouTube

# How to use
1. Install dependencies (optionally, you could do this in a virtual environment):
```
pip install -r requirements.txt
```
2. Run the python script
3. Enter the URL of the video you want to download in the search bar

![image](https://user-images.githubusercontent.com/47938380/182882009-e54a2995-35cb-41ee-9413-96ff127ee631.png)

4. Change the settings to your likings
5. Use whichever download button you need. The output path is the current working directory if it is not specified. The file name is:
```
Video only: video_title-VIDEO.file_extension
Audio only: video_title-AUDIO.file_extension
Video and audio: video_title.file_extension
```
Note: The full video is produced by merging the video file and audio file together, so you might see the audio and video files, don't try deleting them, they are removed when the job is done.
