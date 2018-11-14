#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the settings data object derived from the CORE_SETTINGS.ini

Copyright Ian Vermes 2018
"""

from tests.base_testcases import INIandSettingsTestCase, ExtendedTestCase
from validator.helpers import settings_handler
from validator import exceptions

import unittest
import os
import time
from io import StringIO
from contextlib import redirect_stdout



INI_PARTIAL_NAME = "CORE_SETTINGS.ini"
PACKAGE_ROOT = '../..'
PACKAGE_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), PACKAGE_ROOT))

class TestSingletonMetaClass(ExtendedTestCase):

    def setUp(self):

        msg = "set value"

        class ExampleSingleton(metaclass=settings_handler.Singleton):
            def __init__(self, arg):
                self.value = arg

        class ExampleSingletonSideEffect(ExampleSingleton):
            def __init__(self, arg):
                super(ExampleSingletonSideEffect, self).__init__(arg)
                # Sideeffect - should only happen once ever
                # with a singeton class call
                print(msg)

        self.arg = "Foo"
        self.ExampleSingleton = ExampleSingleton
        self.ExampleSingletonSideEffect = ExampleSingletonSideEffect
        self.printed_message = msg

    def tearDown(self):
        metaclass = settings_handler.Singleton
        classes = (self.ExampleSingleton, self.ExampleSingletonSideEffect)
        for class_ in classes:
            try:
                metaclass.reset_singleton(class_)
            except KeyError:
                continue

    def test_instances_follow_singleton_pattern(self):
        instance1 = self.ExampleSingleton(self.arg)
        instance2 = self.ExampleSingleton(self.arg)

        self.assertIs(instance1, instance2)
        self.assertIs(instance1.value, instance2.value)

    def test_singleton_calls_do_not_call_init_more_once(self):
        expected_msg = self.printed_message
        expected_count = 1

        with StringIO() as f:
            with redirect_stdout(f) as caputured_stdout:
                _ = self.ExampleSingletonSideEffect(self.arg)
                _ = self.ExampleSingletonSideEffect(self.arg)

            caputured_stdout = caputured_stdout.getvalue()
        actual_count = caputured_stdout.count(expected_msg)

        self.assertIn(expected_msg, caputured_stdout)
        self.assertEqual(expected_count, actual_count)

    def test_singleton_first_instantiation_needs_argument(self):

        with self.assertRaises(TypeError):
            self.ExampleSingleton()

    def test_singleton_subsequent_instantiation_tolerates_argument(self):
        arg1 = self.arg
        arg2 = "Bar"

        instance1 = self.ExampleSingleton(arg1)
        try:
            instance2 = self.ExampleSingleton(arg2)
        except TypeError:
            errmsg = ("Did not expect TypeError; __init__ called twice thus "
                      "subsequent class calls intolerent of having an "
                      "argument.")
            self.fail(errmsg)

    def test_singleton_subsequent_instantiation_expects_no_argument(self):
        instance1 = self.ExampleSingleton(self.arg)
        try:
            instance2 = self.ExampleSingleton()
        except TypeError:
            errmsg = ("Did not expect TypeError; __init__ called twice thus "
                      "subsequent class calls calls are expecting an argument "
                      "which is incorrect.")
            self.fail(errmsg)

    def test_singleton_instantiation_sets_value_on_first_call(self):
        arg1 = self.arg
        arg2 = "Bar"

        instance1 = self.ExampleSingleton(arg1)
        instance2 = self.ExampleSingleton(arg2)

        self.assertEqual(instance1.value, arg1)
        self.assertEqual(instance1.value, instance2.value)

        self.assertNotEqual(instance1.value, arg2)
        self.assertNotEqual(instance2.value, arg2)


class TestSettingsDataSingleton(INIandSettingsTestCase):

    @classmethod
    def setUpClass(cls):
        cls.inifile = cls.find_and_get_path(
            INI_PARTIAL_NAME, PACKAGE_DIRECTORY)

    def tearDown(self):
        # Reset the singleton so that singletons created between tests are unique.
        metaclass = settings_handler.Singleton
        class_ = settings_handler.Settings
        try:
            metaclass.reset_singleton(class_)
        except KeyError:
            pass  # A test may not have created a singleton.

    def test_instantiation_requires_ini_argument(self):
        inifile = self.inifile
        settings_handler.Settings(inifile)

    def test_failed_instantiation_raises_package_error(self):
        inifile = "Foo"
        assert not os.path.isfile(inifile), os.path.join(os.getcwd(), inifile)
        with self.assertRaises(exceptions.FileNotFound):
            settings_handler.Settings(inifile)

    def test_instances_follow_singleton_pattern(self):
        metaclass = settings_handler.Singleton
        class_ = settings_handler.Settings

        self.assertIsInstance(class_, metaclass)

    def test_has_expected_attributes(self):
        expected_attributes = set(["log_filename"])
        singleton = settings_handler.Settings(self.inifile)

        for expected in expected_attributes:
            with self.subTest(attr=expected):

                self.assertHasAttr(obj=singleton, attrname=expected)

    def test_attributes_are_not_settable(self):
        singleton = settings_handler.Settings(self.inifile)
        # No magic or 'private' attributes
        attributes = [a for a in dir(singleton) if not a.startswith("_")]
        if len(attributes) < 1:
            self.fail("Not Written")

        some_var = str(time.time())  # Unique string.

        for attribute in attributes:
            with self.subTest(attr=attribute):
                with self.assertRaises(AttributeError):
                    setattr(singleton, attribute, some_var)

    def test_specific_attribute_LOG_FILENAME(self):
        singleton = settings_handler.Settings(self.inifile)
        var = singleton.log_filename

        self.assertIsInstance(var, str)
        self.assertTrue(os.path.isfile(var))






if __name__ == '__main__':
    unittest.main()
