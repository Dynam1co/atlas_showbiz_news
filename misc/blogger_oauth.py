"""Manage Blogger oauth."""
import requests
from conf import config_mgt as conf
import json

class BloggerToken():
    """Google oauth token class."""

    access_token = ''

    def __init__(self) -> None:
        """Constuctor."""
        self.grant_type = conf.getBloggerGrantType()
        self.client_id = conf.getBloggerClientId()
        self.client_secret = conf.getBloggerClientSecret()
        self.refresh_token = self.getCurrentRefreshToken()
        self.access_token = self.get_access_token()

    def getCurrentRefreshToken(self) -> str:
        """Connect to Postgre an get current refresh token."""
        json_object = self.getTokenData()
        return json_object['refresh']

    def get_access_token(self) -> str:
        """Compare latest token with new token and sets access token."""
        json_object = self.getTokenData()
        return json_object['access_token']


    def getTokenData(self) -> dict:
        """Get data informatio from tokens."""
        url = conf.getFastApiLatestTokenUrl()

        payload={}
        headers = {}

        try:    
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.exceptions.RequestException as e:
            return {}

        return json.loads(response.text)

    def do_refresh_token(self) -> str:
        """Refresh token with Google."""
        payload = {
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token
        }

        url = conf.getBlogerAuthUrl()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
        except requests.exceptions.RequestException as e:
            return {}

        json_object = json.loads(response.text)

        if response.status_code == 200:
            self.access_token = json_object['access_token']
            print(self.insert_access_token())
        else:
            return response.reason

    def insert_access_token(self):
        """Call fast api to insert new access token."""
        url = conf.getFastApiLatestTokenUrl()

        payload = {
            "access_token": self.access_token,
            "refresh": self.refresh_token
        }

        payload = json.dumps(payload)

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(response.text)