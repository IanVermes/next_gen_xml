#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the various exceptions within the package.

Copyright Ian Vermes 2018
"""

from tests.basesuite import ExtendedTestCase
from validator import exceptions

import unittest


class HasBaseException(ExtendedTestCase):

    def test_base_exc(self):

        self.assertHasAttr(exceptions, attrname="NextGenError")

if __name__ == '__main__':
    unittest.main()
