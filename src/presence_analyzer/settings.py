"""
Presence analyzer settings.
"""
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
"""Application root path"""

APP_DATA = os.path.join(APP_ROOT, '..', '..', 'runtime', 'data')
"""Runtime aplication data path"""

USERS_XML = os.path.join(APP_DATA, 'users.xml')
"""Path to local copy of users XML file"""

USERS_XML_SOURCE = 'http://sargo.bolt.stxnext.pl/users.xml'
"""URL to Users XML file"""
