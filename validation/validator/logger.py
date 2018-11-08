#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""This module captures the errors related to XML parsing or validation.

The purpose is to aid user review of XML and to know which files and where
within a file to make said correction.

Copyright Ian Vermes 2018
"""

import datetime
from functools import wraps


class ErrorLogger(object):
    """Digests error stream objects and writes them to a log file.

    args:
        filename(str)
        error_stream(queue.Queue)
    """

    def __init__(self, filename, error_stream):
        self.filename = filename
        self.stream = error_stream
        self.add_linebreak_packaging = "{}\n"

    def add_linebreak(func):
        """A decorator to add linebreaks to string returning functions."""
        @wraps(func)
        def magic(*args):
            packaging = "{}\n"
            return packaging.format(func(*args))
        return magic

    def listen(self):
        """Process the queued exceptions and log them as a headed section."""
        f = self._touch_file()
        try:
            f.write(self._generate_header())
            for i in range(self.stream.qsize()):
                error = self.stream.get()
                error_string = self._process_error(error)
                f.write(error_string)
            f.write(self._generate_tail())
        finally:
            f.close()

    def _touch_file(self):
        f = open(self.filename, mode='a+')
        return f

    @add_linebreak
    def _process_error(self, item):
        string = str(item)
        return string

    @add_linebreak
    def _generate_header(self):
        count = self.stream.qsize()
        timestamp = datetime.datetime.now().ctime()
        header = f"{timestamp}    Errors: {count}"
        return header

    @add_linebreak
    def _generate_tail(self):
        tail = "* * *"
        return tail
