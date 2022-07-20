import os
from pytube import YouTube

def download_video(url,current_playlist_name):
    try:
        video_obj = YouTube(url)
        stream = video_obj.streams.get_highest_resolution()
        print(f"Скачиваю видео: {stream.title}")
        stream.download(f'{os.getcwd()}/videos/{current_playlist_name.replace("/","")}', f'{stream.title.replace("/","")}.mp4')
    except Exception as ex:
        print(f"Возникла ошибка при скачивании видео: {stream.title}\nКод ошибки: {ex}")
