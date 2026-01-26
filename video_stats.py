import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL = 'MrBeast'


def get_play_list_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL}&key={API_KEY}'

        response = requests.get(url)
        data = response.json()
        playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        # print(playlist_id)
        return playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == '__main__':
    get_play_list_id()