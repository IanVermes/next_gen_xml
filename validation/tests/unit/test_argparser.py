#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of helper.argparse.py.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import CommandLineTestCase
from validator.helpers.argparse import NextGenArgParse

import io
import argparse
import unittest
import shlex

from contextlib import redirect_stderr


class CommandLineArgumentTest(CommandLineTestCase):

    def setUp(self):
        argparser = NextGenArgParse()
        self.parser = argparser._make_parser()
        self.stderr_bypass = io.StringIO()

    def tearDown(self):
        self.stderr_bypass.close()


    def test_parse_valid_dir(self):
        cmd = "{}".format(shlex.quote(self.dir_valid))
        cmd = shlex.split(cmd)

        args = self.parser.parse_args(cmd)

        self.assertEqual(args.directory, self.dir_valid)

    def test_parse_invalid_dir(self):
        cmd = "{}".format(shlex.quote(self.dir_invalid))
        cmd = shlex.split(cmd)
        exit_code = 2
        substring_1 = "error"
        substring_2 = "does not exist"

        with redirect_stderr(self.stderr_bypass):
            with self.assertRaises(SystemExit) as context:
                self.parser.parse_args(cmd)
            stderr_output = self.stderr_bypass.getvalue()

        self.assertEqual(context.exception.code, exit_code)
        self.assertIn(substring_1, stderr_output)
        self.assertIn(substring_2, stderr_output)

    def test_parse_no_argument(self):
        cmd = ""
        cmd = shlex.split(cmd)
        exit_code = 2
        substring_1 = "error"
        substring_2 = "the following arguments are required: DIR"

        with redirect_stderr(self.stderr_bypass):  # Supress printing
            with self.assertRaises(SystemExit) as context:
                self.parser.parse_args(cmd)
            stderr_output = self.stderr_bypass.getvalue()

        self.assertEqual(context.exception.code, exit_code)
        self.assertIn(substring_1, stderr_output)
        self.assertIn(substring_2, stderr_output)


if __name__ == '__main__':
    unittest.main()
