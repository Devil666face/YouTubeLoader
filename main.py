# 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=ADVIT4000&type=channel&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
# 'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UC-sAMvDe7gTmBbub-rWljZg&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
# 'https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId=UC-sAMvDe7gTmBbub-rWljZg&maxResults=50&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
# 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId=PLg5SS_4L6LYvN1RqaVesof8KAf-02fJSi&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
import sys

import requests
import lxml
from bs4 import BeautifulSoup
from config import API_TOKEN
from DB import Database
from download import download_video

def get_json_search(channel_name,url_channel=''):
    try:
        request = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&type=channel&key={API_TOKEN()}")
        data = request.json()
        channel_id = data['items'][0]['id']['channelId']
        return channel_id
    except:
        request = requests.get(url_channel)
        soup = BeautifulSoup(request.text, "lxml")
        channel_title_name = str(soup.title.string).replace(' - YouTube','')
        request = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_title_name}&type=channel&key={API_TOKEN()}")
        data = request.json()
        channel_id = data['items'][0]['id']['channelId']
        return channel_id


def get_json_channel():
    pass

def get_icon(url):
    # request = requests.get(url)
    # return request.content
    return False

def get_json_playlists(channel_id):
    request = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId={channel_id}&maxResults=50&key={API_TOKEN()}")
    data = request.json()
    playlist_ids = data['items']
    playlist_dict = {}
    for playlist in playlist_ids:
        playlist_dict[playlist['id']] = str(playlist['snippet']['title']).replace('"',''), get_icon(playlist['snippet']['thumbnails']['medium']['url'])
        # print(f'Загружаю плейлист '+str(playlist['snippet']['title']).replace('"',''))
    return playlist_dict


def get_json_video(playlist_id):
    request = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=400&playlistId={playlist_id}&key={API_TOKEN()}")
    data = request.json()
    video_ids = data['items']
    video_dict = {}
    for video_obj in video_ids:
        try:
            video_dict[video_obj['contentDetails']['videoId']] = str(video_obj['snippet']['title']).replace('"',''), get_icon(video_obj['snippet']['thumbnails']['medium']['url'])
            #print(f"Считываю видео: {str(video_obj['snippet']['title'])}")
        except:
            print(f"Ошибка добавления видео {video_obj['contentDetails']['videoId']}")
    return video_dict


def get_video_dict_for_playlist(playlist_dict):
    video_dict_for_playlist = {}
    for playlist_id in playlist_dict.keys():
        video_dict_for_playlist[playlist_id] = get_json_video(playlist_id)
    return video_dict_for_playlist


def get_channel_id(url_channel: str):
    try:
        type_of_channel_name = url_channel.split('www.youtube.com')[1].split('/')[1]
        match type_of_channel_name:
            case 'channel':
                channel_id = url_channel.split('www.youtube.com')[1].split('/')[2]
                return channel_id
            case 'c':
                channel_name = url_channel.split('www.youtube.com')[1].split('/')[2]
                return get_json_search(channel_name, url_channel)
            case 'user':
                channel_name = url_channel.split('www.youtube.com')[1].split('/')[2]
                return get_json_search(channel_name, url_channel)
    except:
        return get_json_search(channel_name=url_channel)

def get_current_playlist_name(playlist_dict):
    for (i,playlist_id) in enumerate(playlist_dict.keys()):
        print(f'{i}. {playlist_dict[playlist_id][0]}')

    current_playlist_number = input("Введите цифру плейлиста для загрузки\n")

    for (i, playlist_id) in enumerate(playlist_dict.keys()):
        if i==int(current_playlist_number):
            print(f'Для загрузки выбран плейлист: {playlist_dict[playlist_id][0]}')
            return playlist_id, playlist_dict[playlist_id][0]

def download_playlist(current_playlist_id,current_playlist_name, video_dict_for_playlist):
    video_dict = video_dict_for_playlist[current_playlist_id]
    for video_id in video_dict.keys():
        url_to_video = f"https://www.youtube.com/watch?v={video_id}"
        download_video(url_to_video,current_playlist_name)

if __name__ == '__main__':
    url_channel = ''
    if len(sys.argv)>1:
        url_channel = sys.argv[1]
    else:
        url_channel = input("Отпрвьте ссылку на канал\n")
    db = Database("database.db")
    channel_id = get_channel_id(url_channel.replace('/featured', ''))
    playlist_dict = get_json_playlists(channel_id)
    video_dict_for_playlist = get_video_dict_for_playlist(playlist_dict)
    db.save_all(video_dict_for_playlist, playlist_dict)

    current_playlist_id, current_playlist_name = get_current_playlist_name(playlist_dict)

    download_playlist(current_playlist_id,current_playlist_name,video_dict_for_playlist)

    del db
