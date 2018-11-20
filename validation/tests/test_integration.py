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
        self.unformatted_cmd = "python {} {}"

    def invoke_cmd_via_commandline(self, unformatted_cmd, expected_status):
        """Collects the stdout when invoking and validates the exit status."""
        quote = shlex.quote
        cmd = unformatted_cmd.format(quote(self.entry_point_py),
                                     quote(self.dir_valid))

        status, stdout = subprocess.getstatusoutput(cmd)

        if expected_status == 0:
            self.assertEqual(status, 0,
                             msg=f"'$ {cmd}': did not exit cleanly/validly.")
        elif 0 < expected_status < 3:
            self.assertGreater(status, 0,
                               msg=(f"'$ {cmd}': should have exited with an "
                                    "error but exited cleanly."))
        else:
            msg = (f"Got expected_status={repr(expected_status)}, "
                   "not int: 0 <= i < 3.")
            raise ValueError(msg)

        return stdout

    def test_user_expected_arg(self):
        # User invokes the script through the commandline with a directory
        cmd = self.unformatted_cmd

        # Script processes user input while printing to the CLI.
        status = 0
        stdout = self.invoke_cmd_via_commandline(cmd, expected_status=status)
        stdout = stdout.lower()

        # User reads CLI to confirm details.
        self.assertNotIn(self.error_text, stdout)
        self.assertNotIn("mode.test", stdout)
        self.assertIn("mode.live", stdout)
        self.assertIn("done!", stdout)

    def test_user_expected_arg_with_optional_arg(self):
        rawcmd = self.unformatted_cmd + " "
        options = ["-t", "--test"]
        cmds = {opt: rawcmd + opt for opt in options}

        # User invokes the script through the commandline with a
        # directory and optional argument
        status = 0
        for option, cmd in cmds.items():
            with self.subTest(optional_arg=option):
                args = cmd, status

                # Script processes user input while printing to the CLI.
                stdout = self.invoke_cmd_via_commandline(*args)
                stdout = stdout.lower()

                # User reads CLI to confirm details.
                self.assertNotIn(self.error_text, stdout)
                self.assertIn("done!", stdout)
                self.assertIn("mode.test", stdout)

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
        cmd = self.unformatted_cmd
        cmd = cmd.format(quote(self.entry_point_py),
                         quote(self.dir_invalid))

        # User invokes the script through the commandline WITHOUT a directory
        status, stdout = subprocess.getstatusoutput(cmd)

        # User recieves an error, script exits.
        self.assertNotEqual(status, 0, msg=cmd)
        self.assertIn(self.error_text, stdout.lower())


if __name__ == '__main__':
    unittest.main()
