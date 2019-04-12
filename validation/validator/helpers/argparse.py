#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Collects arguments from the commandline for validated entry into the package.

Copyright Ian Vermes 2018
"""

from argparse import ArgumentParser, ArgumentTypeError

import os


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

    @staticmethod
    def is_valid_directory(dir):
        """Validate that the directory is genuine not just a string."""
        return_obj = ""
        if os.path.exists(dir):
            if os.path.isdir(dir):
                return_obj = dir
            elif os.path.isfile(dir):
                msg = f"Expected a directory not file, got '{dir}'."
                return_obj = ArgumentTypeError(msg)
            else:
                return_obj = TypeError(dir)
        else:
            msg = f"The location '{dir}' does not exist!"
            raise ArgumentTypeError(msg)

        if isinstance(return_obj, Exception):
            raise return_obj
        else:
            return return_obj

    def _make_parser(self):
        description = 'Validate XML in a directory against a schema and python encoded rules.'
        parser = ArgumentParser(description=description)
        parser.add_argument("directory",
                            metavar="DIR",
                            type=lambda x: self.is_valid_directory(x),
                            help="the directory for the program to process.")
        parser.add_argument("-t", "--test",
                            dest='testmode',
                            action='store_true',
                            help="if provided run in testmode")
        return parser

    def get_args(self):
        """Get the argument object parsed from the command line args."""
        parser = self._make_parser()
        args = parser.parse_args()
        return args
