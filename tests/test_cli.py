"""
Tests for sup cli module
"""
# pylint: disable=missing-docstring, import-error, wildcard-import
# pylint: disable=attribute-defined-outside-init,unused-wildcard-import, no-init
from __future__ import print_function
from datetime import datetime, timedelta
import os
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock.mock import patch, MagicMock

from nose.tools import *

from sup import cli


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestSup(object):
    def setup(self):
        print('SETUP!')


    def teardown(self):
        print('TEAR DOWN!')


    @patch('sup.cli.sup')
    def test_update_by_date(self, sup):
        args = {
            '--update': True,
            '--date': '2018-10-10',
        }
        cli.execute_args(args)
        target = datetime(2018, 10, 10), datetime.now().date()
        sup.create_update.assert_called_with(*target)


    @patch('sup.cli.sup')
    def test_update_by_last(self, sup):
        args = {'--update': True, '--last': True}
        prev_date = datetime(2018, 10, 10)
        today = datetime.now().date()
        sup.find_last_date.return_value = prev_date
        cli.execute_args(args)
        sup.create_update.assert_called_with(prev_date, today)


    @patch('sup.cli.sup')
    def test_update_by_default(self, sup):
        args = {'--update': True}
        cli.execute_args(args)
        today = datetime.now().date()
        prev_date = today - timedelta(days=1)
        sup.create_update.assert_called_with(prev_date, today)


    @patch('sup.cli.sup')
    def test_print_by_date(self, sup):
        args = {'--print': True, '--date': '2018-10-10'}
        cli.execute_args(args)
        sup.print_sup.assert_called_with(datetime(2018, 10, 10))


    @patch('sup.cli.sup')
    def test_print_by_default(self, sup):
        args = {'--print': True}
        cli.execute_args(args)
        sup.print_sup.assert_called_with(datetime.now().date())


    @patch('sup.cli.sup')
    def test_date(self, sup):
        args = {'--date': '2018-10-10'}
        cli.execute_args(args)
        sup.create_file.assert_called_with(datetime(2018, 10, 10))


    @patch('sup.cli.sup')
    def test_last(self, sup):
        args = {'--last': True}
        prev_date = datetime(2018, 10, 10)
        sup.find_last_date.return_value = prev_date
        cli.execute_args(args)
        sup.open_file.assert_called_with(prev_date)


    @patch('sup.cli.sup')
    def test_yesterday(self, sup):
        args = {'--yesterday': True}
        cli.execute_args(args)
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        sup.open_file.assert_called_with(yesterday)


    @patch('sup.cli.sup')
    def test_tomorrow(self, sup):
        args = {'--tomorrow': True}
        cli.execute_args(args)
        today = datetime.now().date()
        tomm = today + timedelta(days=1)
        sup.create_file.assert_called_with(tomm)
        sup.open_file.assert_called_with(tomm)


    @patch('sup.cli.sup')
    def test_new(self, sup):
        args = {'--new': True}
        sup.create_file.return_value = 'FOO'
        cli.execute_args(args)
        today = datetime.now().date()
        sup.create_file.assert_called_with(today, new=True)
        sup.open_file.assert_called_with(filepath='FOO')


    @patch('sup.cli.sup')
    def test_iteration(self, sup):
        args = {'--iteration': 7}
        sup.create_file.return_value = 'FOO'
        cli.execute_args(args)
        today = datetime.now().date()
        sup.create_file.assert_called_with(today, i=7)
        sup.open_file.assert_called_with(filepath='FOO')


    @patch('sup.cli.sup')
    def test_review(self, sup):
        args = {'--review': True}
        sup.create_review_file.return_value = 'FOO'
        cli.execute_args(args)
        today = datetime.now().date()
        sup.create_review_file.assert_called_with(today)
        sup.open_file.assert_called_with(filepath='FOO')


    def test_dir(self):
        args = {'--dir': True}
        cli.execute_args(args)
        ok_(True)


    @patch('sup.cli.sup')
    def test_default(self, sup):
        args = {}
        cli.execute_args(args)
        today = datetime.now().date()
        sup.create_file.assert_called_with(today)
        sup.open_file.assert_called_with(today)
