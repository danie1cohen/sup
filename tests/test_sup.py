"""
Tests for sup.sup module
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

from sup import sup


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestSup(object):
    def setup(self):
        print('SETUP!')


    def teardown(self):
        print('TEAR DOWN!')

    def test_print_yaml(self):
        obj = {'foo': 'bar'}
        eq_(sup.print_yaml(obj), ['foo: bar', '\n\n\n\n', ''])


    @nottest
    def test_get_fileloc(self):
        date = datetime.now().date()
        eq_(sup.get_fileloc(date), False)

    @nottest
    @patch('sup.sup.os')
    def test_open_file(self):
        date = datetime.now().date()
        sup.open_file(date)
