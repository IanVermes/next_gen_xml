#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of helper.argparse.py.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import CommandLineTestCase
from validator.helpers.argparser import NextGenArgParse

import io
import argparse
import unittest
import shlex
import os
import glob
import pathlib

from contextlib import redirect_stderr


class CommandLineClassMethods(CommandLineTestCase):

    def test_method_searchdirectories_finds_xmls(self):
        method = NextGenArgParse.searchdirectory
        path = self.dir_valid
        expected = glob.glob(os.path.join(path, "*.xml"))

        result = method(path)

        # Test1: returns a list
        self.assertIsInstance(result, list)

        # Test2: each list item is a pathlib.Path file with suffix .xml
        self.assertGreater(len(result), 0, msg="Precondition!")
        for item in result:
            self.assertIsInstance(item, pathlib.Path)
            self.assertTrue(item.is_file())
            self.assertEqual(item.suffix.lower(), ".xml")

        # Test3: list has same number of items as a glob.glob search for xml
        self.assertEqual(len(expected), len(result))
        self.assertListEqual(list(map(str, result)), expected)


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

    def test_parse_multiple_args(self):
        cmd_template = "{a} {b}"
        params = {"multiple dirs": [self.dir_valid, self.dir_valid],
                  "multiple files": [self.file_valid, self.file_valid],
                  "multiple mixed": [self.file_valid, self.dir_valid],
        }
        for condition, paths in params.items():
            path1, path2, *_ = paths
            with self.subTest(condition=condition):
                cmd = cmd_template.format(a=shlex.quote(path1),
                                          b=shlex.quote(path2))
                cmd = shlex.split(cmd)

                args = self.parser.parse_args(cmd)

                # Test 1: only one item in args.xmls
                self.assertEqual(len(args.xmls), len(paths))

                # Test 2: the single args.xmls item == self.file_valid
                args = list(map(str, args.xmls))
                self.assertListEqual(args, paths)

    def test_parser_output_is_list_of_pathlibPaths(self):
        path = self.file_valid
        self.assertTrue(os.path.exists(path), msg="Precondition!")

        cmd = "{}".format(shlex.quote(path))
        cmd = shlex.split(cmd)

        args = self.parser.parse_args(cmd)

        # Test1: args.xmls is a list
        self.assertIsInstance(args.xmls, list)

        # Test2: each item is a pathlib.PATHS
        for item in args.xmls:
            self.assertIsInstance(item, pathlib.Path)

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
