#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""
from tests.base_testcases import ExtendedTestCase
from tests.validation_testcases import ValidationTestCase
from helpers.checkencoding import validate_syntax
from helpers.enum import Passing
from helpers.result import ValidationResult
import exceptions

from lxml import etree

import unittest


class TestValidateSchemaFunction(ValidationTestCase, ExtendedTestCase):
    """Some test methods are written in the first parent class
    """

    @classmethod
    def setUpClass(cls):
        resource = "tests/resources/syntax"
        func = validate_syntax
        failing_enum = Passing.SYNTAX

        cls.preSetup(directory=resource, validator=func, enum=failing_enum)
        cls.resource_dict = cls.get_resources()

if __name__ == '__main__':
    unittest.main()
