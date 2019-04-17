#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Collects arguments from the commandline for validated entry into the package.

Copyright Ian Vermes 2018
"""

from argparse import ArgumentParser, ArgumentTypeError

import os
import pathlib


class NextGenArgParse(object):
    """Process the command line args for the purposes of satisfying core.main().

    The interface for the program allows multiple positional arguments and an
    optional mode flag. The positional arguments should be file or directory
    paths.

    The file paths should be XML files, though the .xml file extension is not
    essential.

    The directory path should contain XML files with .xml file extensions at the
    next directory level. The search for .xml files is not recursive and hence
    will not search through subdirectories.

    Usage:

    >>> from argparse import ArgumentParser, ArgumentTypeError
    >>> argparser = NextGenArgParse()
    >>> kwargs = argparser.get_args()
    """

    GLOB_PATTERN = "*.xml"

    @classmethod
    def is_valid_path(cls, filename):
        """Validate that the file or directory exists and not just a string."""
        filepath = pathlib.Path(filename)
        if filepath.exists():
            if filepath.is_dir():
                xmls = list(filepath.glob(cls.GLOB_PATTERN))
                if len(xmls) > 0:
                    return_obj = filepath
                else:
                    msg = (f"Got a directory '{str(filepath)}' which does not "
                           "contain any files that match the "
                           f"'{cls.GLOB_PATTERN}' pattern.")
                    return_obj = ArgumentTypeError(msg)
            elif filepath.is_file():
                if filepath.suffix in cls.GLOB_PATTERN:
                    return_obj = filepath
                else:
                    msg = (f"Got a file '{str(filepath)}' which does not "
                           f"satisfy the '{cls.GLOB_PATTERN}' pattern.")
                    return_obj = ArgumentTypeError(msg)
            else:
                return_obj = TypeError(filepath)
        else:
            msg = f"Got the path '{filepath}' but it does not exist."
            raise ArgumentTypeError(msg)

        if isinstance(return_obj, Exception):
            raise return_obj
        else:
            return return_obj

    def _make_parser(self):
        description = 'Validate XML in a directory against a schema and python encoded rules.'
        parser = ArgumentParser(description=description)
        parser.add_argument("xmls",
                            metavar="PATHS",
                            nargs="*",
                            type=lambda x: self.is_valid_path(x),
                            help=("Multiple positional arguments that consist of file or directory paths."
                                  "\n  Directory paths will be searched for XML."
                                  "\n  File paths must have .xml file extensions."))
        parser.add_argument("-t", "--test",
                            dest='testmode',
                            action='store_true',
                            help="If provided run in testmode")
        return parser

    def get_args(self):
        """Get the argument object parsed from the command line args."""
        parser = self._make_parser()
        args = parser.parse_args()
        return args
