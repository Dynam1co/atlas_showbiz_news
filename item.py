"""coding=utf-8."""

import datetime

class Item:
    """Item Object contains standard information for a Movie or TV Show."""

    def __init__(self, media_type, time_window) -> None:
        """
        Create object for Item class.

        Parameters:
        media_type (string): person, movie, tv
        time_window (string): day, week
        """        
        self.media_type = media_type
        self.time_window = time_window
        self.insert_date = datetime.datetime.now()
