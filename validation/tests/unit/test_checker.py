#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test suite for the Checker class

Copyright Ian Vermes 2019
"""

from tests.base_testcases import ExtendedTestCase
from checker import Checker
from helpers.checkschema import validate_schema
from helpers.checksyntax import validate_syntax
from helpers.result import ValidationResult
import exceptions

import functools
import pathlib
import os

class TestChecker(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.resources = cls.get_resource_files()
        cls.Checker = functools.partial(Checker)

    def test_class_instantiation(self):
        _ = self.Checker()

    def test_attribute_VALIDATORS(self):
        attr_name = "validators"
        checker = self.Checker()

        # Test1 - correct attribute name
        self.assertHasAttr(checker, attr_name)

        # Test2 - readonly type
        values = getattr(checker, attr_name)
        self.assertIsInstance(values, tuple)

        # Test3 - correct member count
        self.assertEqual(len(values), 2)

        # Test4 - correct member identities
        expected = [validate_schema, validate_syntax]
        for func in expected:
            self.assertIn(func, values)

        # Test5 - order of members is correct
        expected.sort()
        self.assertSequenceEqual(expected, values)

    def test_method_FEED_IN(self):
        method_name = "feed_in"
        checker = self.Checker()

        # Test1
        self.assertHasAttr(checker, method_name)

        # Test2
        method = getattr(checker, method_name)

        # Test3 - extant files yield validation result
        input_files = self.resources[True][0], self.resources[False][0]

        for input_file in input_files:
            basename = os.path.basename(input_file)
            for input in [str(input_file), pathlib.Path(input_file)]:
                self.assertTrue(os.path.isfile(input), msg="Precondition")
                with self.subTest(arg_type=type(input), name=basename):
                    result = method(input)
                    self.assertIsInstance(result, ValidationResult)

        # Test4 - non-extant files raise exception
        input_file = "foobar.xml"
        expected_exception = exceptions.FileNotFound

        for input in [str(input_file), pathlib.Path(input_file)]:
            self.assertFalse(os.path.isfile(input), msg="Precondition")
            with self.subTest(arg_type=type(input), name=basename):
                with self.assertRaises(expected_exception) as _:
                    method(input)

    @classmethod
    def get_resource_files(cls):
        glob_pattern = "*.xml"
        directories = {True: ["tests/resources/valid"],
                       False: ["tests/resources/schema", "tests/resources/syntax"]
        }
        files = {}
        for validity, dir_list in directories.items():
            for directory in dir_list:
                path = pathlib.Path(directory)
                if not path.exists():
                    raise NotADirectoryError("Precondition " + str(path))
                else:
                    xmls = list(path.glob(glob_pattern))
                    files.setdefault(validity, []).extend(xmls)
        return files
