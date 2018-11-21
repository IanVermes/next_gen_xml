#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML syntax validator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationTestCase

import os

class Test_XMLValidationTestCase_Itself(XMLValidationTestCase):
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


class TestSyntaxValidation(XMLValidationTestCase):

    def test_fail(self):
        self.fail("Not written.")
