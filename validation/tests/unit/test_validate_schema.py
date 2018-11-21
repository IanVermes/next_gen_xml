#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML schema validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase


class TestSchemaValidation(XMLValidationTestCase):

    def test_fail(self):
        self.fail("Not written.")
