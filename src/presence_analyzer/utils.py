# -*- coding: utf-8 -*-
"""
Helper functions used in views.
"""

import csv
from json import dumps
from functools import wraps
from datetime import datetime
from threading import Lock

from flask import Response

from presence_analyzer.main import app
from presence_analyzer.models import User

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def cache(timeout=600):
    """
    Decorator for caching function output
    """
    cache = dict()
    lock = Lock()

    def decorator(function):
        """
        Function that is used for parametrized decorator
        """
        @wraps(function)
        def wrapper(*args, **kwargs):
            """
            This docstring will be overridden by @wraps decorator.
            """
            key = '{0}{1}{2}'.format(
                function.__repr__(),
                args.__repr__(),
                kwargs.__repr__(),
            )

            if (
                    key in cache and
                    timeout > (datetime.now() - cache[key]['created']).seconds
            ):
                return cache[key]['data']

            with lock:
                result = function(*args, **kwargs)
                cache[key] = {
                    'data': result,
                    'created': datetime.now()
                }
            return result
        return wrapper
    return decorator


def jsonify(function):
    """
    Creates a response with the JSON representation of wrapped function result.
    """
    @wraps(function)
    def inner(*args, **kwargs):
        """
        This docstring will be overridden by @wraps decorator.
        """
        return Response(
            dumps(function(*args, **kwargs)),
            mimetype='application/json'
        )
    return inner


@cache()
def get_data():
    """
    Extracts presence data from CSV file and groups it by user_id.

    It creates structure like this:
    data = {
        'user_id': {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }
    }
    """
    data = {}
    with open(app.config['DATA_CSV'], 'r') as csvfile:
        presence_reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(presence_reader):
            if len(row) != 4:
                # ignore header and footer lines
                continue

            try:
                user_id = int(row[0])
                date = datetime.strptime(row[1], '%Y-%m-%d').date()
                start = datetime.strptime(row[2], '%H:%M:%S').time()
                end = datetime.strptime(row[3], '%H:%M:%S').time()
            except (ValueError, TypeError):
                log.debug('Problem with line %d: ', i, exc_info=True)

            data.setdefault(user_id, {})[date] = {'start': start, 'end': end}

    return data


def group_by_weekday(items):
    """
    Groups presence entries by weekday.
    """
    result = [[], [], [], [], [], [], []]  # one list for every day in week
    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()].append(interval(start, end))
    return result


def seconds_since_midnight(time):
    """
    Calculates amount of seconds since midnight.
    """
    return time.hour * 3600 + time.minute * 60 + time.second


def interval(start, end):
    """
    Calculates inverval in seconds between two datetime.time objects.
    """
    return seconds_since_midnight(end) - seconds_since_midnight(start)


def mean(items):
    """
    Calculates arithmetic mean. Returns zero for empty lists.
    """
    return float(sum(items)) / len(items) if len(items) > 0 else 0


def fetch_users_file():
    """
    Fetches users XML file from external server
    """
    return User.fetch_users_file()
