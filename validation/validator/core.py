#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validator XML Core.

Validator of that incorporates XML Schema and Python techniques to ensure JJS
XML is both well formed, valid and sematicly correct.

Copyright Ian Vermes 2018
"""

import exceptions
import helpers

import os

CORE_SETTINGS_FILENAME = os.path.join(os.path.dirname(__file__),
                                      "CORE_SETTINGS.ini")


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


def main(directory, testmode=False):
    """Validate the XML in the directory and reporting on each."""
    # Set the mode depending on the main Kwargs.
    if testmode is True:
        mode = helpers.settings_handler.Mode.TEST
    elif testmode is False:
        mode = helpers.settings_handler.Mode.LIVE
    # Get the ini file, from an expected location OR failing that find it.
    ini_file = helpers.path.expandpath(CORE_SETTINGS_FILENAME, exists=True)
    settings = helpers.settings_handler.Settings(ini_file, mode=mode)

    # Create a settings singleton from the ini file.
    # Infer the log file output location from the given directory. # HUH WHAT DID I MEAN?
    # Generate a list of xml file paths to iterate over
    # Feed errors to an error parser that works with the log file
    # Parse the xml with lxml and the XSD
    # Perform examinations that are beyond the scope of XSD

    print(f"test mode: {settings.mode}")  # TODO remove one your integration tests are more fully written
    print("done!") # TODO remove one your integration tests are more fully written
    return


if __name__ == '__main__':
    parser = helpers.argparser.NextGenArgParse()
    args = parser.get_args(search_dirs=True)
    main(args.xmls, testmode=args.testmode)
