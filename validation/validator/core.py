#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validator XML Core.

Validator of that incorporates XML Schema and Python techniques to ensure JJS
XML is both well formed, valid and sematicly correct.

Copyright Ian Vermes 2018
"""

import os

CORE_SETTINGS_FILENAME = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "CORE_SETTINGS.ini"))


class NextGenError(Exception):
    """Base exception for this package."""


class _TestingPrimitive():
    """This class is used by the package's test suit for initial validation."""

    @classmethod
    def verify_import_tester(cls):
        """Confirms that the module has been imported."""
        return True

    @classmethod
    def raise_package_error(cls):
        """Confirms that the module has a base exception."""
        package_base_eror = NextGenError()
        raise package_base_eror



def main(directory):
    """Validate the XML in the directory and reporting on each."""
    # Read the ini file for log file default name
    # Infer the log file output location from the given directory
    # Generate a list of xml file paths to iterate over
    # Feed errors to an error parser that works with the log file
    # Parse the xml with lxml and the XSD
    # Perform examinations that are beyond the scope of XSD

    return

if __name__ == '__main__':
    print(f"ini: {CORE_SETTINGS_FILENAME}")
    print(f"isfile: {os.path.isfile(CORE_SETTINGS_FILENAME)}")
