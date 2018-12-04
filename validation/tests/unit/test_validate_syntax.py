#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidation
from helpers.xml import validate_syntax, ValidationResult
import exceptions

import os
import unittest


class TestSyntaxValidation(XMLValidation.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.criterion = criterion = "syntax"
        cls.base_exc = exceptions.SyntaxValidationError
        cls.valid_file = next(cls.get_resources_by_criterion("valid"))
        cls.illegal_file = next(cls.get_resources_by_criterion(criterion))
        cls.result_type = ValidationResult
        cls.imported_validation_func = (validate_syntax, )

    def test_nofalses_after_syntax_validation(self):

        kwargs = {"values": self.files,
                  "criterion": self.criterion,
                  "validator": self.validator,
                  "permitted_exceptions": self.base_exc}
        self.assertNoFalsePositivesOrNegatives(**kwargs)


if __name__ == '__main__':
    unittest.main()
