"""Download data from third party API."""
import requests
import config_mgt as conf
import json
import uuid

def get_detail(id, type) -> dict:
    """Connect to third party API to download details of the item."""
    ws_name = f'{type}/{id}?language=es-ES'

    return get_tmdb_data(ws_name)

def get_trending(period, type) -> dict:
    """Connect to third party API to download data."""
    ws_name = f'trending/{type}/{period}'
    
    return get_tmdb_data(ws_name)

def get_tmdb_data(ws_name) -> dict:
    """Do GET to TMDB."""
    url = conf.getTmdbBaseUrl() + ws_name + f'?api_key={conf.getTmdbApiKey()}'

    if '?' in ws_name:
        url = conf.getTmdbBaseUrl() + ws_name + f'&api_key={conf.getTmdbApiKey()}'

    payload={}
    headers = {}

    try:    
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)

def fast_api_post_item(payload) -> dict:
    """Insert new item in postgres using fast api."""
    url = conf.getFastApiPostItemUrl()

    headers = {
    'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)

def fill_item_data_and_post(item):
    """Fill al fields of an item."""
    result = {}

    # Detail data of an intem
    data = get_detail(item['id'], item['media_type'])

    result['imdb_id'] = data['imdb_id']
    result['overview'] = data['overview']
    result['title'] = data['title']
    result['tmdb_id'] = item['id']
    result['id'] = str(uuid.uuid1())

    result['media_type'] = item['media_type']
    result['poster_path'] = item['poster_path']
    result['vote_average'] = item['vote_average']    
    result['time_window'] = item['time_window']

    json_object = json.dumps(result)
        
    print(fast_api_post_item(json_object))