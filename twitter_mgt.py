"""Twitter management."""

import tweepy
import config_mgt as conf
import requests
import os

CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET = conf.getTwitterData()

def download_image(image_url):
    """Download image."""
    request = requests.get(image_url, stream=True)
    filename = 'temp.jpg'

    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        return filename
    else:
        print("Unable to download image")

def post_tweet(item):
    """Publish tweet and delete image from disk."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    filename = download_image("https://www.themoviedb.org/t/p/original" + item['poster_path'])

    # Tweet image and text
    x = tweepy.API(auth)
    x.update_with_media(filename, get_tweet_text(item))

    os.remove(filename)

def get_tweet_text(item) -> str:
    """Generate tweet text."""
    text = 'Tendencias de '

    if item['time_window'] == 'day':
        text += 'hoy en '
    elif item['time_window'] == 'week':
        text += 'la semana en '

    if item['media_type'] == 'movie':
        text += 'cine:'
    else:
        text += 'televisión:'

    text += '\n\n'

    text += item['title']

    text += '\n'

    text += f"Valoración: {item['vote_average']}"

    return text
