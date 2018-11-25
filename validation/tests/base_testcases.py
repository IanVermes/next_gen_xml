#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""A class that extends unittest.TestCase with additional methods."""

import tests.context

from collections import namedtuple

import unittest
import os
import glob

# To allow consistent imports of pkg modules
tests.context.main()

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


class ExtendedTestCase(unittest.TestCase):

    def assertHasAttr(self, obj, attrname, message=None):
        """Assert whether an object has the expected attribute."""
        if not hasattr(obj, attrname):
            if message is not None:
                self.fail(message)
            else:
                self.fail(HAS_ATTR_MESSAGE.format(obj, attrname))


class CommandLineTestCase(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        expanduser = os.path.expanduser
        abspath = os.path.abspath
        cls.dir_valid = abspath(expanduser("~/Desktop"))
        cls.dir_invalid = abspath(expanduser("~/FooBar"))
        cls.file_valid = abspath(expanduser("tests/resources/valid.xml"))
        assert os.path.isdir(cls.dir_valid)
        assert not os.path.isdir(cls.dir_invalid)
        assert os.path.isfile(cls.file_valid)


class INIandSettingsTestCase(ExtendedTestCase):

    @staticmethod
    def find_and_get_path(filename, root_dir):
        path = None

        for root, dirs, files in os.walk(root_dir):
            for candidate_file in files:
                if filename == candidate_file:
                    path = os.path.abspath(os.path.join(root, filename))
                    break

        if path is not None:
            return path
        else:
            msg = (f"file:'{filename}' was not found despite "
                   f"walking dir:'{root_dir}.'")
            raise FileNotFoundError(msg)


class XMLValidationTestCase(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.invalid_attr = invalid = "illegal"
        cls.valid_attr = valid = "valid"
        criteria = f"{valid} {invalid} syntax document rules".split()
        FileProperties = namedtuple("FileProperties", criteria)

        # Strings
        cls.asserttype = {True: "TruePositive", False: "TrueNegative"}
        cls.falsepositive_msg = ("{expect} expected from {file}, got "
                                 "FalsePositive instead.")
        cls.falsenegative_msg = ("{expect} expected from {file}, got "
                                 "FalseNegative instead which raised this "
                                 "unexpected exception: {exc}")
        cls.detail_msg = ("\nproperty.{attr}: {expect}, resValid: {actual}")

        resources = "tests/resources"
        resources = os.path.abspath(resources)
        assert os.path.isdir(resources), f"Could not find {resources}"
        files = glob.iglob(os.path.join(resources, "*.xml"))
        iter_assessment = cls.assess_resources(files, criteria)
        cls.files = {f: FileProperties(**d) for f, d in iter_assessment}

    @staticmethod
    def assess_resources(files, criteria):
        """Identify the presence or absence of keywords in resource filenames.

        Depending on substrings in criteria, check if substring in filename.
        e.g. check if 'illegal' and 'document' in illegal_document_bad_isbn.xml

        Yields:
            str, dict
        """
        for fullname in files:
            assessment = dict()
            name = os.path.basename(fullname).lower()
            for substring in criteria:
                assessment[substring] = substring in name
            yield fullname, assessment

    @classmethod
    def get_files_by_criterion(cls, criterion):
        """Get all resources & properties that have properties.<criterion>==True.

        Yields:
            tuple(str, FileProperties)
        """
        resources_iter = cls.get_resources_by_criterion(criterion)
        for filename in resources_iter:
            yield filename, cls.files[filename]

    @classmethod
    def get_resources_by_criterion(cls, criterion):
        """Get all filenames/resources that have properties.<criterion>==True.

        Yields:
            str
        """
        for filename, properties in cls.files.items():
            flag = getattr(properties, criterion, None)
            if flag is None:
                msg = f"namedtuple '{properties}' has no attribute {criterion}."
                raise AttributeError(msg)
            if not flag:
                continue
            else:
                yield filename


    def assertNoFalsePositivesOrNegatives(self, values, criterion, validator,
                                          permitted_exceptions,
                                          propogate=False):
        """Tests if known values are pass through validation fucntions correctly.

        Args:
            values(dict): Keys  : filenames
                          Values: FileProperties namedtuple
            criterion(string): An attribute of a FileProperties object.
            validator(func): A boolean function that operates on a filename.
            permitted_exceptions(Exception/Exceptions)
        Kwargs:
            propogate(bool): If True raise AssertionError exceptions, otherwise
                let the testrunner handle things.
        Exceptions:
            FalseNegative
            FalsePositive
        """

        # Setup
        filtered = {}
        for file, properties in values.items():
            filtered[file] = getattr(properties, criterion)

        try:
            permitted_exceptions = tuple(permitted_exceptions)
        except TypeError:
            permitted_exceptions = (permitted_exceptions, )

        # Perform validation operation and collect results
        for file, expectValid in filtered.items():
            try:
                resValid = validator(file)  # Two Outcomes: bool + exc
            except Exception as exc:
                resValid = False  # Auto-false.
                resExc = exc
            else:
                resExc = None

            # The resValid method should be boolean-like for this test
            # as ducktesting approach is not sufficient. X is True or False
            # leaves no ambiguity
            try:
                if not isinstance(resValid, bool):
                    raise TypeError()
            except TypeError as exc:
                if hasattr(resValid, "__bool__"):
                    resValid = bool(resValid)
                    resExc = None
                else:
                    msg = ("Validator return object is neither a boolean nor "
                           "has a __bool__ method, preventing False "
                           f"Positive/Negative evaluation: {type(resValid)}")
                    raise ValueError(msg) from exc

            shortname = os.path.basename(file)
            args = (resValid, expectValid, criterion, propogate, shortname)
            kwargs = {"result": resValid,
                      "expected": expectValid,
                      "exception": resExc,
                      "expected_exceptions": permitted_exceptions}
            if propogate is False:
                with self.subTest(filename=shortname, property=criterion):
                    self._falsePositiveNegative_logic(*args, **kwargs)
            else:
                self._falsePositiveNegative_logic(*args, **kwargs)

    def _falsePositiveNegative_logic(self, resValid, expectValid, criterion,
                                     propogate, shortname, **kwargs):
        # Draw assertions from results
        try:
            if resValid is True:
                self.raisesIfNotTruePositive(**kwargs)
            elif resValid is False:
                self.raisesIfNotTrueNegative(**kwargs)
        except FalsePositive:
            if propogate is True:
                raise
            msg = self.falsepositive_msg
            msg = msg.format(expect=self.asserttype[resValid],
                             file=shortname)
        except FalseNegative as exc:
            if propogate is True:
                raise
            msg = self.falsenegative_msg
            msg = msg.format(expect=self.asserttype[resValid],
                             file=shortname,
                             exc=repr(exc.__cause__))
        else:
            msg = ""  # TruePositive and TrueNegative pass the test

        if msg and propogate is False:
            detail = self.detail_msg
            detail = detail.format(attr=criterion,
                                   expect=expectValid,
                                   actual=resValid)
            self.fail(msg + detail)


    def raisesIfNotTruePositive(self, result, expected, exception, expected_exceptions=None):
        """Raise exceptions unless result is expected & that exception is None.

        Precondition:
            result is True
        Args:
            result(bool)
            expected(bool)
            exception(NoneType, Exception)
        Kwargs
            expected_exceptions(Exception or tuple of Exceptions)

        Exceptions:
            FalseNegative
            FalsePositive
        """
        # Guard block: result == True when we call this.
        if result is not True:  # i.e. result is not a positive of some sort.
            msg = ("This function applies logic to positives only, result arg "
                   "is negative.")
            raise ValueError(msg)
        # Check block
        if result == expected:
            if exception is None:
                return  # TruePositive
            elif expected_exceptions and isinstance(exception, expected_exceptions):
                raise FalseNegative() from exception  # FalseNegative despite result == expected
            elif isinstance(exception, Exception):
                raise FalseNegative() from exception  # FalseNegative despite result == expected
            else:
                msg = ("Expected NoneType or Exception, got exception: "
                       f"{repr(exception)}")
                raise TypeError(msg)
        else:
            raise FalsePositive()  # FalsePositive

    def raisesIfNotTrueNegative(self, result, expected, exception, expected_exceptions):
        """Raise exceptions unless result is different to expected or exceptions cant be handled

        Precondition:
            result is False
        Args:
            result(bool)
            expected(bool)
            exception(NoneType, Exception)
            expected_exceptions(Exception or tuple of Exceptions)

        Exceptions:
            FalseNegative
        """
        # Guard block: result == False when we call this.
        if result is True:  # i.e. result is not a negative of some sort.
            msg = ("This function applies logic to negatives only, result arg "
                   "is positive.")
            raise ValueError(msg)
        # Check block
        if result == expected:
            if exception is None:
                return  # TrueNegative
            elif isinstance(exception, expected_exceptions):
                return  # TrueNegative
            elif isinstance(exception, Exception):
                raise FalseNegative() from exception  # FalseNegative despite result == expected
            else:
                msg = ("Expected NoneType or Exception, got exception: "
                       f"{repr(exception)}")
                raise TypeError(msg)
        else:
            raise FalseNegative()  # FalseNegative


class FalsePositive(AssertionError):
    """Raise when the expectation and result match yet they should not."""


class FalseNegative(AssertionError):
    """Raise when the expectation and result do not match yet they should."""
