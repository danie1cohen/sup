"""
Tests for sup config module
"""
# pylint: disable=missing-docstring, import-error, wildcard-import
# pylint: disable=attribute-defined-outside-init,unused-wildcard-import, no-init
from __future__ import print_function
import os
import shutil

from nose.tools import *
import yaml

from sup import config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestSup(object):
    def setup(self):
        print('SETUP!')
        self.config_path = os.path.join(BASE_DIR, 'test_config.yml')
        self.archive_dir = os.path.join(BASE_DIR, 'test_archive_dir')

        self.config = {
            'archive_dir': self.archive_dir,
            'text_editor': 'vim',
            'print_cmd': 'cat',
        }
        if not os.path.exists(self.archive_dir):
            os.mkdir(self.archive_dir)

        self.delete_these = [
            self.config_path,
            self.archive_dir,
        ]


    def teardown(self):
        print('TEAR DOWN!')
        for filepath in self.delete_these:

            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
            elif os.path.exists(filepath):
                os.remove(filepath)


    def test_create_config(self):
        assert_false(os.path.exists(self.config_path))
        conf = config.create_config(self.config_path)
        ok_(os.path.exists(self.config_path))


    def test_read_config(self):
        assert_false(os.path.exists(self.config_path))
        conf = config.read_config(
            self.config_path,
            autocreate=True,
            **self.config
        )
        ok_(os.path.exists(self.config_path))
        eq_(conf['archive_dir'], self.archive_dir)
        eq_(conf['text_editor'], 'vim')
        eq_(conf['print_cmd'], 'cat')
