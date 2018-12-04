#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML pythonic-rules validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidation
import exceptions

import unittest


class TestRuledValidation(XMLValidation.TestCase):

    @unittest.expectedFailure
    def test_fail(self):
        self.fail("Not written.")


if __name__ == '__main__':
    unittest.main()
