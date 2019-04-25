#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XMLValidationTestCase test case.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationAbstractCase
from tests.base_testcases import FalseNegative, FalsePositive
import exceptions


import os
import unittest

REASON = "this test is to be deprecated - xml validation framework change"

@unittest.skip(REASON)
class Test_XMLValidationTestCase_Itself(XMLValidationAbstractCase):
    """This TestCase has a complicated setUpClass method and needs vetting."""

    def test_setupClass_files(self):
        for file, properties in self.files.items():
            with self.subTest(name=os.path.basename(file)):

                # Test1 - a file is valid or invalid, not both.
                valid_flag = getattr(properties, self.valid_attr)
                invalid_flag = getattr(properties, self.invalid_attr)

                self.assertNotEqual(valid_flag, invalid_flag)

                # Test2 - other property attributes should dictate valid/invald.
                isTrue = 0
                dict_props = properties._asdict()
                for attr, value in dict_props.items():
                    if attr in (self.invalid_attr, self.valid_attr):
                        continue
                    else:
                        if value is True:
                            isTrue += 1
                        elif value is False:
                            pass
                        else:
                            msg = f"Not boolean {file}.{attr}: {repr(value)}"
                            raise TypeError(msg)
                invalid_property_flags = bool(isTrue)

                if valid_flag is True:
                    msg = f"{properties}"
                    self.assertFalse(invalid_property_flags, msg)
                elif invalid_flag is True:
                    msg = f"{properties}"
                    self.assertTrue(invalid_property_flags, msg)

    def test_falsePosNegAssertionFunc(self):
        values = self.files
        criterion = self.valid_attr

        def blackbox(filename):
            "Example validator-like function"
            filename = os.path.basename(filename)
            flag = criterion.lower() in filename.lower()
            return flag

        kwargs = {"criterion": criterion,
                  "validator": blackbox,
                  "permitted_exceptions": exceptions.NextGenError}

        counter_FN = 0
        counter_FP = 0
        counter_pass = 0
        for k, v in values.items():
            val = {k: v}

            try:
                self.assertNoFalsePositivesOrNegatives(val, propogate=True, **kwargs)
            except FalseNegative:
                counter_FN += 1
            except FalsePositive:
                counter_FP += 1
            else:
                counter_pass += 1

        self.assertEqual(counter_pass, len(values))
        self.assertEqual(counter_FN, 0)
        self.assertEqual(counter_FP, 0)

    def test_falsePosNegAssertionFunc_catch_falsePos(self):
        values = self.files
        criterion = self.valid_attr

        def blackbox_introduce_falsepositives(filename):
            "Falsepositive introduced due to 'valid' in absolute filename"
            flag = criterion.lower() in filename.lower()  # Bad code
            return flag

        kwargs = {"criterion": criterion,
                  "validator": blackbox_introduce_falsepositives,
                  "permitted_exceptions": exceptions.NextGenError}

        counter_FN = 0
        counter_FP = 0
        counter_pass = 0
        for k, v in values.items():
            val = {k: v}

            try:
                self.assertNoFalsePositivesOrNegatives(val, propogate=True, **kwargs)
            except FalseNegative:
                counter_FN += 1
            except FalsePositive:
                counter_FP += 1
            else:
                counter_pass += 1

        self.assertEqual(counter_pass, 3)
        self.assertEqual(counter_FN, 0)
        self.assertEqual(counter_FP, 43)

    def test_falsePosNegAssertionFunc_catch_falseNeg(self):
        values = self.files
        criterion = self.invalid_attr

        def blackbox_introduce_falsenegatives(filename):
            "Falsenegative thrown by unexpected error."
            filename = os.path.basename(filename)
            flag = criterion.lower() in filename.lower()
            if "valid" in filename:
                raise ValueError("Test Foo")
            return flag

        kwargs = {"criterion": criterion,
                  "validator": blackbox_introduce_falsenegatives,
                  "permitted_exceptions": exceptions.NextGenError}

        counter_FN = 0
        counter_FP = 0
        counter_pass = 0
        for k, v in values.items():
            val = {k: v}

            try:
                self.assertNoFalsePositivesOrNegatives(val, propogate=True, **kwargs)
            except FalseNegative:
                counter_FN += 1
            except FalsePositive:
                counter_FP += 1
            else:
                counter_pass += 1

        self.assertEqual(counter_pass, 43)
        self.assertEqual(counter_FN, 3)
        self.assertEqual(counter_FP, 0)

    def test_falsePosNegAssertionFunc_permit_known_exc(self):
        values = self.files
        criterion = self.invalid_attr

        def blackbox_introduce_falsenegatives(filename):
            "Falsenegative forgiven due to permitted error"
            filename = os.path.basename(filename)
            flag = criterion.lower() in filename.lower()
            if "valid" in filename:
                raise exceptions.NextGenError("Test Foo")
            return flag

        kwargs = {"criterion": criterion,
                  "validator": blackbox_introduce_falsenegatives,
                  "permitted_exceptions": exceptions.NextGenError}

        counter_FN = 0
        counter_FP = 0
        counter_pass = 0
        for k, v in values.items():
            val = {k: v}

            try:
                self.assertNoFalsePositivesOrNegatives(val, propogate=True, **kwargs)
            except FalseNegative:
                counter_FN += 1
            except FalsePositive:
                counter_FP += 1
            else:
                counter_pass += 1

        self.assertEqual(counter_pass, 46)
        self.assertEqual(counter_FN, 0)
        self.assertEqual(counter_FP, 0)


if __name__ == '__main__':
    unittest.main()
