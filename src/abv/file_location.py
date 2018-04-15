#pylint: disable=too-few-public-methods
"""This class enables the location for the fetched files to be abstracted."""

class FileLocation:

    def __init__(self):
        self.current_location = "/beer_data"

    def get_file_location(self):
        return self.current_location
