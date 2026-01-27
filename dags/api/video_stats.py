import requests
import json
from datetime import date
from airflow.decorators import task
from airflow.models import Variable


API_KEY = Variable.get("API_KEY")
CHANNEL = Variable.get("CHANNEL_HANDLE")
MAX_RESULT=50

@task
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
@task
def get_videos_id(playlist_id):
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULT}&playlistId={playlist_id}&key={API_KEY}"
    videos_id = []
    pageToken = None

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                videos_id.append(video_id)
            
            pageToken = data.get('nextPageToken')
            # print(pageToken)
            if not pageToken:
                break
        return videos_id
    except requests.exceptions.RequestException as e:
        raise e
@task
def extracted_data(video_list_id):
    extracted_data = []

    def batch_list(video_list_id,batch_size):
        for video_id in range(0,len(video_list_id),batch_size):
            yield video_list_id[video_id: video_id+batch_size]
    try:
        for batch in batch_list(video_list_id,MAX_RESULT):
            videos_id_str = ','.join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=statistics&part=snippet&id={videos_id_str}&key={API_KEY}"

            response = requests.get(url)

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                stats = item['statistics']

                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    'viewCount': stats.get('viewCount',None),
                    'likeCount': stats.get('likeCount',None),
                    'commentCount': stats.get('commentCount',None)
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e
@task        
def save_to_json(data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path,"w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
if __name__ == '__main__':
    playlist_id = get_play_list_id()
    video_list_id = get_videos_id(playlist_id)
    final_data = extracted_data(video_list_id)
    save_to_json(final_data)