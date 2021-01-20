"""Download data from third party API."""
from json.decoder import JSONDecodeError
import requests
from sqlalchemy.sql.expression import label
import config_mgt as conf
import json
import uuid
from blogger_post import BlogPost

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

    if 'imdb_id' in data:
        result['imdb_id'] = data['imdb_id']    

    if item['media_type'] == 'movie':
        result['title'] = data['title']
    else:
        result['title'] = data['name']

    result['tmdb_id'] = item['id']
    result['id'] = str(uuid.uuid1())
    result['overview'] = data['overview']
    result['media_type'] = item['media_type']
    result['poster_path'] = item['poster_path']
    result['vote_average'] = item['vote_average']    
    result['time_window'] = item['time_window']

    json_object = json.dumps(result)

    try:  
        print(fast_api_post_item(json_object))
    except JSONDecodeError as e:
        print('Error in insert')

def get_stored_data(date, period, tw_published) -> dict:
    """Get filterded data from Fast API."""
    url = conf.getFastApiPostItemUrl()
    url += f'?date_insert={date}&period={period}&twitter_published={tw_published}'

    payload={}
    headers = {}

    try:    
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)

def get_item_data(date, period) -> dict:
    """Get filterded data from Fast API."""
    url = conf.getFastApiPostItemUrl()
    url += f'?date_insert={date}&period={period}'

    payload={}
    headers = {}

    try:    
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)

def update_twitter_published(id, value) -> dict:
    """Set published in Twitter."""
    url = conf.getFastApiPostItemUrl()
    url += f'{id}'

    payload = {
        "published_in_twitter": value,
    }

    payload = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    return json.loads(response.text)

def do_get(url) -> dict:
    """Do get method."""
    payload={}
    headers = {}

    try:    
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        return {}

    return json.loads(response.text)

def do_post(url, payload) -> dict:
    """Do post method."""
    payload = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except JSONDecodeError as e:
        print('Error in insert')
        return None

    return json.loads(response.text)

def do_patch(url, payload) -> dict:
    """Do patch method."""
    payload = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("PATCH", url, headers=headers, data=payload)
    except JSONDecodeError as e:
        print('Error in insert')
        return None

    return json.loads(response.text)

def get_item_published_in_blogger(tmdb_id) -> bool:
    """Return if item has published in Blogger."""
    jsonObject = do_get(conf.getFastApiBloggerItemUrl() + f'?tmdb_id={tmdb_id}')
    
    if len(jsonObject) == 0:
        return False

    return True
    
def create_blogger_item(item) -> dict:
    """Insert blog item into database."""
    url = conf.getFastApiBloggerItemUrl()
    labels = []

    if str(item['media_type']).lower() == 'movie':
        labels.append('Películas')
    else:
        labels.append('Series')

    payload = {
        "media_type": item['media_type'],
        "tmdb_id": item['tmdb_id'],
        "vote_average": item['vote_average'],
        "poster_path": item['poster_path'],
        "title": item['title'],
        "imdb_id": item['imdb_id'],
        "overview": item['overview'],
        "labels": str(labels)
    }

    return do_post(url, payload)

def create_blogger_post_item(blog_item) -> BlogPost:
    """Create blogger post using google api."""
    labels = []
    labels = list(blog_item['labels'].strip("]['").split(','))

    content = f'<h2>Puntuación: {blog_item["vote_average"]}</h2>'
    content += f'<h2>Sinopsis:</h2>{blog_item["overview"]}'

    my_post = BlogPost(
        title=blog_item['title'],
        content=content,
        labels=labels,
        image_url=f'https://www.themoviedb.org/t/p/original{blog_item["poster_path"]}'
    )

    jsonobject = my_post.create_blogger_post()

    if not 'id' in jsonobject:
        raise 'Error in create blog post.'

    my_post.id = jsonobject['id']
    my_post.published = jsonobject['published']
    my_post.updated = jsonobject['updated']
    my_post.url = jsonobject['url']

    my_post.store_post_into_database()

    return my_post

def update_blogger_post_item(my_post, id):
    """Update using fast api blog id a url."""
    url = conf.getFastApiBloggerItemUrl() + id

    payload = {
        "post_url": my_post.url,
        "blog_id": my_post.blog_id
    }

    return do_patch(url, payload)