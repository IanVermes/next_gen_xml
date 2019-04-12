#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Unit test of the XML encoding subvalidator.

Copyright Ian Vermes 2018
"""

from tests.base_testcases import XMLValidationAbstractCase
from helpers.xml import handle_encoding_errors, EncodingOperations, EncodingErrorCode
from helpers.enum import EncodingErrorCode
import exceptions

from lxml import etree
import chardet

import os
import unittest
from itertools import chain


class TestSyntaxErrorEncodingHandler(XMLValidationAbstractCase):

    @classmethod
    def get_syntax_errors(cls, filename):
        try:
            etree.parse(filename, parser=cls.parser)
        except etree.XMLSyntaxError as exc:
            result = exc
        else:
            result = None
        return result

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parser = None
        cls.syntax_errors = {file: (properties, cls.get_syntax_errors(file)) for file, properties in cls.files.items()}

    def test_only_processes_syntax_errors(self):
        filename = "foobar.xml"
        exc = Exception("Generic Exception")

        with self.assertRaises(TypeError):
            handle_encoding_errors(filename, exc)

    def test_enum_accepts_syntax_exc_codes_or_None(self):
        enum_members = set(EncodingErrorCode)
        for file, (_, exc) in self.syntax_errors.items():
            exc_code = getattr(exc, "code", None)

            this_enum = EncodingErrorCode(exc_code)
            self.assertIn(this_enum, enum_members)

    def test_enum_values_are_not_arbitrary(self):
        exemptions = (0, 1000)
        iter_enum = (m for m in EncodingErrorCode
                             if min(exemptions) < m.value < max(exemptions))
        for member in iter_enum:
            with self.subTest(enum=repr(member)):

                err_name = etree.ErrorTypes._getName(member.value)

                self.assertEqual(err_name, member.name)

    def test_files_with_encoding_problems_have_non_zero_enum(self):
        for file, (properties, exc) in self.syntax_errors.items():
            has_encoding_problem = getattr(properties, "encoding")
            exc_code = exc_code = getattr(exc, "code", None)
            with self.subTest(code=exc_code, file=os.path.basename(file)):

                this_enum = EncodingErrorCode(exc_code)
                if has_encoding_problem:
                    self.assertGreater(this_enum, EncodingErrorCode.NOT_ENCODING_ERR)
                else:
                    self.assertEqual(this_enum, EncodingErrorCode.NOT_ENCODING_ERR)




class TestEncodingOperations(XMLValidationAbstractCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        criterion_1 = "encoding"
        criterion_2 = cls.valid_attr

        iter1 = cls.get_files_by_criterion(criterion_1)
        iter2 = cls.get_files_by_criterion(criterion_2)
        iters = [iter1, iter2]


        cls.encoding_files = {k: d for k, d in chain.from_iterable(iters)}

        is_ascii_1 = "illegal_syntax_declaration_encoding_mismatch_1.xml"
        is_ascii_2 = "valid.xml"
        cls.ascii_files = [f for f in cls.encoding_files
                                   if f.endswith(is_ascii_1) or f.endswith(is_ascii_2)]
        assert len(cls.ascii_files) == 2

    def test_grep_declaration_encoding(self, strict=True):
        declarations = {
                """<?xml version="1.0" encoding="utf-16"?>\r\n""": "utf-16",
                """<?xml version="1.0" encoding="utf-8"?>�""": "utf-8",
                """<?xml version="1.0" encoding=""?>""": "",
                '''<?xml version="1.0" encoding="?>\r\n''': "",
                """<?xml version="1.0" encoding="rabbit"?>\r\n""": "rabbit",
                """<?xml version="1.0"?>\n""": ""
                }
        func = EncodingOperations.grep_declaration_encoding
        for decl, expected_enc in declarations.items():
            with self.subTest(encoding=expected_enc):
                try:
                    result = func(decl, strict)
                except Exception as exc:
                    with self.assertRaises(exceptions.EncodingOperationError):
                        raise exc
                else:
                    self.assertEqual(result, expected_enc)

    def test_grep_declaration_encoding_supress_errors(self):
        strict = False
        self.test_grep_declaration_encoding(strict)

    def test_detect_file_encoding(self):
        for file in self.encoding_files:
            with open(file, "rb") as handle:
                raw_file = handle.read()
                expected = chardet.detect(raw_file)["encoding"].lower()
                if expected == "ascii":
                    expected = "utf-8"

            with self.subTest(file=os.path.basename(file)):
                assessed = EncodingOperations.detect_file_encoding(raw_file)
                self.assertEqual(expected, assessed)

    def test_detect_file_encoding_replace_ascii(self):
        for file in self.ascii_files:
            with open(file, "rb") as handle:
                raw_file = handle.read()
                expected = chardet.detect(raw_file)["encoding"].lower()
                self.assertEqual(expected, "ascii")

            with self.subTest(file=os.path.basename(file)):
                assessed = EncodingOperations.detect_file_encoding(raw_file)
                self.assertEqual(assessed, "utf-8")

    def test_get_detected_and_declared_encoding_can_identify_encodings(self):
        func = EncodingOperations.get_detected_and_declared_encoding
        for file in self.encoding_files:
            shortname = os.path.basename(file)

            with self.subTest(file=shortname):
                detected_enc, declared_enc = func(file)
                if "mismatch" in shortname:
                    self.assertNotEqual(detected_enc, declared_enc)

                elif "valid" in shortname:
                    self.assertEqual(detected_enc, declared_enc)

    def test_get_detected_and_declared_encoding_can_identify_validity(self):
        func = EncodingOperations.get_detected_and_declared_encoding
        for file, properties in self.encoding_files.items():
            shortname = os.path.basename(file)

            has_criterion = getattr(properties, "encoding")
            # valid files dont have the criterion in their filename
            if has_criterion:
                isValid = False
            else:
                isValid = True

            with self.subTest(file=shortname):
                detected_enc, declared_enc = func(file)
                assessment_flag = (detected_enc == declared_enc)

                self.assertEqual(isValid, assessment_flag)

if __name__ == '__main__':
    unittest.main()
