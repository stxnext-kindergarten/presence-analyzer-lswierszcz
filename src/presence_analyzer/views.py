# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from collections import defaultdict
from flask import abort, redirect, render_template, url_for
from presence_analyzer.main import app
from presence_analyzer.utils import (
    get_data,
    group_by_weekday,
    jsonify,
    mean,
    seconds_since_midnight as ssm
)

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect(url_for('presence_weekday'))


@app.route('/presence-weekday')
def presence_weekday():
    """
    Presence weekday view.
    """
    return render_template('presence_weekday.html')


@app.route('/presence-mean-time')
def presence_mean_time():
    """
    Presence mean time view.
    """
    return render_template('presence_mean_time.html')


@app.route('/presence-start-end')
def presence_start_end():
    """
    Presence start-end view.
    """
    return render_template('presence_start_end.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = get_data()
    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
        for i in data.keys()
    ]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_data(user_id):
    """
    Returns average start/end time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    sums = defaultdict(lambda: defaultdict(int))
    for date in data[user_id]:
        sums[date.weekday()]['items'] += 1
        sums[date.weekday()]['start'] += ssm(data[user_id][date]['start'])
        sums[date.weekday()]['end'] += ssm(data[user_id][date]['end'])

    return [
        [
            calendar.day_name[i][:3],
            sums[i]['start'] / sums[i]['items'],
            sums[i]['end'] / sums[i]['items']
        ]
        for i in xrange(5)
        if sums[i]['items'] > 0
    ]
