#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of validator.py.

Copyright Ian Vermes 2018
"""

from validator import core

import unittest
import sys
import os


class DummyTestSuite(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
