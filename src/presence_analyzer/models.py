import os
import urllib
from pprint import pprint
from presence_analyzer.main import app
from presence_analyzer import settings


class User(object):
    """
    User model class
    """

    @staticmethod
    def fetch_users_file():
        """
        Fetches users.xml file specified in settings file
        """
        try:
            urllib.urlretrieve(
                settings.USERS_XML_SOURCE,
                settings.USERS_XML
            )
            return True
        except:
            return False
