#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the path convenience functions.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from helpers import path as under_consideration  # <- avoid confusion with os.path
import exceptions  # from validator import exceptions

from collections import namedtuple
import unittest
import os
import getpass

PathDetail = namedtuple("PathDetail", "name desc expandedname touched valid")

VERBOSITY = False

class TestExpandPath(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        username = getpass.getuser()
        dummyfilename = "unittest_dummyfile.txt"
        cls.files = []
        valid_dirs = {"~/Desktop" : "user directory",
                "": "empty string",
                f"/Users/{username}/Documents": "expanded user directory"}
        invalid_dirs = {
                "/Users/foobar": "invalid absolute directory",
                "./foobar": "invalid local directory"}

        # Make dummy file in real location for valid_dirs
        for dir, description in valid_dirs.items():
            name = os.path.join(dir, dummyfilename)
            expandedname = os.path.abspath(os.path.expanduser(name))
            with open(expandedname, "w") as f:
                f.write("touch")
            detail = PathDetail(name, description, expandedname,
                                valid=True,
                                touched=os.path.exists(expandedname))
            if VERBOSITY:
                print(f"{detail.expandedname}: {os.path.exists(detail.expandedname)}")
            cls.files.append(detail)

        # Just add dummy file paths for invalid_dirs
        for dir, description in invalid_dirs.items():
            name = os.path.join(dir, dummyfilename)
            expandedname = os.path.abspath(os.path.expanduser(name))
            detail = PathDetail(name, description, expandedname,
                                valid=False,
                                touched=os.path.exists(expandedname))
            cls.files.append(detail)

        # Validate touching
        naughty_files = []
        for detail in cls.files:
            if detail.valid == True and detail.touched == False:
                naughty_files.append(detail)

        if naughty_files:
            for detail in cls.files:
                if detail.touched:
                    os.remove(detail.expandedname)
                    if VERBOSITY:
                        print(f"{detail.expandedname}: {os.path.exists(detail.expandedname)} - there were naughtfiles!")
            msg = "The following files were not written: " + ", ".join([d.name for d in cls.files])
            raise AssertionError(msg)

    @classmethod
    def tearDownClass(cls):
        for detail in cls.files:
            if detail.touched:
                os.remove(detail.expandedname)
                if VERBOSITY:
                    print(f"{detail.expandedname}: {os.path.exists(detail.expandedname)}")

    def test_expand_path(self):
        for detail in self.files:
            filename = detail.name

            try:
                expandedname = under_consideration.expandpath(filename)
            except exceptions.NextGenError as err:
                continue # Forgive package else:exceptions as they're to handled.
            else:
                with self.subTest(filename=detail.name):
                    expected = detail.expandedname
                    msg = f"Did not expand '{filename}' into '{expected}'."
                    self.assertEqual(expandedname, expected, msg=msg)

    def expand_path_fails_on_false_positve_false_negative(self, criteria_attr, **kwargs):
        base_error = exceptions.NextGenError
        appropriate_errors = (exceptions.ParentDirNotFound, exceptions.FileNotFound)

        for detail in self.files:
            # True positives pass. True negatives except.
            # False positives are true negative that do not except.
            # False negatives are true positives that except.
            criterion = getattr(detail, criteria_attr)
            if criterion:
                # True positives do not assert.
                with self.subTest(false_positive=detail.name):
                    try:
                        under_consideration.expandpath(detail.name, **kwargs)
                    except appropriate_errors:
                        errmsg = f"Valid file '{detail.name}' raising package exception."
                    except base_error:
                        errmsg = f"Valid file '{detail.name}' raising base package exception."
                    except Exception as err:
                        errmsg = f"Something else went wrong: {repr(err)}."
                    else:
                        errmsg = ""

                    if errmsg:
                        self.fail(errmsg)

            elif not criterion and criterion is not None:
                # True negatives do not assert.
                with self.subTest(false_positive=detail.name):
                    with self.assertRaises(base_error) as expected:
                        under_consideration.expandpath(detail.name, **kwargs)
                    self.assertIsInstance(expected.exception, appropriate_errors)

    def test_expand_path_raises_exceptions_default(self):
        kwargs = {"criteria_attr": "valid"}
        self.expand_path_fails_on_false_positve_false_negative(**kwargs)

    def test_expand_path_raises_exceptions_check_file(self):
        kwargs = {"criteria_attr": "touched", "exists": True}
        self.expand_path_fails_on_false_positve_false_negative(**kwargs)

    def test_expand_path_raises_exceptions_check_dir(self):
        kwargs = {"criteria_attr": "valid", "exists": False, "dir_exists": True}
        self.expand_path_fails_on_false_positve_false_negative(**kwargs)

    def test_expand_path_raises_exceptions_do_not_validate_existence(self):
        kwargs = {"criteria_attr": "name", "exists": False, "dir_exists": False}


if __name__ == '__main__':
    unittest.main()
