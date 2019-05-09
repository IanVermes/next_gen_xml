#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XMLValidationTestCase test case.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import ExtendedTestCase
from tests.base_testcases import XMLValidationAbstractCase
from tests.base_testcases import FalseNegative, FalsePositive
import exceptions


import os
import unittest

REASON = "this test is to be deprecated - xml validation framework change"


class Test_BaseTestCase_AssertMethods_Strings(ExtendedTestCase):

    @classmethod
    def setUpClass(cls):
        cls.string = """Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa
qui officia deserunt mollit anim id est laborum.
"""
        cls.all_subs = ["Lorem", "ipsum", "consequat", "dolor", "Excepteur",
                        "esse", "in", "est", "voluptate"]
        cls.some_overlap_subs = ["Lorem", "ipsum", "consequat", "foobar",
                                 "pedestrian", "doctor", "toilet"]
        cls.no_subs = ["foobar", "George", "president", "light", "down",
                       "extinguish", "fishing", "articulate", "petty"]
        cls.method_in = cls.assertSubstringsInString
        cls.method_notin = cls.assertSubstringsNotInString

    def test_all_substrings_present(self):
        subs = self.all_subs

        # Test assert substrings IN string
        with self.subTest(method=self.method_in.__name__):
            self.method_in(substrings=subs, string=self.string)

        # Test assert substrings NOT IN string
        with self.subTest(method=self.method_notin.__name__):
            with self.assertRaises(AssertionError) as failure:
                self.method_notin(substrings=subs, string=self.string)
            # Assertion error message test
            err_msg_subs = list(map(lambda x: x.lower(), subs))
            err_msg_subs.append("unexpectedly present")
            self.assertSubstringsInString(substrings=err_msg_subs,
                                          string=str(failure.exception).lower(),
                                          msg=f"orginal: {str(failure.exception)}")

    def test_some_substrings_present(self):
        subs = self.some_overlap_subs
        not_in_count = 4
        subs_notin = [s.lower() for s in subs[-not_in_count:]]
        subs_in = [s.lower() for s in (set(subs) - set(subs_notin))]

        # Test assert substrings IN string
        with self.subTest(method=self.method_in.__name__):
            with self.assertRaises(AssertionError) as fail:
                self.method_in(substrings=subs, string=self.string)
            # Assertion error message test: setup
            err_msg_subs = subs_notin
            err_msg_subs.extend([f"{len(subs_in)}", f"{len(subs)}",
                                 "unexpectedly missing"])
            # Assertion error message test
            self.assertSubstringsInString(substrings=err_msg_subs,
                                          string=str(fail.exception).lower(),
                                          msg=f"orginal: {str(fail.exception)}")

        # Test assert substrings NOT IN string
        with self.subTest(method=self.method_notin.__name__):
            with self.assertRaises(AssertionError) as fail:
                self.method_notin(substrings=subs, string=self.string)
            # Assertion error message test: setup
            err_msg_subs = subs_in
            err_msg_subs.extend([f"{len(subs_notin)}", f"{len(subs)}",
                                 "unexpectedly present"])
            # Assertion error message test
            self.assertSubstringsInString(substrings=err_msg_subs,
                                          string=str(fail.exception).lower(),
                                          msg=f"orginal: {str(fail.exception)}")

    def test_no_substrings_present(self):
        subs = self.no_subs
        not_in_count = len(subs)
        subs_notin = [s.lower() for s in subs[-not_in_count:]]

        # Test assert substrings IN string
        with self.subTest(method=self.method_in.__name__):
            with self.assertRaises(AssertionError) as fail:
                self.method_in(substrings=subs, string=self.string)
            # Assertion error message test: setup
            err_msg_subs = subs_notin
            err_msg_subs.extend(["0", f"{len(subs)}", "unexpectedly missing"])
            # Assertion error message test
            self.assertSubstringsInString(substrings=err_msg_subs,
                                          string=str(fail.exception).lower(),
                                          msg=f"orginal: {str(fail.exception)}")

        # Test assert substrings NOT IN string
        with self.subTest(method=self.method_notin.__name__):
            self.method_notin(substrings=subs, string=self.string)

    def test_empty_substrings(self):
        subs = []

        with self.assertRaises(ValueError):
            self.method_in(substrings=subs, string=self.string)
        with self.assertRaises(ValueError):
            self.method_notin(substrings=subs, string=self.string)

    def test_string_not_list_as_substring(self):
        subs_present = "Lorem ipsum dolor"
        subs_absent = "This archaic concept"

        # Test assert substrings IN string
        with self.subTest(method=self.method_in.__name__):
            self.method_in(substrings=subs_present,
                           string=self.string)
            with self.assertRaises(AssertionError):
                self.method_in(substrings=subs_absent,
                               string=self.string)

        # Test assert substrings NOT IN string
        with self.subTest(method=self.method_notin.__name__):
            self.method_notin(substrings=subs_absent,
                              string=self.string)
            with self.assertRaises(AssertionError):
                self.method_notin(substrings=subs_present,
                                  string=self.string)

    def test_empty_string(self):
        subs = self.some_overlap_subs

        with self.assertRaises(ValueError):
            self.method_in(substrings=subs, string="")
        with self.assertRaises(ValueError):
            self.method_notin(substrings=subs, string="")


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
