from typing import Dict
from os import environ


class Message(object):
    """Message class."""

    def __init__(self, body = {}):
        """Initialize Message."""
        self.body = body
        self.env = environ
        self.context = {}
