import os
import re

import PySimpleGUI as sg
import pytube

layout = [[sg.Text("Enter the URL of the video you want to download, then choose your quality and download")],
          [sg.Text("URL: "), sg.InputText(key="url"), sg.Button("Download (this may take a while)", key="submit")],
          [sg.Text("Quality: "), sg.DropDown(["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p",
                                              "Maximum Resolution"], default_value="720p", key="quality")],
          [sg.Text("FPS: "), sg.DropDown(["30fps", "60fps"], default_value="60fps", key="fps")],
          [sg.Text("Video format:"), sg.DropDown(["mp4", "webm", "3gpp"], default_value="webm", key="format")],
          [sg.Text("Audio quality:"), sg.DropDown(["48kbps", "50kbps", "70kbps", "128kbps",
                                                   "160kbps"], default_value="160kbps",
                                                  key="audioQuality")],
          [sg.Button("Download audio only", key="downAudio"),
           sg.Button("Download video only", key="downVideo")],
          [sg.Text("Choose an output location (Optional)"), sg.Input(key="outputLocation"), sg.FolderBrowse()],
          [sg.Text("Downloading... this may take a while", visible=False, key="downloading")]]
window = sg.Window("Youtube Video Downloader", layout)


def handleAudioDownload(values, location):
    video = pytube.YouTube(values["url"])
    audio = video.streams.filter(only_audio=True, abr=values["audioQuality"]).first()
    print()
    audio.download(filename=re.sub(r'[\/:*?"<>|]', "", video.title) + "-AUDIO." +
                            audio.mime_type.replace("audio/", ""), output_path=location)
    window.Element("downloading").Update(value="Download complete!", visible=True)
    return audio


def handleVideoDownload(values, location):
    quality = values["quality"]
    fps = int(values["fps"].replace("fps", ""))
    vidFormat = values["format"]
    video = pytube.YouTube(values["url"])
    streams = video.streams
    if quality == "Maximum Resolution":
        quality = str(max(map(lambda n: int(n), re.findall(r"(?<=res=\")\d+", streams.all.__str__())))) \
            .__add__("p")
    vidStream = streams.filter(res=quality, fps=fps, file_extension=vidFormat).first()
    vidStream.download(filename=re.sub(r'[\/:*?"<>|]', "", video.title) + "-VIDEO." +
                                vidStream.mime_type.replace("video/", ""), output_path=location)
    window.Element("downloading").Update(value="Download complete!", visible=True)
    return vidStream


global vidFile, audioFile
vidFile = ""
audioFile = ""


def handleDownload(values, location):
    global vidFile, audioFile
    video = pytube.YouTube(values["url"])
    try:
        legalTitle = re.sub(r'[\/:*?"<>|]', "", video.title)
        audio = handleAudioDownload(values, location)
        audioFile = location + "/" + legalTitle + "-AUDIO." + audio.mime_type.replace("audio/", "")
        vidStream = handleVideoDownload(values, location)
        vidExtension = vidStream.mime_type.replace("video/", "")
        vidFile = location + "/" + legalTitle + "-VIDEO." + vidExtension
        print(vidFile)
        os.system("ffmpeg -i \"" + vidFile + "\" -i \"" + audioFile + "\" -c copy \"" + location + "/" +
                  legalTitle + "." + vidExtension + "\"")
        os.remove(vidFile)
        os.remove(audioFile)
    except AttributeError:
        try:
            print(vidFile)
            os.remove(vidFile)
        except FileNotFoundError:
            pass
        try:
            print(audioFile)
            os.remove(audioFile)
        except FileNotFoundError:
            pass
        window.Element("downloading").Update(value="Could not find video with the specified settings", visible=True)
        return
    window.Element("downloading").Update(value="Download complete!", visible=True)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == "submit":
        location = os.getcwd() if values["outputLocation"] == "" else values["outputLocation"]
        handleDownload(values, location)
    if event == "downVideo":
        location = os.getcwd() if values["outputLocation"] == "" else values["outputLocation"]
        handleVideoDownload(values, location)
    if event == "downAudio":
        location = os.getcwd() if values["outputLocation"] == "" else values["outputLocation"]
        handleAudioDownload(values, location)

window.close()
