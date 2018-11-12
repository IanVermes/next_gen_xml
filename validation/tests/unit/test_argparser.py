#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of helper.argparse.py.

Copyright Ian Vermes 2018
"""

from tests.basesuite import ExtendedTestCase
from validator.helpers.argparse import NextGenArgParse

import unittest
import os

class CommandLineTestCase(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir_valid = os.path.expanduser("~/Desktop")
        cls.dir_invalid = os.path.expanduser("~/FooBar")
        assert os.path.isdir(cls.dir_valid)
        assert not os.path.isdir(cls.dir_invalid)


class CommandLineArgumentTest(CommandLineTestCase):

    def setUp(self):
        argparser = NextGenArgParse()
        self.parser = argparser._make_parser()

    def test(self):
        self.fail("TODO")
