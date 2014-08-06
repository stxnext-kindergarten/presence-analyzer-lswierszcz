# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import os.path
import json
import datetime
import unittest

from flask import url_for

from presence_analyzer import main, utils
from presence_analyzer import views  # pylint: disable=unused-import

TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)

TEST_DATA_WRONG_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime',
    'data', 'test_data_wrong.csv'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

        # Create context for request object.
        # This is reqired if url_for function is used.
        self.ctx = main.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        self.ctx.pop()

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith(url_for('presence_weekday'))

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})

    def test_mean_time_weekday(self):
        """
        Test mean time view for user that exists in test data.
        """
        resp = self.client.get('/api/v1/mean_time_weekday/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)

        self.assertEqual(len(data), 7)

    def test_mean_time_weekday_wrong(self):
        """
        Test mean time view for user that doesn't exists in test data.
        """
        resp = self.client.get('/api/v1/mean_time_weekday/john')
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get('/api/v1/mean_time_weekday/0')
        self.assertEqual(resp.status_code, 404)

    def test_presence_weekday(self):
        """
        Test presence weekday view for user that exists in test data.
        """
        resp = self.client.get('/api/v1/presence_weekday/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 8)

    def test_presence_weekday_wrong(self):
        """
        Test presence weekday view for user that doesn't exists in test data.
        """
        resp = self.client.get('/api/v1/presence_weekday/0')
        self.assertEqual(resp.status_code, 404)

    def test_presence_start_end(self):
        """
        Test presence start-end view
        """
        resp = self.client.get('/api/v1/presence_start_end/0')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/api/v1/presence_start_end/10')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertNotEqual(len(data), 0)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )

    def test_get_data_wrong(self):
        """
        Test parsing of CSV file with wrong data.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_WRONG_CSV})
        data = utils.get_data()
        self.assertIsNotNone(data)


class PresenceAnalyzerMenuTestCase(unittest.TestCase):
    """
    Menu extension tests.
    """
    def setUp(self):
        """
        Before each test, set up a environment.
        """
        self.client = main.app.test_client()

        # Create context for request object.
        # This is reqired if url_for function is used.
        self.ctx = main.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        self.ctx.pop()

    def test_active_element(self):
        """
        Test active element in menu
        """
        for view_name in [
                'presence_weekday',
                'presence_mean_time',
                'presence_start_end'
        ]:
            current_url = url_for(view_name)
            resp = self.client.get(current_url)
            self.assertEqual(resp.status_code, 200)

            # Change context for current url
            with main.app.test_request_context(current_url):
                menu = main.app.extensions['menu'].menu()

                for item in menu.entries:
                    if current_url == item.url:
                        self.assertTrue(item.is_active())


def suite():
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerMenuTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
