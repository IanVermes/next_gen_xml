#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""Test the Passing enum

Copyright Ian Vermes 2019
"""
from tests.base_testcases import ExtendedTestCase
from helpers.enum import Passing

import random
import operator

class PassingEnumTest(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ordered = (Passing.FAILS,
                       Passing.ENCODING,
                       Passing.SYNTAX,
                       Passing.SCHEMA,
                       Passing.RULES,
                       Passing.PASSING)

    def test_enum_is_sortable(self):
        ordered = self.ordered

        randomised = list(ordered)
        random.shuffle(randomised)
        self.assertNotEqual(tuple(randomised), ordered, msg="Precondition.")

        randomised.sort()

        self.assertSequenceEqual(randomised, ordered)

    def test_order_of_enum(self):
        lt = operator.lt
        enums, enums_offset = self.ordered, self.ordered[1:]
        booleans = (lt(x, x_off) for x, x_off in zip(enums, enums_offset))

        self.assertTrue(all(booleans))
