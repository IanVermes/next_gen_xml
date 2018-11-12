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
        cls.dir_valid = os.path.expanduser("~/Desktop")
        cls.dir_invalid = os.path.expanduser("~/FooBar")
        assert os.path.isdir(cls.dir_valid)
        assert not os.path.isdir(cls.dir_invalid)
