#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Collects arguments from the commandline for validated entry into the package.

Copyright Ian Vermes 2018
"""

import argparse
import os


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
