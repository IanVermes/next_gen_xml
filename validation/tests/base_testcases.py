#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""A class that extends unittest.TestCase with additional methods."""

import tests.context

from collections import namedtuple
from types import FunctionType

import unittest
import os
import glob
import functools

# To allow consistent imports of pkg modules
tests.context.main()

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


class ExtendedTestCase(unittest.TestCase):

    def assertHasAttr(self, obj, attrname, message=None):
        """Assert whether an object has the expected attribute."""
        if not hasattr(obj, attrname):
            if message is not None:
                raise AssertionError(message)
            else:
                raise AssertionError(HAS_ATTR_MESSAGE.format(obj, attrname))

    def assertSubstringsInString(self, substrings, string, msg=None):
        method = "IN"
        self._SubstringsInString_base(substrings, string, method, msg=msg)

    def assertSubstringsNotInString(self, substrings, string, msg=None):
        method = "NOT IN"
        self._SubstringsInString_base(substrings, string, method, msg=msg)

    def _SubstringsInString_base(self, substrings, string, method, msg=None):

        # Precondition
        if isinstance(substrings, str):
            substrings = [substrings]  # Rather than raise a type error.
        if not substrings:
            errmsg = f"Positional argument 1 is invalid: {repr(substrings)}"
            raise ValueError(errmsg)
        if not string:
            errmsg = f"Positional argument 2 is invalid: {repr(string)}"
            raise ValueError(errmsg)
        methods = ("IN", "NOT IN")
        if method not in methods:
            raise ValueError(f"Method arg not valid: chose from {methods}.")

        # Dependent setup:
        def spaceing(n_spaces):
            return "\n" + " " * n_spaces
        if method == "IN":
            line_0 = f"{len(substrings)} substrings were found in the string."
            line_1 = f"{spaceing(4)}Unexpectedly missing:"
            criteria_subs = [sub for sub in substrings if sub not in string]
        else:
            line_0 = f"{len(substrings)} substrings were absent from the string."
            line_1 = f"{spaceing(4)}Unexpectedly present:"
            criteria_subs = [sub for sub in substrings if sub in string]
        # General setup:
        count = len(criteria_subs)  # Expect zero to pass assertion

        # Main loop
        if count > 0:
            detail = "".join([(spaceing(8) + "- " + s) for s in criteria_subs])
            errmsg = "".join([f"{len(substrings) - count} out of ",
                              line_0, line_1, f"{detail}"])
            if msg:
                errmsg = errmsg + f"{spaceing(4)}Custom message : {msg}"
            raise AssertionError(errmsg)
        else:
            return


class CommandLineTestCase(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        expanduser = os.path.expanduser
        abspath = os.path.abspath
        cls.dir_valid = abspath(expanduser("~/Desktop"))
        assert os.path.isdir(cls.dir_valid)
        cls.file_valid = abspath(expanduser("tests/resources/valid/valid.xml"))
        assert os.path.isfile(cls.file_valid)
        cls.file_wrongtype = abspath(expanduser(__file__))
        assert os.path.isfile(cls.file_wrongtype)
        cls.dir_invalid = abspath(expanduser("~/FooBar"))
        assert not os.path.isdir(cls.dir_invalid)
        cls.file_invalid = abspath(expanduser("~/FooBar/imaginaryfile.xml"))
        assert not os.path.isfile(cls.file_invalid)



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


class XMLValidationAbstractCase(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.invalid_attr = invalid = "illegal"
        cls.valid_attr = valid = "valid"
        criteria = f"{valid} {invalid} syntax encoding document rules schema"
        criteria = criteria.split()
        FileProperties = namedtuple("FileProperties", criteria)

        # Strings
        cls.asserttype = {True: "TruePositive", False: "TrueNegative"}
        cls.falsepositive_msg = ("{expect} expected from {file}, got "
                                 "FalsePositive instead.")
        cls.falsenegative_msg = ("{expect} expected from {file}, got "
                                 "FalseNegative instead which raised this "
                                 "unexpected exception: {exc}")
        cls.detail_msg = ("\nproperty.{attr}: {expect}, resValid: {actual}")

        #Files
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

        # Setup:
        #   A file is explicitly valid or illegal, but a criterion
        #   may determine if a file is valid for that criterion in particular
        #      E.g. illegal_syntax.xml is illegal BUT valid in terms
        #      of schema YET illegal in terms of syntax
        filtered = {}
        for file, properties in values.items():
            if criterion in (self.valid_attr, self.invalid_attr):
                # Get absolute, explicit validity
                validity = getattr(properties, criterion)
            else:
                # Get implicit, criterion-focused validity
                has_criterion = getattr(properties, criterion)
                assert isinstance(has_criterion, bool)
                if has_criterion:
                    validity = False
                else:
                    validity = True
            filtered[file] = validity

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
            msg = msg.format(expect=self.asserttype[expectValid],
                             file=shortname)
        except FalseNegative as exc:
            if propogate is True:
                raise
            msg = self.falsenegative_msg
            msg = msg.format(expect=self.asserttype[expectValid],
                             file=shortname,
                             exc=repr(exc.__cause__))
        else:
            msg = ""  # TruePositive and TrueNegative pass the test

        if msg and propogate is False:
            detail = self.detail_msg
            detail = detail.format(attr=criterion,
                                   expect=expectValid,
                                   actual=resValid)
            raise AssertionError(msg + detail)


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


def decorate_tests(decorator):
    """Create a metaclass to decorate test methods with the same decorator.

    source: https://stackoverflow.com/a/10067363
    """

    def do_decorate(attr, value):
        """Boolean check if an object should be decorated."""
        flag = ('__' not in attr and
                attr.lower().startswith("test_") and
                isinstance(value, FunctionType))
        return flag

    class DecorateAll(type):
        def __new__(cls, name, bases, dct):
            for attr, value in dct.items():
                if do_decorate(attr, value):
                    dct[attr] = decorator(value)
            return super(DecorateAll, cls).__new__(cls, name, bases, dct)
        def __setattr__(self, attr, value):
            if do_decorate(attr, value):
                value = decorator(value)
            super(DecorateAll, self).__setattr__(attr, value)
    return DecorateAll


class XMLValidation:
    """Container of XMLValidation.TestCase and supporting functions."""

    def verify_setUpClass(func):
        """Decorator that verifies setUpClass assigned attributes were set."""

        def verify_attributes(instance):
            expected_attrs = ["criterion",
                              "base_exc",
                              "cause_exc",
                              "valid_file",
                              "illegal_file",
                              "result_type",
                              "imported_validation_func"]
            detected = {attr: hasattr(instance, attr) for attr in expected_attrs}
            if not all(detected.values()):
                missing = [attr for attr, isPresent in detected.items() if not isPresent]
                missing = ",\n\t".join(missing)
                msg = ("setUpClass method for this TestCase "
                       f"'{instance.__class__.__name__}' needs to assign "
                       "attributes. The following class attributes were "
                       f"expected but not declared:\n\t{missing}")
                raise NotImplementedError(msg)

        functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Test method decorator
            try:
                verify_attributes(args[0])
            except NotImplementedError:
                raise
            else:
                return_val = func(*args, **kwargs)
            return return_val
        return wrapper


    class TestCase(XMLValidationAbstractCase, metaclass=decorate_tests(verify_setUpClass)):
        """Collection of validition related tests, repeated for each validator."""

        def _validator(self, *args, _func):
            """Basis for partialmethod"""
            return _func(*args)

        def validator(self, *args):
            """Main validation function of the testcase."""
            func = self.imported_validation_func[0]
            result = func(*args)
            return result

        def test_validation_passes_with_valid_file(self):
            filename = self.valid_file

            result = self.validator(filename)

            self.assertTrue(result)

        def test_validation_fails_with_illegal_file(self):
            filename = self.illegal_file

            result = self.validator(filename)

            self.assertFalse(result)

        def test_failed_validation_result_has_correct_exception(self):
            filename = self.illegal_file
            expected_pkg_exc = self.base_exc
            expected_cause_exc = self.cause_exc

            result = self.validator(filename)

            with self.assertRaises(expected_pkg_exc):
                raise result.exception
            with self.assertRaises(expected_cause_exc):
                raise result.exception.__cause__

        def test_validation_returns_result_obj(self):
            filename = self.illegal_file

            result = self.validator(filename)

            self.assertIsInstance(result, self.result_type)

        def test_other_illegal_files_pass(self):
            """Similar to test_nofalses_after_syntax_validation but explict."""
            for filename, properties in self.files.items():
                is_illegal = getattr(properties, self.invalid_attr)
                has_syntax_err = getattr(properties, self.criterion)

                if is_illegal and not has_syntax_err:
                    with self.subTest(name=os.path.basename(filename)):
                        result = self.validator(filename)

                        self.assertTrue(result)
