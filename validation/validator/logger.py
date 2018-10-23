#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""This module captures the errors related to XML parsing or validation.

The purpose is to aid user review of XML and to know which files and where
within a file to make said correction.

Copyright Ian Vermes 2018
"""

import datetime

class ErrorLogger(object):
    """Digests error stream objects and writes them to a log file.
    args:
        filename(str)
        error_stream(queue.Queue)
    """

    def __init__(self, filename, error_stream):
        self.filename = filename
        self.stream = error_stream

    def listen(self):
        f = self._make_log()

        f.write(self._generate_header())
        for i in range(self.stream.qsize()):
            item = self.stream.get()
            string = self._process_item(item)
            f.write(string)
        f.write(self._generate_tail())

        f.close()

    def _make_log(self):
        f = open(self.filename, mode='a+')
        return f

    def _process_item(self, item):
        string = str(item)
        return self._format_string(string)

    def _format_string(self, string):
        packaging = "{}\n"
        return packaging.format(string)

    def _generate_header(self):
        count = self.stream.qsize()
        timestamp = datetime.datetime.now().ctime()
        header = f"{timestamp}    Errors: {count}"
        return self._format_string(header)

    def _generate_tail(self):
        tail = "* * *"
        return self._format_string(tail)
