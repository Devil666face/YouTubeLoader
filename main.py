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


def get_json_search(channel_name,url_channel):
    try:
        request = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&type=channel&key={API_TOKEN}")
        data = request.json()
        channel_id = data['items'][0]['id']['channelId']
        return channel_id
    except:
        request = requests.get(url_channel)
        soup = BeautifulSoup(request.text, "lxml")
        channel_title_name = str(soup.title.string).replace(' - YouTube','')
        request = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_title_name}&type=channel&key={API_TOKEN}")
        print(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_title_name}&type=channel&key={API_TOKEN}")
        data = request.json()
        channel_id = data['items'][0]['id']['channelId']
        return channel_id


def get_json_channel():
    pass

# def get_icon(url,id):
#     request = requests.get(url)
#     print(request.content)
#     # with open(f"{id}.jpg",'wb') as image:
#     #     image.write(request.content)


def get_json_playlists(channel_id):
    request = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId={channel_id}&maxResults=50&key={API_TOKEN}")
    data = request.json()
    playlist_ids = data['items']
    playlist_dict = {}
    for playlist in playlist_ids:
        playlist_dict[playlist['id']] = str(playlist['snippet']['title']).replace('"',''), playlist['snippet']['thumbnails']['medium']['url']
        # get_icon(playlist['snippet']['thumbnails']['medium']['url'],playlist['id'])
    return playlist_dict


def get_json_video(playlist_id):
    request = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=400&playlistId={playlist_id}&key={API_TOKEN}")
    data = request.json()
    video_ids = data['items']
    video_dict = {}
    for video_obj in video_ids:
        try:
            video_dict[video_obj['contentDetails']['videoId']] = str(video_obj['snippet']['title']).replace('"',''), video_obj['snippet']['thumbnails']['medium']['url']
        except:
            print(f"Ошибка добавления видео {video_obj['contentDetails']['videoId']}")
    return video_dict


def get_video_dict_for_playlist(playlist_dict):
    video_dict_for_playlist = {}
    for playlist_id in playlist_dict.keys():
        video_dict_for_playlist[playlist_id] = get_json_video(playlist_id)
    return video_dict_for_playlist


def get_channel_id(url_channel: str):
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


if __name__ == '__main__':
    url_channel = sys.argv[1]
    if len(sys.argv)>2:
        exec_path_for_windows = sys.argv[2]
        db = Database(exec_path_for_windows + "/database.db")
    else:
        db = Database("database.db")

    # url_channel = input()
    channel_id = get_channel_id(url_channel.replace('/featured', ''))
    playlist_dict = get_json_playlists(channel_id)
    video_dict_for_playlist = get_video_dict_for_playlist(playlist_dict)
    db.save_all(video_dict_for_playlist, playlist_dict)
    del db
