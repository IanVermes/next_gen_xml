#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML encoding subvalidator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidation
from helpers.xml import validate_encoding, ValidationResult
import exceptions

from lxml import etree

import os
import unittest
import functools


class TestEncodingValidation(XMLValidation.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.criterion = criterion = "encoding"
        cls.base_exc = exceptions.SyntaxValidationError
        cls.valid_files = list(cls.get_resources_by_criterion("valid"))
        cls.valid_file = cls.valid_files[0]
        cls.illegal_file = next(cls.get_resources_by_criterion(criterion))
        cls.result_type = ValidationResult
        cls.imported_validation_func = (validate_encoding, )

    def test_nofalses_after_encoding_validation(self):

        kwargs = {"values": self.files,
                  "criterion": self.criterion,
                  "validator": self.validator,
                  "permitted_exceptions": self.base_exc}
        self.assertNoFalsePositivesOrNegatives(**kwargs)
