#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML pythonic-rules validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase


class TestRuledValidation(XMLValidationTestCase):

    def test_fail(self):
        self.fail("Not written.")
