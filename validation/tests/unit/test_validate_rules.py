#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML pythonic-rules validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from helpers.checkrules import validate_rules
from helpers.enum import EncodingErrorCode
from helpers.result import ValidationResult

from lxml import etree

import exceptions

import unittest


if __name__ == '__main__':
    unittest.main()
