"""Download data from third party API."""
import requests
import config_mgt as conf
import json

def get_trending(period, type):
    """Connect to third party API to download data."""
    ws_name = f'trending/{type}/{period}'
    
    return get_tmdb_data(ws_name)

def get_tmdb_data(ws_name) -> dict:
    """Do GET to TMDB."""
    url = conf.getTmdbBaseUrl() + ws_name + f'?api_key={conf.getTmdbApiKey()}'

    payload={}
    headers = {}

    try:    
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)