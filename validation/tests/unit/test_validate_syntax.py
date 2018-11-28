#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase
from helpers.xml import validate_syntax, ValidationResult
import exceptions

from lxml import etree

import os
import unittest
import functools


class TestSyntaxValidation(XMLValidationTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_exc = exceptions.SyntaxValidationError
        cls.valid_file = next(cls.get_resources_by_criterion("valid"))
        cls.illegal_file = next(cls.get_resources_by_criterion("syntax"))
        cls.result_type = ValidationResult

    def _validator(self, *args, _func):
        """Basis for partialmethod"""
        return _func(*args)

    validator = functools.partialmethod(_validator, _func=validate_syntax)

    def test_validation_passes_with_valid_file(self):
        filename = self.valid_file

        result = self.validator(filename)

        self.assertTrue(result)

    def test_validation_fails_with_illegal_file(self):
        filename = self.illegal_file

        result = self.validator(filename)

        self.assertFalse(result)

    def test_failed_validation_result_has_correct_exception(self):
        filename = self.illegal_file
        expected_pkg_exc = self.base_exc
        expected_cause_exc = etree.XMLSyntaxError

        result = self.validator(filename)

        with self.assertRaises(expected_pkg_exc):
            raise result.exception
        with self.assertRaises(expected_cause_exc):
            raise result.exception.__cause__

    def test_validation_returns_result_obj(self):
        filename = self.illegal_file

        result = self.validator(filename)

        self.assertIsInstance(result, self.result_type)

    def test_nofalses_after_syntax_validation(self):

        kwargs = {"values": self.files,
                  "criterion": "syntax",
                  "validator": self.validator,
                  "permitted_exceptions": self.base_exc,
                  "propogate": False}
        self.assertNoFalsePositivesOrNegatives(**kwargs)

    def test_other_illegal_files_pass(self):
        """Similar to test_nofalses_after_syntax_validation but explict."""
        for filename, properties in self.files.items():
            is_illegal = getattr(properties, self.invalid_attr)
            has_syntax_err = getattr(properties, "syntax")

            if is_illegal and not has_syntax_err:
                with self.subTest(name=os.path.basename(filename)):
                    result = self.validator(filename)

                    self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
