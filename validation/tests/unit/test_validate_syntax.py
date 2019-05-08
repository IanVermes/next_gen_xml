#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""
from tests.base_testcases import ExtendedTestCase
from tests.validation_testcases import ValidationTestCase
from helpers.checksyntax import validate_syntax, raise_if_mismatched_encodings
from helpers.enum import Passing
from helpers.result import ValidationResult
import exceptions

from lxml import etree

import unittest


class TestValidateSyntaxFunction(ValidationTestCase, ExtendedTestCase):
    """Some test methods are written in the first parent class
    """

    @classmethod
    def setUpClass(cls):
        resource = "tests/resources/syntax"
        func = validate_syntax
        failing_enum = Passing.SYNTAX

        cls.preSetup(directory=resource, validator=func, enum=failing_enum)
        cls.resource_dict = cls.get_resources()

    def test_encoding_mismatch_func(self):
        """The encoding mismatch function is used by validate_syntax."""
        func = raise_if_mismatched_encodings
        expected_exception = exceptions.EncodingOperationError
        true_positives = self.resource_dict[True]
        true_negatives = ["illegal_syntax_declaration_encoding_value_4.xml",
                          "illegal_syntax_declaration_encoding_mismatch_4.xml"]
        true_negatives = [self.failing_directory.joinpath(f) for f in true_negatives]

        for filename in true_positives:
            with self.subTest(true_pos_filename=filename):
                try:
                    func(filename)
                except expected_exception as unexpected:
                    # False negative!
                    msg = ("Got a false negative - the function raised "
                           f"{expected_exception} for a case it should not "
                           "have.")
                    raise AssertionError(msg) from unexpected
                except Exception as unexpected:
                    raise AssertionError() from unexpected
                else:
                    pass

        for filename in true_negatives:
            with self.subTest(true_neg_filename=filename):
                msg = ("Got a false positive - the case should have raised an "
                       "error but did not.")
                with self.assertRaises(Exception, msg=msg) as error:
                    func(filename)
                msg = ("Got a false negative - wrong exception was raised.")
                self.assertIsInstance(error.exception, expected_exception, msg=msg)


if __name__ == '__main__':
    unittest.main()
