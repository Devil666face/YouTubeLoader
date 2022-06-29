import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def exec_and_save(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as ex:
            print(f'Ошибка выполения запроса\n{query}\n{ex}')

    def create_playlist_table(self):
        create_query = f'CREATE TABLE "playlists" ("playlist_id" TEXT NOT NULL UNIQUE, "title" TEXT NOT NULL, "image" TEXT NOT NULL, PRIMARY KEY("playlist_id"));'
        self.exec_and_save(create_query)

    def create_video_table(self, playlis_id):
        create_query = f'CREATE TABLE "{playlis_id}" ("video_id" TEXT NOT NULL UNIQUE, "title" TEXT NOT NULL, "image" TEXT NOT NULL, PRIMARY KEY("video_id"));'
        self.exec_and_save(create_query)

    def insert_video_data_for_playlist(self, playlist_id, playlist_dict):
        for video_id in playlist_dict.keys():
            insert_query = f'INSERT INTO "{playlist_id}" VALUES ("https://www.youtube.com/watch?v={video_id}","{playlist_dict[video_id][0]}","{playlist_dict[video_id][1]}");'
            self.exec_and_save(insert_query)

    def insert_playlist_data(self, playlist_dict):
        for playlist_id in playlist_dict.keys():
            insert_query = f'INSERT INTO "playlists" VALUES ("{playlist_id}","{playlist_dict[playlist_id][0]}","{playlist_dict[playlist_id][1]}");'
            self.exec_and_save(insert_query)

    def save_all(self, video_dict_for_playlist, playlist_dict):
        self.delete_all_tables()
        self.create_playlist_table()
        self.insert_playlist_data(playlist_dict)
        for playlist_id in video_dict_for_playlist.keys():
            self.create_video_table(playlist_id)
            playlist_dict_temp = video_dict_for_playlist[playlist_id]
            self.insert_video_data_for_playlist(playlist_id,playlist_dict_temp)

    def delete_all_tables(self):
        select_query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.exec_and_save(select_query)
        table_name_list = []
        for query in self.cursor:
            table_name_list.append(query[0])
            print(table_name_list[len(table_name_list)-1])
        for table_name in table_name_list:
            delete_query = f'DROP TABLE "{table_name}";'
            self.exec_and_save(delete_query)





