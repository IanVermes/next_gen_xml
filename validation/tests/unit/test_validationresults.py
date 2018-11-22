#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML result class spawned by various validators.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from helpers.xml import ValidationResult

import exceptions as pkg_excs


class TestValidationResult(ExtendedTestCase):

    def test_instantialization_succeeds_with_package_exception(self):
        self.fail("Not Written")

    def test_instantialization_succeeds_with_None(self):
        self.fail("Not Written")

    def test_instantialization_fails_with_other_exception(self):
        self.fail("Not Written")

    def test_instantialization_fails_without_exception(self):
        self.fail("Not Written")

    def test_attributes_are_properties(self):
        self.fail("Not Written")

    def test_is_false_with_exception_attr(self):
        self.fail("Not Written")

    def test_is_true_without_exception_attr(self):
        self.fail("Not Written")

    def test_passed_XXX_attrs_true_if_without_exception(self):
        self.fail("Not Written")

    def test_passed_XXX_attrs_false_if_any_exception(self):
        self.fail("Not Written")

    def test_passed_syntax_attr_false_if_syntax_error(self):
        self.fail("Not Written")

    def test_passed_syntax_attr_true_not_others_if_schema_error(self):
        self.fail("Not Written")

    def test_passed_syntax_passed_schema_attr_true_not_rules_if_rules_error(self):
        self.fail("Not Written")
