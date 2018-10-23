#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of core.py.

Copyright Ian Vermes 2018
"""

from .basesuite import ExtendedTestCase
from validator import core

import unittest
import sys
import os

class DummyTestSuite(ExtendedTestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        truth = True
        self.assertTrue(truth)

    def test_relative_import_of_contextualised_of_module(self):
        module_directory = os.path.abspath(
            os.path.join(os.path.basename(__file__), ".."))
        path_list = sys.path.copy()

        self.assertIn(module_directory, path_list)

    def test_relative_import_of_module_successful(self):
        import_validator = core.contextual_import_tester

        self.assertTrue(import_validator())


class TestGlobals(ExtendedTestCase):

    def test_has_global_for_ini_path(self):
        self.assertHasAttr(obj=core, attrname="CORE_SETTINGS_FILENAME")

    def test_ini_path_is_to_a_file(self):
        path = core.CORE_SETTINGS_FILENAME

        self.assertTrue(os.path.isfile(path),
                        msg=f"path:{repr(path)} does not lead to a file.")

if __name__ == '__main__':
    unittest.main()
