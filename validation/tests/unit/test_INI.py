#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of CORE_SETTINGS.ini

Copyright Ian Vermes 2018
"""

from tests.base_testcases import INIandSettingsTestCase

import unittest
import configparser
import glob
import os

INI_PARTIAL_NAME = "CORE_SETTINGS.ini"
PACKAGE_ROOT = '../..'
PACKAGE_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), PACKAGE_ROOT))
INI_SECTIONS = ('Log File', 'schema', 'xslt', 'Config Object Attributes')


class TestINIFindable(INIandSettingsTestCase):


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


class TestINIValues(INIandSettingsTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ini_filename = cls.find_and_get_path(
            INI_PARTIAL_NAME, PACKAGE_DIRECTORY)

    def test_ini_file_is_readable(self):
        _config = configparser.ConfigParser()

        try:
            _config.read(self.ini_filename)
        except configparser.Error as err:
            self.fail(str(err))
        except Exception as err:
            raise err

    def test_ini_for_expected_categories(self):
        expected_sections = set(INI_SECTIONS)
        _config = configparser.ConfigParser()
        _config.read(self.ini_filename)

        actual_sections = set(_config.sections())
        difference = expected_sections ^ actual_sections

        self.assertEqual(0, len(difference),
                         msg=f"INI has unepexcted sections: {difference}")


if __name__ == '__main__':
    unittest.main()
