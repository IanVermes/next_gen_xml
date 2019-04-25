#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML schema validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from tests.validation_testcases import ValidationTestCase
from helpers.checkschema import SchemaOperations, validate_schema
from helpers.enum import EncodingErrorCode
from helpers.result import ValidationResult

from lxml import etree

import exceptions

import unittest
import sys


class TestValidateSchemaFunction(ValidationTestCase, unittest.TestCase):
    """Some test methods are written in the first parent class
    """

    @classmethod
    def setUpClass(cls):
        resource = "../resources/schema"
        func = validate_schema

        cls.preSetup(directory=resource, validator=func)
        cls.resource_dict = cls.get_resources()

    # Test specific to the schema_validator go here



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

if __name__ == '__main__':
    unittest.main()
