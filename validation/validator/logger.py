#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""This module captures the errors related to XML parsing or validation.

The purpose is to aid user review of XML and to know which files and where
within a file to make said correction.

Copyright Ian Vermes 2018
"""

class ErrorLogger(object):
    """Digests error stream objects and writes them to a log file.
    """

    def __init__(self, filename, error_stream):
        self.filename = filename
        self.stream = error_stream

    def listen(self):
        pass
