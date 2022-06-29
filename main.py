#'https://www.googleapis.com/youtube/v3/search?part=snippet&q=ADVIT4000&type=channel&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
#'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UC-sAMvDe7gTmBbub-rWljZg&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
#'https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId=UC-sAMvDe7gTmBbub-rWljZg&maxResults=50&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'
#'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId=PLg5SS_4L6LYvN1RqaVesof8KAf-02fJSi&key=AIzaSyBI8LuIFg3lxi1cl7OIscifGeraB3bKnwM'

import requests
import lxml
import json
from config import API_TOKEN
from bs4 import BeautifulSoup

def get_json_search(channel_name):
    request = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&type=channel&key={API_TOKEN}")
    data = request.json()
    channel_id = data['items'][0]['id']['channelId']
    return channel_id

def get_json_channel():
    pass

def get_json_playlists(channel_id):
    request = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId={channel_id}&maxResults=50&key={API_TOKEN}")
    data = request.json()
    playlist_ids = data['items']
    playlist_dict = {}
    for playlist in playlist_ids:
        playlist_dict[playlist['id']]=playlist['snippet']['title'],playlist['snippet']['thumbnails']['medium']['url']
        # playlist_id_list.append(playlist['id'])
        # print(playlist['snippet']['title'])
        # print(playlist['snippet']['thumbnails']['medium']['url'])
    return playlist_dict

def get_json_video(playlist_id):
    request = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={playlist_id}&key={API_TOKEN}")
    data = request.json()
    video_ids = data['items']
    video_dict = {}
    for video_obj in video_ids:
        try:
            print(video_obj['contentDetails']['videoId'])
            print(video_obj['snippet']['title'])
            print(video_obj['snippet']['thumbnails']['medium']['url'])
            video_dict[video_obj['contentDetails']['videoId']]=video_obj['snippet']['title'],video_obj['snippet']['thumbnails']['medium']['url']
        except:
            print(f"Ошибка добавления видео {video_obj['contentDetails']['videoId']}")
    return video_dict

def get_channel_id(url_channel:str):
    type_of_channel_name = url_channel.split('www.youtube.com')[1].split('/')[1]
    match type_of_channel_name:
        case 'channel':
            channel_id = url_channel.split('www.youtube.com')[1].split('/')[2]
            return channel_id
        case 'c':
            channel_name = url_channel.split('www.youtube.com')[1].split('/')[2]
            return get_json_search(channel_name)
        case 'user':
            channel_name = url_channel.split('www.youtube.com')[1].split('/')[2]
            return get_json_search(channel_name)

if __name__ == '__main__':
    url_channel = input()
    channel_id = get_channel_id(url_channel.replace('/featured',''))
    playlist_dict = get_json_playlists(channel_id)
    video_dict_for_playlist = {}
    for playlist_id in playlist_dict.keys():
        video_dict_for_playlist[playlist_id] = get_json_video(playlist_id)

    for playlist_id in video_dict_for_playlist.keys():
        playlist_dict_temp = video_dict_for_playlist[playlist_id]
        for video_id in playlist_dict_temp.keys():
            print(playlist_dict_temp[video_id][0]+f" https://www.youtube.com/watch?v={video_id}")

