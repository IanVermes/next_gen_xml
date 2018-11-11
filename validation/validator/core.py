#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validator XML Core.

Validator of that incorporates XML Schema and Python techniques to ensure JJS
XML is both well formed, valid and sematicly correct.

Copyright Ian Vermes 2018
"""

try:
    import exceptions
except ModuleNotFoundError:
    # Arises from calling: $ python -m unittest
    try:
        from validator import exceptions
    except ModuleNotFoundError:
        raise

import os
import argparse

CORE_SETTINGS_FILENAME = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "CORE_SETTINGS.ini"))


class _TestingPrimitive():
    """This class is used by the package's test suit for initial validation."""

    @classmethod
    def verify_import_tester(cls):
        """Confirms that the module has been imported."""
        return True

    @classmethod
    def raise_package_error(cls):
        """Confirms that the module has a base exception."""
        package_base_eror = exceptions.NextGenError()
        raise package_base_eror


class NextGenArgParse(object):
    """Process the command line args for the purposes of satisfying main()."""

    @staticmethod
    def is_valid_directory(dir):
        """Validate that the directory is genuine not just a string."""
        if not os.path.isdir(dir):
            msg = f"The directory '{dir}' does not exist!"
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir

    def _make_parser(self):
        description = 'Validate XML in a directory against a schema and python encoded rules.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("directory",
                            metavar="DIR",
                            type=lambda x: self.is_valid_directory(x),
                            help="the directory for the program to process")
        return parser

    def get_args(self):
        """Get the argument object parsed from the command line args."""
        parser = self._make_parser()
        args = parser.parse_args()
        return args


def main(directory):
    """Validate the XML in the directory and reporting on each."""
    # Read the ini file for log file default name
    # Infer the log file output location from the given directory
    # Generate a list of xml file paths to iterate over
    # Feed errors to an error parser that works with the log file
    # Parse the xml with lxml and the XSD
    # Perform examinations that are beyond the scope of XSD

    print("done!")
    return


if __name__ == '__main__':
    argparser = NextGenArgParse()
    args = argparser.get_args()
    main(args.directory)
