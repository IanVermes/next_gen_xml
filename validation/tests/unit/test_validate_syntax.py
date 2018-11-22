#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase
from helpers.xml import validate_syntax
import exceptions

import os
import unittest
import functools


class TestSyntaxValidation(XMLValidationTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_exc = exceptions.NextGenError

    def _validator(self, *args, _func):
        """Basis for partialmethod"""
        return _func(*args)

    validator = functools.partialmethod(_validator, _func=validate_syntax)

    @unittest.expectedFailure
    def test_fail(self):
        self.fail("Not written.")

    def test_nofalses_after_syntax_validation(self):

        kwargs = {"values": self.files,
                  "criterion": "syntax",
                  "validator": self.validator,
                  "permitted_exceptions": self.base_exc}
        self.assertNoFalsePositivesOrNegatives(**kwargs)

if __name__ == '__main__':
    unittest.main()
