#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the settings data object derived from the CORE_SETTINGS.ini

Copyright Ian Vermes 2018
"""

from tests.base_testcases import INIandSettingsTestCase, ExtendedTestCase
from helpers import settings_handler
import exceptions  # from validator import exceptions

import unittest
import os
import time
import pathlib
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

        cls.expected_attributes = ("log_filename", "mode")

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
        attrs = self.expected_attributes
        singleton = settings_handler.Settings(self.inifile)

        for expected in attrs:
            with self.subTest(attrname=expected):

                self.assertHasAttr(obj=singleton, attrname=expected)

    def test_has_no_unexpected_attributes(self):
        expected_attrs = set(self.expected_attributes)
        singleton = settings_handler.Settings(self.inifile)
        attrs = (a for a in dir(singleton) if not a.startswith("_"))

        for actual in attrs:
            with self.subTest(unepexcted_attr=actual):
                msg = f"Suprise: did not expect to find 'singleton.{actual}'"
                self.assertIn(actual, expected_attrs, msg=msg)

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

        dest_dir = os.path.dirname(singleton.log_filename)
        isAbsolute = dest_dir.startswith("/")
        isExpandedUser = "~" in dest_dir

        self.assertIsInstance(var, (str, pathlib.Path))
        self.assertTrue(os.path.isdir(dest_dir), f"Dir: {dest_dir}")
        self.assertTrue(isAbsolute, f"Dir: {dest_dir} is not an absolute path.")
        self.assertFalse(isExpandedUser, f"Dir: {dest_dir} needs userexpansion.")


class TestSettingsDataSingleton_Mode_Kwarg(INIandSettingsTestCase):

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

    def test_singleton_class_accepts_mode_kwarg(self):
        live = settings_handler.Mode.LIVE
        try:
            settings_handler.Settings(self.inifile, mode=live)
        except TypeError as err:
            err_msg = str(err)
            err_kwarg = "keyword argument"
            if err_msg in err_kwarg:
                assertion_msg = "TypeError due to bad keyword argument."
                self.fail(assertion_msg)
            else:
                raise
        else:
            pass  # pass test if kwarg is accepted

    def test_singleton_has_mode_attr(self):
        live = settings_handler.Mode.LIVE
        expected_attr = "mode"

        singleton = settings_handler.Settings(self.inifile, mode=live)

        self.assertHasAttr(obj=singleton, attrname=expected_attr)

    def test_singleton_mode_attr_is_enum(self):
        import enum
        live = settings_handler.Mode.LIVE

        singleton = settings_handler.Settings(self.inifile, mode=live)

        self.assertIsInstance(singleton.mode, enum.Enum)
        self.assertIsInstance(singleton.mode, settings_handler.Mode)

    def test_singleton_mode_defaults_to_live(self):
        Mode = settings_handler.Mode
        expected_mode = Mode.LIVE
        wrong_modes = [m for m in list(Mode) if m is not expected_mode]

        singleton = settings_handler.Settings(self.inifile)

        self.assertIs(singleton.mode, expected_mode)
        self.assertEqual(singleton.mode, expected_mode)
        for some_mode in wrong_modes:
            with self.subTest(wrong_mode=some_mode):
                self.assertIsNot(singleton.mode, some_mode)
                self.assertNotEqual(singleton.mode, some_mode)

    def test_singleton_contextually_presents_different_values(self):
        Mode = settings_handler.Mode
        modes = list(Mode)
        metaclass = settings_handler.Singleton

        results = []
        for some_mode in modes:
                try:
                    instantiated = False
                    singleton = settings_handler.Settings(self.inifile, mode=some_mode)
                except Exception as e:
                    raise
                else:
                    instantiated = True
                    contextual_value = singleton.log_filename
                    results.append(contextual_value)
                finally:
                    # cleanup and reset singeton
                    if instantiated:
                        metaclass.reset_singleton(type(singleton))

        msg = "The values of the attribute did not vary with context."
        set_length = len(set(results))
        self.assertEqual(set_length, len(results), msg=msg)


if __name__ == '__main__':
    unittest.main()
