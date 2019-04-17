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
import glob
import os

from contextlib import redirect_stderr


class CommandLineArgumentTest(CommandLineTestCase):

    def setUp(self):
        argparser = NextGenArgParse()
        self.parser = argparser._make_parser()
        self.stderr_bypass = io.StringIO()

    def tearDown(self):
        self.stderr_bypass.close()

    def test_parse_valid_path(self):
        files = {"file": self.file_valid, "dir": self.dir_valid}
        for path_type, path in files.items():
            with self.subTest(path_type=path_type):
                self.assertTrue(os.path.exists(path), msg="Precondition!")

                cmd = "{}".format(shlex.quote(path))
                cmd = shlex.split(cmd)

                args = self.parser.parse_args(cmd)

                # Test 1: only one item in args.xmls
                self.assertEqual(len(args.xmls), 1)

                # Test 2: the single args.xmls item == self.file_valid
                item = args.xmls[0]
                self.assertEqual(str(item), path)

    def test_parse_nonexistant_paths(self):
        files = {"file": self.file_invalid, "dir": self.dir_invalid}

        exit_code = 2
        substring_1 = "error"
        substring_2 = "does not exist"

        for path_type, path in files.items():
            with self.subTest(path_type=path_type):
                self.assertFalse(os.path.exists(path), msg="Precondition!")

                cmd = "{}".format(shlex.quote(path))
                cmd = shlex.split(cmd)

                with redirect_stderr(self.stderr_bypass):
                    with self.assertRaises(SystemExit) as context:
                        self.parser.parse_args(cmd)

                stderr_output = self.stderr_bypass.getvalue().lower()
                self.assertEqual(context.exception.code, exit_code)
                self.assertIn(substring_1, stderr_output)
                self.assertIn(substring_2, stderr_output)

    def test_parse_multiple_valid_dir(self):
        self.fail("test not written")

    def test_parse_multiple_valid_file(self):
        self.fail("test not written")

    def test_parse_multiple_valid_files_dirs_mixed(self):
        """Mixed positional args."""
        self.fail("test not written")

    def test_parser_output_is_list_of_pathlibPaths(self):
        self.fail("test not written")

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

    @unittest.expectedFailure
    def test_parse_valid_file_rather_than_dir(self):
        cmd = "{}".format(shlex.quote(self.file_valid))
        cmd = shlex.split(cmd)
        exit_code = 2
        substring_1 = "error"
        substring_2 = "Expected a directory not file"

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
        substring_2 = "the following arguments are required: PATHS"

        with redirect_stderr(self.stderr_bypass):  # Supress printing
            with self.assertRaises(SystemExit) as context:
                self.parser.parse_args(cmd)
            stderr_output = self.stderr_bypass.getvalue()

        self.assertEqual(context.exception.code, exit_code)
        self.assertIn(substring_1, stderr_output)
        self.assertIn(substring_2, stderr_output)

    def test_parse_optional_argument_TEST_present(self):
        cmd = "{}".format(shlex.quote(self.dir_valid))
        cmd += " --test"
        cmd = shlex.split(cmd)

        args = self.parser.parse_args(cmd)
        self.assertIsInstance(args.testmode, bool)
        self.assertTrue(args.testmode)

    def test_parse_optional_argument_TEST_absent(self):
        cmd = "{}".format(shlex.quote(self.dir_valid))
        cmd += ""
        cmd = shlex.split(cmd)

        args = self.parser.parse_args(cmd)
        self.assertIsInstance(args.testmode, bool)
        self.assertFalse(args.testmode)

if __name__ == '__main__':
    unittest.main()
