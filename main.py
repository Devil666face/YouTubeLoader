import sys
from pytube import YouTube

def load_video(url):
    video_obj = YouTube(url)
    stream = video_obj.streams.get_highest_resolution()
    stream.download('/home/king/Загрузки/',f'{video_obj.title}.mp4')

if __name__ == '__main__':
    url = input("Отправьте url видео\n")
    load_video(url)