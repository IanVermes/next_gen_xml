#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""A class that extends unittest.TestCase with additional methods."""

import unittest
import os

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
        cls.file_valid = abspath(expanduser("tests/resources/valid_document.xml"))
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
