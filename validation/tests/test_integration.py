#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of core.py.

Copyright Ian Vermes 2018
"""

from tests.basesuite import ExtendedTestCase
from validator import core

import unittest

class TestUserStories(ExtendedTestCase):

    def test_basic_user(self):

        # User invokes the script through the commandline with a directory
        self.fail('Not written')

        # User supplies directory

        # User is presented with on screen progress of operation

        # User is presented with a log file


class Test_CommandLine_Entry(TestUserStories):

    def test_user_default_args(self):

        # User invokes the script through the commandline with a directory
        self.fail('Not written')

    def test_user_no_dir_arg(self):

        # User invokes the script through the commandline WITHOUT a directory
        self.fail('Not written')
