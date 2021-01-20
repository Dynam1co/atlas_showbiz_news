"""Blogger post entity."""
import requests
from sqlalchemy.sql.expression import label
import config_mgt as conf
import json
import blogger_oauth as ba
import datetime

class BlogPost():
    """Blogger post."""

    published = None
    updated = None
    url = ""
    id = ""

    def __init__(self, title, content, labels, image_url) -> None:
        """Init instance."""
        self.blog_id = conf.getBloggerBlogId()
        self.title = title
        self.labels = labels
        self.image_url = image_url
        self.content = f"<img src='{self.image_url}'><br>{content}"

    def create_blogger_post(self, curr_token=None):
        """Create blogger post via API rest."""
        if not curr_token:
            my_token = ba.BloggerToken()
        else:
            my_token = curr_token

        url = conf.getBloggerPostEndpoint()

        payload = {
            "kind": "blogger#post",
            "title": self.title,
            "content": self.content,
            "labels": self.labels
        }

        payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {my_token.access_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        json_object = json.loads(response.text)

        if 'error' in json_object:
            if 'status' in json_object['error']:
                if json_object['error']['status'] == 'UNAUTHENTICATED':
                    my_token.do_refresh_token()
                    return self.create_blogger_post(my_token)

        return json_object

    def store_post_into_database(self):
        """Insert post data into fast api database."""
        url = conf.getFastApiBloggerPostUrl()

        payload = {
            "id": self.id,
            "published_datetime": self.published,
            "updated_datetime": self.updated,
            "post_url": self.url,
            "blog_id": self.blog_id,
            "title": self.title,
            "content": self.content,
            "image_url": self.image_url,
            "labels": str(self.labels)
        }

        payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text)
        

if __name__ == "__main__":
    labels = ['amime', 'manga']

    pos = BlogPost(
        title='Título',
        content='Esto es el contenido',
        labels=labels,
        image_url='https://www.themoviedb.org/t/p/w600_and_h900_bestv2/mzQf0QAs4jz0fDMrzFlZxQvC9KT.jpg'
    )

    jsonobject = pos.create_blogger_post()

    if not 'id' in jsonobject:
        raise 'Error in create blog post.'

    pos.id = jsonobject['id']
    pos.published = jsonobject['published']
    pos.updated = jsonobject['updated']
    pos.url = jsonobject['url']

    pos.store_post_into_database()