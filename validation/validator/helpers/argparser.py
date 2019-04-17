#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Collects arguments from the commandline for validated entry into the package.

Copyright Ian Vermes 2018
"""

import argparse as py_argparse

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
    """

    GLOB_PATTERN = "*.xml"

    @classmethod
    def searchdirectory(cls, filename):
        """Search a directory and retrieve xml files within."""
        path = pathlib.Path(filename)
        files = list(path.glob(cls.GLOB_PATTERN))
        return files

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
                    return_obj = py_argparse.ArgumentTypeError(msg)
            elif filepath.is_file():
                if filepath.suffix in cls.GLOB_PATTERN:
                    return_obj = filepath
                else:
                    msg = (f"Got a file '{str(filepath)}' which does not "
                           f"satisfy the '{cls.GLOB_PATTERN}' pattern.")
                    return_obj = py_argparse.ArgumentTypeError(msg)
            else:
                return_obj = TypeError(filepath)
        else:
            msg = f"Got the path '{filepath}' but it does not exist."
            raise py_argparse.ArgumentTypeError(msg)

        if isinstance(return_obj, Exception):
            raise return_obj
        else:
            return return_obj

    def _make_parser(self):
        description = 'Validate XML in a directory against a schema and python encoded rules.'
        parser = py_argparse.ArgumentParser(description=description)
        parser.add_argument("xmls",
                            metavar="PATHS",
                            nargs="+",
                            type=lambda x: self.is_valid_path(x),
                            help=("Multiple positional arguments that consist of file or directory paths."
                                  "\n  Directory paths will be searched for XML."
                                  "\n  File paths must have .xml file extensions."))
        parser.add_argument("-t", "--test",
                            dest='testmode',
                            action='store_true',
                            help="If provided run in testmode")
        return parser

    def get_args(self, search_dirs=True):
        """Get the argument object parsed from the command line args.

        kwargs:
            search_dirs (bool): By default, directory positional arguments are
                replaced with a series of XML files found within the directory.
                Otherwise the directory will be left untouched.
        return:
            argparse.Namespace
        """
        parser = self._make_parser()
        args = parser.parse_args()
        if search_dirs:
            # Add files to a new list, clear and replace the original list.
            new_list = []
            for path in args.xmls:
                if path.is_dir():
                    files = self.searchdirectory(path)
                    new_list.extend(files)
                elif path.is_file():
                    new_list.append(path)
            args.xmls.clear()
            for path in new_list:
                args.xmls.append(path)
            return args
        else:
            return args


if __name__ == '__main__':
    import sys
    print("This is a visual test of this module.")
    MSG_RAWARGS = (f"You called this script with these args:\n  {sys.argv}")
    parser = NextGenArgParse()
    args = parser.get_args()
    MSG_PROCESSED = (f"The processed args are:\n  {vars(args)}")
    print(MSG_RAWARGS)
