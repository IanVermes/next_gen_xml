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

        resources = "tests/resources"
        resources = os.path.abspath(resources)
        assert os.path.isdir(resources), f"Could not find {resources}"
        files = glob.iglob(os.path.join(resources, "*.xml"))
        iter_assessment = cls.assess_filenames(files, criteria)
        cls.files = {f: FileProperties(**d) for f, d in iter_assessment}

    @staticmethod
    def assess_filenames(files, criteria):
        # criteria = set([c.lower() for c in criteria])

        for fullname in files:
            assessment = dict()
            name = os.path.basename(fullname).lower()
            for substring in criteria:
                assessment[substring] = substring in name
            yield fullname, assessment


    # FalsePositive/FalseNegative method that takes files, criterion, validator and exceptions.
