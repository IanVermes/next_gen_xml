#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML schema validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidation, ExtendedTestCase
from helpers.checkschema import SchemaOperations, validate_schema
from helpers.enum import EncodingErrorCode
from helpers.result import ValidationResult

from lxml import etree

import exceptions

import unittest
import sys


class TestSchemaDependency(ExtendedTestCase):

    def tearDown(self):
        try:
            del sys.modules['helpers.checkschema']
        except KeyError:
            pass

    def test_module_loads_has_a_schema_global(self):
        expected_attr = "SCHEMA"

        import helpers.checkschema
        module = helpers.checkschema

        # Test1
        self.assertHasAttr(module, expected_attr)

        # Test2
        candidate = getattr(module, expected_attr)
        self.assertIsInstance(candidate, etree.XMLSchema)

    def test_module_loads_with_settings_singleton_global(self):
        expected_attr = "SETTINGS"

        import helpers.checkschema
        module = helpers.checkschema

        self.assertHasAttr(module, expected_attr)


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
