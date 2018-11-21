#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase

import os


class TestSyntaxValidation(XMLValidationTestCase):

    def test_fail(self):
        self.fail("Not written.")
