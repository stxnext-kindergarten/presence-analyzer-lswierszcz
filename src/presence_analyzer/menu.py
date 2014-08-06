from flask import request
from werkzeug.local import LocalProxy

__all__ = ['main_menu', ]


class MenuEntry:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.is_active = lambda: request.path == self.url


class Menu:
    entries = []

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.context_processor(lambda: dict(
            main_menu=self.entries))

    def add_entry(self, name, url):
        self.entries.append(MenuEntry(name=name, url=url))

    @staticmethod
    def menu():
        return current_app.extensions['menu']


main_menu = LocalProxy(Menu.menu)
