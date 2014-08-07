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

    @staticmethod
    def get_data():
        """
        Gets users data from XML.
        """
        users = []

        if (
            not os.path.isfile(settings.USERS_XML) and
            not User.fetch_users_file()
        ):
            return users

        with open(settings.USERS_XML, 'r') as xml_file:
            xml = etree.parse(xml_file)
            root = xml.getroot()

            server = root.find('server')
            server_url = '{0}://{1}'.format(
                server.find('protocol').text,
                server.find('host').text,
            )

            for user in root.find('users'):
                users.append({
                    'user_id': user.get('id'),
                    'name': user.find('name').text,
                    'image_url': '{0}{1}'.format(
                        server_url,
                        user.find('avatar').text
                    ),
                })

        return users
