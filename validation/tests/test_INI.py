#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of CORE_SETTINGS.ini

Copyright Ian Vermes 2018
"""

from .basesuite import ExtendedTestCase

import unittest
import configparser
import glob
import os

INI_PARTIAL_NAME = "CORE_SETTINGS.ini"
PACKAGE_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))


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
        cls.package_directory = PACKAGE_DIRECTORY
        cls.ini_filename = TestINIFindable.find_and_get_path(
            "CORE_SETTINGS.ini", cls.package_directory)

    def test_inin_file_is_readable(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.ini_filename)
        except configparser.Error as err:
            self.fail(str(err))
        except Exception as err:
            raise err


if __name__ == '__main__':
    unittest.main()
