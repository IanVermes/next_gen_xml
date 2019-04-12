#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML result class spawned by various validators.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from helpers.result import ValidationResult

import exceptions as pkg_excs


class TestValidationResult(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.pkg_base_exc = pkg_excs.NextGenError
        cls.base_exc = pkg_excs.ValidationError
        cls.syntax_exc = pkg_excs.SyntaxValidationError
        cls.schema_exc = pkg_excs.SchemaValidationError
        cls.rules_exc = pkg_excs.RuleValidationError

    def test_instantialization_succeeds_with_package_validation_exception(self):
        filename = "FooBar.xml"
        exception = self.base_exc(filename)

        ValidationResult(filename, exception)

    def test_instantialization_succeeds_with_None(self):
        filename = "FooBar.xml"
        exception = None

        ValidationResult(filename, exception)

    def test_instantialization_fails_with_package_general_exception(self):
        filename = "FooBar.xml"
        exception = self.pkg_base_exc(filename)

        with self.assertRaises(TypeError):
            ValidationResult(filename, exception)

    def test_instantialization_fails_with_other_exception(self):
        filename = "FooBar.xml"
        exception = ValueError(filename)

        with self.assertRaises(TypeError):
            ValidationResult(filename, exception)

    def test_instantialization_fails_without_exception(self):
        """This test forbids defining __init__ with a kwarg exception=None"""
        filename = "FooBar.xml"

        with self.assertRaises(TypeError):
            ValidationResult(filename)

    def test_attributes_are_properties(self):
        """This test forbids setting attributes externally."""
        filename = "FooBar.xml"
        exception = self.base_exc(filename)
        result = ValidationResult(filename, exception)
        var = "FooBar"

        attrs = [a for a in dir(result) if not a.startswith("_")]

        for attr in attrs:
            msg = f"result.{attr} can be set"
            with self.assertRaises(AttributeError, msg=msg):
                setattr(result, attr, var)

    def test_args_become_attrs(self):
            filenames = "FooBar.xml", "BazCat.xml"
            exceptions = self.base_exc(filenames[0]), None
            types = self.base_exc, type(None)
            args = filenames, exceptions, types

            for fname, exc, type_ in zip(*args):
                result = ValidationResult(fname, exc)
                self.assertIsInstance(result.exception, type_)
                self.assertEqual(result.filename, fname)

    def test_is_false_with_exception_attr(self):
        filename = "FooBar.xml"
        exception = self.base_exc(filename)
        result = ValidationResult(filename, exception)

        self.assertFalse(result)

    def test_is_true_with_exception_as_None(self):
        filename = "FooBar.xml"
        exception = None
        result = ValidationResult(filename, exception)

        self.assertTrue(result)

    def test_passed_XXX_attrs_true_with_exception_as_None(self):
        filename = "FooBar.xml"
        exception = None
        result = ValidationResult(filename, exception)

        self.assertTrue(result.passed_syntax)
        self.assertTrue(result.passed_schema)
        self.assertTrue(result.passed_rules)
        self.assertTrue(result)

    def test_passed_XXX_attrs_false_if_any_exception(self):
        filename = "FooBar.xml"
        exception = self.base_exc(filename)
        result = ValidationResult(filename, exception)

        self.assertFalse(result.passed_syntax)
        self.assertFalse(result.passed_schema)
        self.assertFalse(result.passed_rules)
        self.assertFalse(result)

    def test_passed_syntax_attr_false_if_syntax_error(self):
        filename = "FooBar.xml"
        exception = self.syntax_exc(filename)
        result = ValidationResult(filename, exception)

        self.assertFalse(result.passed_syntax)
        self.assertFalse(result.passed_schema)
        self.assertFalse(result.passed_rules)
        self.assertFalse(result)

    def test_passed_syntax_attr_true_not_others_if_schema_error(self):
        filename = "FooBar.xml"
        exception = self.schema_exc(filename)
        result = ValidationResult(filename, exception)

        self.assertTrue(result.passed_syntax)
        self.assertFalse(result.passed_schema)
        self.assertFalse(result.passed_rules)
        self.assertFalse(result)

    def test_passed_syntax_passed_schema_attr_true_not_rules_if_rules_error(self):
        filename = "FooBar.xml"
        exception = self.rules_exc(filename)
        result = ValidationResult(filename, exception)

        self.assertTrue(result.passed_syntax)
        self.assertTrue(result.passed_schema)
        self.assertFalse(result.passed_rules)
        self.assertFalse(result)
