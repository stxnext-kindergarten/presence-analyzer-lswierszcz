"""
Flask menu extension
"""

from flask import current_app, request
from werkzeug.local import LocalProxy

__all__ = ['MAIN_MENU', ]


class MenuEntry(object):
    """
    Menu entry class for main menu
    """
    def __init__(self, name, url):
        """
        Assign attributes for menu entry
        """
        self.name = name
        self.url = url

    def is_active(self):
        """
        Returns True if current item have same url as request path
        """
        return request.path == self.url


class Menu(object):
    """
    Main menu class
    """
    entries = []

    def __init__(self, app=None):
        """
        Setup app for menu
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Adds menu to context
        """
        app.context_processor(lambda: dict(
            main_menu=self.entries))

    def add_entry(self, name, url):
        """
        Adds menu entry
        """
        self.entries.append(MenuEntry(name=name, url=url))

    @staticmethod
    def menu():
        """
        Returns menu for current application instance
        """
        return current_app.extensions['menu']


MAIN_MENU = LocalProxy(Menu.menu)
