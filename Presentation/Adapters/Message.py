from os import environ


class Message(object):
    """Message class."""

    def __init__(self, content={}):
        """Initialize Message."""
        self.content = content
        self.env = environ
        self.context = {}
