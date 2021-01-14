"""Configuration management."""

import config as cfg


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