# -*- coding: utf-8 -*-
"""
Flask app initialization.
"""


from flask import Flask
from presence_analyzer.menu import Menu


app = Flask(__name__)  # pylint: disable=invalid-name


# Add menu extension into Flask
MAIN_MENU = Menu(app=app)


app.extensions['menu'] = MAIN_MENU


MAIN_MENU.add_entry(name='Presence by weekday', url='/presence-weekday')
MAIN_MENU.add_entry(name='Presence mean time ', url='/presence-mean-time')
MAIN_MENU.add_entry(name='Presence start-end', url='/presence-start-end')
