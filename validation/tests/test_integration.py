#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of core.py.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase, CommandLineTestCase
from validator import core

import unittest
import os
import subprocess
import shlex


class TestUserStories(ExtendedTestCase):

    def test_basic_user(self):

        # User invokes the script through the commandline with a directory
        self.fail('Not written')

        # User supplies directory

        # User is presented with on screen progress of operation

        # User is presented with a log file


class Integration_CommandLine_Entry(CommandLineTestCase):

    @classmethod
    def setUpClass(self):
        super(Integration_CommandLine_Entry, self).setUpClass()
        self.entry_point_py = core.__file__
        assert os.path.isfile(self.entry_point_py)

        self.error_text = f"{os.path.basename(self.entry_point_py)}: error"

    def test_user_expected_arg(self):
        quote = shlex.quote
        cmd = "python {} {}".format(quote(self.entry_point_py),
                                    quote(self.dir_valid))

        # User invokes the script through the commandline with a directory
        status, stdout = subprocess.getstatusoutput(cmd)

        # Scipt processes user input exiting successfully.
        self.assertEqual(status, 0)
        self.assertNotIn(self.error_text, stdout.lower())
        self.assertIn("done!", stdout.lower())

    def test_user_no_arg(self):
        quote = shlex.quote
        self.entry_point_py
        cmd = "python {}".format(quote(self.entry_point_py))

        # User invokes the script through the commandline WITHOUT a directory
        status, stdout = subprocess.getstatusoutput(cmd)

        # User recieves an error, script exits.
        self.assertNotEqual(status, 0)
        self.assertIn(self.error_text, stdout.lower())

    def test_user_invalid_dir_arg(self):
        quote = shlex.quote
        cmd = "python {} {}".format(quote(self.entry_point_py),
                                    quote(self.dir_invalid))

        # User invokes the script through the commandline WITHOUT a directory
        status, stdout = subprocess.getstatusoutput(cmd)

        # User recieves an error, script exits.
        self.assertNotEqual(status, 0, msg=cmd)
        self.assertIn(self.error_text, stdout.lower())


if __name__ == '__main__':
    unittest.main()
