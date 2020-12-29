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