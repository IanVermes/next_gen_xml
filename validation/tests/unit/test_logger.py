#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the error logger that handles XML parsing results.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
import logger  # from validator import logger

import unittest
import os
import queue


class TestLoggerObject(ExtendedTestCase):

    def test_logger_instantiation(self):
        path_to_write_log = ""
        error_stream = []

        try:
            logger.ErrorLogger(path_to_write_log, error_stream)
        except Exception as err:
            self.fail(f"Could not instantiate Logger: {str(err)}")


class TestLoggerObjectFunctionality(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.log_dir = ("/Users/Ian/Google Drive/code/next_gen_xml"
                       "/validation/tests/logs")
        cls.log_basename = "test_logger.txt"
        cls.log_filename = os.path.join(cls.log_dir, cls.log_basename)
        cls.error_stream_contents = (
            "first", "foo", "bar", "ben", "bat", "last")
        # Flag for tearDown
        cls.rmrf_log_dir = False

    def setUp(self):
        self.error_stream = queue.Queue()
        _ = [self.error_stream.put(e) for e in self.error_stream_contents]
        self.logger = logger.ErrorLogger(self.log_filename, self.error_stream)

    def tearDown(self):
        # Clear directory
        if not self.rmrf_log_dir:
            return
        assert self.log_dir != r"/"
        for root, dirs, files in os.walk(self.log_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_logger_makes_one_file(self):
        self.logger.listen()
        self.logger.listen()

        has_file = os.path.isfile(self.log_filename)
        file_count = len([f for f in os.listdir(self.log_dir) if not f.startswith(".")])  # Ignore 'invisible' files.

        self.assertTrue(has_file)
        self.assertEqual(1, file_count, msg=f"Files: {os.listdir(self.log_dir)}")


if __name__ == '__main__':
    unittest.main()
