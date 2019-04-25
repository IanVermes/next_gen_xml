#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A TestCase for XML validation that depends on resource files.

Decorators:
    preSetupCheck

Classes:
    ValidationTestCase
"""

import tests.base_testcases

from helpers.result import ValidationResult
from helpers.enum import Passing

import functools
import inspect
import pathlib


def preSetupCheck(func):
    """A decorator that gives a more useful reason why an error arose."""
    functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except AttributeError as err:
            errtype = err.__class__.__name__
            msg = (f"{errtype} is due to preSetup() not called "
                   "within setUpClass()")
            raise RuntimeError(msg) from err
        return result
    return decorator


class ValidationTestCase():
    """This class should be multiply inherited with unittest.TestCase.

    This class should be the first positional argument in the class defintion.

    Tests:
        test_validator_passes_valid_files
        test_validator_fails_illegal_files
        test_validator_input_arg_does_not_raise_TypeError

    Class methods:
        preSetup: Should be called inside the classSetup method of the child
            class. It initialises the test cases with helpful attributes like
            the validation function and the file resources necessary for tests
        find_xml: Convenience method. Finds files in a directory that are both
            XML files and also share the direcory name in the file name.
        get_resources: Returns a dictionary with both valid and illegal XML. The
            illegal files are discovered conditionally if preSetup was called.
    """

    _PRECONDITION_TEMPLATE = "Precondition failed: {}"
    _GLOB_XML_PATTERN = "*.xml"

    def test_validator_passes_valid_files(self):
        validator = self.validator
        for file in self.resource_dict[True]:

            with self.subTest():
                result = validator(file)

                # Test1
                self.assertIsInstance(result, ValidationResult)
                # Test2
                self.assertTrue(result)
                # Test3
                expected = Passing.PASSING
                self.assertEqual(expected, result.enum)

    def test_validator_fails_illegal_files(self):
        validator = self.validator
        for file in self.resource_dict[False]:

            with self.subTest():
                result = validator(file)

                # Test1
                self.assertIsInstance(result, ValidationResult)
                # Test2
                self.assertFalse(result)
                # Test3
                expected = Passing.SYNTAX
                self.assertEqual(expected, result.enum)

    def test_validator_input_arg_does_not_raise_TypeError(self):
        self.fail("not written")

    @classmethod
    def preSetup(cls, directory, validator):
        msg = cls._PRECONDITION_TEMPLATE
        assert inspect.isfunction(validator), msg.format(str(validator))
        cls.validator = functools.partial(validator)

        directory = pathlib.Path(directory)
        assert directory.exists(), msg.format(str(directory))
        cls.failing_directory = directory

        passing_directory = pathlib.Path("tests/resources/valid")
        assert passing_directory.exists(), msg.format(str(passing_directory))
        cls.passing_directory = passing_directory

    @classmethod
    @preSetupCheck
    def get_resources(cls):
        pairs = [(True, cls.passing_directory),
                 (False, cls.failing_directory)]
        result = dict()
        for validity, directory in pairs:
            files = cls.find_xml(directory)
            if len(files) > 0:
                result[validity] = files
            else:
                msg = f"Could not find enough files in {str(directory)}"
                raise ValueError(msg)
        return result

    @classmethod
    def find_xml(cls, directory):
        files = list()
        for candidate in directory.glob(cls._GLOB_XML_PATTERN):
            if directory.name in candidate.stem:
                files.append(candidate)
        files = tuple(files)
        return files
