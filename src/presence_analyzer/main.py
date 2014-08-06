# -*- coding: utf-8 -*-
"""
Flask app initialization.
"""
from flask import Flask
from menu import Menu

app = Flask(__name__)  # pylint: disable=invalid-name

# Add menu extension into Flask
menu = app.extensions['menu'] = Menu(app=app)

menu.add_entry(name='Presence by weekday', url='/presence-weekday')
menu.add_entry(name='Presence mean time ', url='/presence-mean-time')
menu.add_entry(name='Presence start-end', url='/presence-start-end')
