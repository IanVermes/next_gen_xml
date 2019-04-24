#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML schema validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidation
from helpers.checkschema import SchemaOperations, validate_schema
from helpers.enum import EncodingErrorCode
from helpers.result import ValidationResult

from lxml import etree

import exceptions

import unittest


class TestSchemaValidation(XMLValidation.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.criterion = criterion = "schema"
        cls.base_exc = exceptions.SchemaValidationError
        cls.valid_file = next(cls.get_resources_by_criterion("valid"))
        cls.illegal_file = next(cls.get_resources_by_criterion(criterion))
        cls.result_type = ValidationResult
        cls.cause_exc = etree.DocumentInvalid
        cls.imported_validation_func = (validate_schema, )

    def test_validation_func_return_type(self):
        self.fail("not written")


if __name__ == '__main__':
    unittest.main()
