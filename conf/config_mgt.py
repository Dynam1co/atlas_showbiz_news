"""Configuration management."""
from conf import config as cfg


def getConnectionString() -> str:
    """Return Postgre connection string."""
    return "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        cfg.POSTGRE_USER,
        cfg.POSTGRE_PASS,
        cfg.POSTGRE_HOST,
        cfg.POSTGRE_PORT,
        cfg.POSTGRE_DATABASE
    )

def getTmdbBaseUrl() -> str:
    """Return TMDB base API url."""
    return cfg.TMDB_BASE_URL

def getTmdbApiKey() -> str:
    """Return TMDB API key."""
    return cfg.TMDB_API_KEY

def getFastApiPostItemUrl() -> str:
    """Return post api url in fast api.""" 
    return cfg.FAST_API_BASE_URL + cfg.FAST_API_POST_ITEM_URL

def getTwitterData():
    """Return twitter api data."""
    return cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET, cfg.ACCESS_KEY, cfg.ACCESS_SECRET

def getBloggerGrantType() -> str:
    """Return grant type from config."""
    return cfg.BLOGGER_GRANT_TYPE

def getBloggerClientId() -> str:
    """Return client id from config."""
    return cfg.BLOGGER_CLIENT_ID

def getBloggerClientSecret() -> str:
    """Return client secret from config."""
    return cfg.BLOGGER_CLIENT_SECRET

def getBlogerAuthUrl() -> str:
    """Get google auth url."""
    return cfg.BLOGGER_AUTH_URL

def getBloggerBlogId() -> str:
    """Get google blog id."""
    return cfg.BLOGGER_BLOG_ID

def getBloggerPostEndpoint() -> str:
    """Return endpoint for post in Blogger."""
    return cfg.BLOGGER_API_URL + cfg.BLOGGER_BLOG_ID + cfg.BLOGGER_API_POST_URL

def getFastApiLatestTokenUrl() -> str:
    """Return token url."""
    return cfg.FAST_API_BASE_URL + cfg.FAST_API_GET_TOKEN_URL

def getFastApiBloggerPostUrl() -> str:
    """Return blogger post api url."""
    return cfg.FAST_API_BASE_URL + cfg.FAST_API_BLOGGER_POST_URL

def getFastApiBloggerItemUrl() -> str:
    """Return blogger item api url."""
    return cfg.FAST_API_BASE_URL + cfg.FAST_API_BLOGGER_ITEM_URL