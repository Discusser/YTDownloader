import os
import re
import threading
from collections import OrderedDict

import PySimpleGUI as sg
import pytube

from pytube.exceptions import RegexMatchError

layout = [[sg.Text("Enter the URL of the video you want to download, then choose your quality and download")],
          [sg.Text("URL: "), sg.InputText(key="url", enable_events=True),
           sg.Button("Submit", key="submit")],
          [sg.Text("Video Quality: "), sg.DropDown(["                "], key="quality")],
          [sg.Text("Audio quality: "), sg.DropDown(["                "], key="audioQuality")],
          [sg.Text("Output path:"), sg.Input(key="outputLocation", default_text=os.getcwd()),
           sg.FolderBrowse()],
          [sg.Text("Filename:"), sg.Input(key="filename", enable_events=True)],
          [sg.Button("Download audio and video", key="download"),
           sg.Button("Download audio only", key="downAudio"),
           sg.Button("Download video only", key="downVideo")],
          [sg.Text(visible=False, key="error")]]
window = sg.Window("Youtube Video Downloader", layout, finalize=True)

dropdowns = ["quality", "audioQuality", "format"]


def submitURL():
    try:
        video = pytube.YouTube(window["url"].get())
        window["error"].update(visible=False)
        qualityValues = []
        audioValues = []
        for stream in video.streams:
            if stream.includes_video_track and not stream.includes_audio_track:
                if stream.resolution is not None:
                    qualityValues.append(stream.mime_type.replace("video/", "").capitalize() + " " +
                                         stream.resolution + str(stream.fps))
            elif stream.includes_audio_track and not stream.includes_video_track:
                audioValues.append(stream.abr)
        qualityValues.sort(key=lambda elem: re.sub(r'(?<=\w\b).*', "", elem))
        window["quality"].update(values=list(OrderedDict.fromkeys(qualityValues)))
        audioValues = list(map(lambda string: int(string.replace("kbps", "")), audioValues))
        audioValues.sort(reverse=True)
        audioValues = list(map(lambda num: str(num) + "kbps", audioValues))
        window["audioQuality"].update(values=audioValues)
        window["filename"].update(value=video.title)
    except RegexMatchError:
        window["error"].update(visible=True, value="Invalid URL, please verify that you inputted the right link.")
        threading.Timer(5.0, lambda: window["error"].update(visible=False)).start()


def download():
    vidFormat = downloadVideo()
    audioFormat = downloadAudio()
    filename = window["filename"].get()
    outputLocation = window["outputLocation"].get()
    video = outputLocation + "/" + filename + "-VIDEO." + vidFormat
    audio = outputLocation + "/" + filename + "-AUDIO." + audioFormat
    print(video)
    print(audio)
    os.system(
        "ffmpeg -i "
        "\"" + video + "\" "
        "-i "
        "\"" + audio + "\" "
        "-c copy "
        "\"" + outputLocation + "/" + filename + ".mp4" + "\""
    )
    os.remove(video)
    os.remove(audio)


def downloadVideo() -> str:
    settings = window["quality"].get()
    _format = re.search(r'\w+?\b', settings)[0].lower()
    quality = re.search(r'\d+?p', settings)[0]
    fps = re.search(r'(?<=p)\d+$', settings)[0]
    video = pytube.YouTube(window["url"].get())
    video.streams.filter(mime_type="video/" + _format, res=quality, fps=int(fps)).first().download(
        filename=window["filename"].get() + "-VIDEO." + _format,
        output_path=window["outputLocation"].get()
    )
    return _format


def downloadAudio() -> str:
    quality = window["audioQuality"].get()
    video = pytube.YouTube(window["url"].get())
    print(video.streams.filter(abr=quality))
    stream = video.streams.filter(abr=quality).first()
    _format = stream.mime_type.replace("audio/", "")
    stream.download(
        filename=window["filename"].get() + "-AUDIO." + _format,
        output_path=window["outputLocation"].get()
    )
    return _format


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == "submit":
        submitURL()
    if event == "filename":
        window["filename"].update(value=re.sub(r'[/:*?"<>|]', "", window["filename"].get()))
    if event == "download":
        download()
    if event == "downVideo":
        downloadVideo()
    if event == "downAudio":
        downloadAudio()

window.close()
