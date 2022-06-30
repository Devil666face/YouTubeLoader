import sys
import os
from pytube import YouTube

def download_video(url,playlist_name,exec_path_for_windows):
    video_obj = YouTube(url)
    stream = video_obj.streams.get_highest_resolution()
    if exec_path_for_windows!='None':
        if playlist_name!='None':
            stream.download(f'{exec_path_for_windows}/videos/{playlist_name}', f'{stream.title}.mp4')
        else:
            stream.download(f'{exec_path_for_windows}/videos', f'{stream.title}.mp4')
    else:
        if playlist_name!='None':
            stream.download(f'{os.getcwd()}/videos/{playlist_name}', f'{stream.title}.mp4')
        else:
            stream.download(f'{os.getcwd()}/videos', f'{stream.title}.mp4')


if __name__=='__main__':
    url_video = sys.argv[1]
    playlist_name='None'
    exec_path_for_windows='None'
    if len(sys.argv)>2:
        playlist_name = sys.argv[2]
    if len(sys.argv)>3:
        exec_path_for_windows = sys.argv[3]

    print(url_video, playlist_name, exec_path_for_windows)
    download_video(url_video,playlist_name,exec_path_for_windows)