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