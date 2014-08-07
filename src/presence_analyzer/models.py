from lxml import etree
import os
import requests

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
        r = requests.get(settings.USERS_XML_SOURCE)
        if r.ok:
            with open(settings.USERS_XML, 'w') as users_file:
                users_file.write(r.content)
            return True

        return False
