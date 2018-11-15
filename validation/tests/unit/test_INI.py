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
        cls.expected_sections = get_sections()

    def setUp(self):
        self.config = configparser.ConfigParser()

    def test_ini_file_is_readable(self):
        cfg = self.config

        try:
            cfg.read(self.ini_filename)
        except configparser.Error as err:
            self.fail(str(err))
        except Exception as err:
            raise err

    def test_ini_for_expected_categories(self):
        expected_sections = set(self.expected_sections)
        self.config.read(self.ini_filename)
        cfg = self.config

        actual_sections = set(cfg.sections())
        difference = expected_sections ^ actual_sections

        self.assertEqual(0, len(difference),
                         msg=f"INI has unepexcted sections: {difference}")

    def test_section_options_not_unique_to_that_section(self):
        self.config.read(self.ini_filename)
        cfg = self.config
        for this_section in cfg.sections():
            other_sections = (s for s in cfg.sections() if s != this_section)
            this_options = cfg.options(this_section)
            for other in other_sections:
                for option in this_options:
                    has_option = cfg.has_option(other, option)
                    self.assertTrue(has_option, msg=f"{this_section}.{option} not in {other} section.")


def get_sections():
    # Do dynamic import
    from validator.helpers import settings_handler
    modes = list(settings_handler.Mode)
    sections = [str(m) for m in modes]
    return sections


if __name__ == '__main__':
    unittest.main()
