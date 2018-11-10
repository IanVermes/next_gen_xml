#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of core.py.

Copyright Ian Vermes 2018
"""

from tests.basesuite import ExtendedTestCase
from validator import core

import unittest
import os


class TestPrimitive(ExtendedTestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        truth = True
        self.assertTrue(truth)

    def test_import_of_module(self):
        primitive = core._TestingPrimitive()

        flag = primitive.verify_import_tester()

        self.assertTrue(flag)

    def test_raising_root_exceptions(self):
        import validator
        root_exception = validator.exceptions.NextGenError
        primitive = core._TestingPrimitive()

        with self.assertRaises(root_exception):
            primitive.raise_package_error()

class TestGlobals(ExtendedTestCase):

    def test_has_global_for_ini_path(self):
        self.assertHasAttr(obj=core, attrname="CORE_SETTINGS_FILENAME")

    def test_ini_path_is_to_a_file(self):
        path = core.CORE_SETTINGS_FILENAME

        self.assertTrue(os.path.isfile(path),
                        msg=f"path:{repr(path)} does not lead to a file.")


if __name__ == '__main__':
    unittest.main()
