"""Download data from third party API."""
import requests
import config_mgt as conf
import json

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

def fill_item_data(item):
    """Fill al fields of an item."""
    # item['media_type']
    # item['poster_path']
    # item['vote_average']
    # item['id']
    # item['time_window']

    # Detail data of an intem
    data = get_detail(item['id'], item['media_type'])

    data['imdb_id']
    data['overview']
    data['title']