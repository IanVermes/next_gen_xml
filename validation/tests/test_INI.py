#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of CORE_SETTINGS.ini

Copyright Ian Vermes 2018
"""

from .basesuite import ExtendedTestCase
from validator.helpers import confighandler

import unittest
import configparser
import glob
import os

INI_PARTIAL_NAME = "CORE_SETTINGS.ini"
PACKAGE_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
INI_SECTIONS = ('Log File', 'schema', 'xslt', 'Config Object Attributes')


class TestINIFindable(ExtendedTestCase):

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

    @classmethod
    def setUpClass(cls):
        cls.package_directory = PACKAGE_DIRECTORY

    def test_ini_is_findable(self):
        search_pattern = os.path.join(self.package_directory, "**/*.ini")
        target_file = INI_PARTIAL_NAME

        flag = False
        for path in glob.iglob(search_pattern, recursive=True):
            if target_file in path:
                flag = True
                break

        self.assertTrue(flag,
                        msg=f"Could not find {target_file} in {self.package_directory}")

    def test_ini_is_findable_2(self):
        try:
            self.find_and_get_path(INI_PARTIAL_NAME, self.package_directory)
        except FileNotFoundError as err:
            self.fail(str(err))
        except Exception as err:
            raise err

    def test_ini_is_in_expected_directory(self):
        ini_filename = self.find_and_get_path(
            INI_PARTIAL_NAME, self.package_directory)
        exepected_directory = "validator"

        residing_directory = os.path.basename(os.path.dirname(ini_filename))

        self.assertEqual(exepected_directory, residing_directory)


class TestINIValues(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ini_filename = TestINIFindable.find_and_get_path(
            INI_PARTIAL_NAME, PACKAGE_DIRECTORY)

    def test_ini_file_is_readable(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.ini_filename)
        except configparser.Error as err:
            self.fail(str(err))
        except Exception as err:
            raise err

    def test_ini_for_expected_categories(self):
        expected_sections = set(INI_SECTIONS)
        config = configparser.ConfigParser()
        config.read(self.ini_filename)

        actual_sections = set(config.sections())
        difference = expected_sections ^ actual_sections

        self.assertEqual(0, len(difference),
                         msg=f"INI has unepexcted sections: {difference}")


class TestConfigDataObject(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.section_for_data_object = "Config Object Attributes"
        cls.ini_filename = TestINIFindable.find_and_get_path(
            INI_PARTIAL_NAME, PACKAGE_DIRECTORY)
        cls.config = configparser.ConfigParser()
        cls.config.read(cls.ini_filename)

    def test_config_has_section_for_data_object(self):
        expected_section = self.section_for_data_object

        flag = self.config.has_section(expected_section)

        self.assertTrue(flag)

    def test_config_data_object_instantiation(self):
        try:
            confighandler.ConfigData(self.ini_filename)
        except Exception as err:
            self.fail(f"Could not instantiate ConfigHandler: {str(err)}")

    def test_config_data_has_expected_attrs(self):
        data = confighandler.ConfigData(self.ini_filename)
        excepected_attrs = self.config.options(self.section_for_data_object)

        for attr in excepected_attrs:
            with self.subTest(f"expected attr: {attr}"):
                self.assertHasAttr(data, attr)

    def test_log_filename_method(self, directory=None):
        data = confighandler.ConfigData(self.ini_filename)
        expected_absolute = r"^\/"
        expected_extension = r".txt$"
        expected_desktop = r"\/Desktop\/"
        unexpected_pattern = r"\~"

        if directory:
            expected_user_dir = fr"\/{os.path.basename(directory)}\/"
            filename = data.log_filename(directory)
            # Default dir SHOULD NOT be leaf dirname
            self.assertNotRegex(filename, expected_desktop)
            self.assertRegex(filename, expected_user_dir)
        else:
            filename = data.log_filename()
            # Default dir expected as leaf dirname
            self.assertRegex(filename, expected_desktop)
        # Expect file to be absolute
        self.assertRegex(filename, expected_absolute)
        # Expect .txt file extension
        self.assertRegex(filename, expected_extension)
        # No "~" User directory notation expected
        self.assertNotRegex(filename, unexpected_pattern)

    def test_log_filename_method_with_user_directory(self):
        user_directory = os.path.dirname(__file__)
        self.test_log_filename_method(user_directory)


if __name__ == '__main__':
    unittest.main()
