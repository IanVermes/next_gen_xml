#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of helper.argparse.py.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import CommandLineTestCase
from validator.helpers.argparse import NextGenArgParse

import unittest
import os


class CommandLineArgumentTest(CommandLineTestCase):

    def setUp(self):
        argparser = NextGenArgParse()
        self.parser = argparser._make_parser()

    def test(self):
        self.fail("TODO")


if __name__ == '__main__':
    unittest.main()
