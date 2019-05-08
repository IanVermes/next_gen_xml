#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML encoding.


Classes:
    EncodingOperations

Copyright Ian Vermes 2018
"""

from helpers.result import ValidationResult
import exceptions

import chardet
from lxml import etree

import os
import enum
import re
import itertools


class EncodingOperations(object):
    """A collection of operations for examining file encodingsself.

    Methods:
        get_detected_and_declared_encoding
        detect_file_encoding
        grep_declaration_encoding
    """

    @classmethod
    def get_detected_and_declared_encoding(cls, filename, return_declaration=False):
        """Get the 'chardet' detected encoding and the one in the delcaration.

        Get the file encoding by interpreting the bytestream and reading
        the XML declaration. Optionally also return the declaration.

        If the declaration lacks an encoding it will return as an empty string,

        Args:
            filname(str)
        Kwargs:
            return_declaration(bool): False by defaultself.

        Return:
            str, str
        or with kwarg
            str, str, str
        """
        with open(filename, "rb") as handle:
            raw_file = handle.read()
            handle.seek(0, 0)
            raw_line = handle.readline()

        dectected_enc = cls.detect_file_encoding(raw_file).lower()

        try:
            line = raw_line.decode(dectected_enc)
        except UnicodeDecodeError as too_strict_exc:
            line = raw_line.decode(dectected_enc, "replace")

        try:
            declared_enc = cls.grep_declaration_encoding(line)
        except exceptions.EncodingOperationError:
            declared_enc = ""
        except exceptions.UnexpectedDeclarationAbsent:
            raise
        else:
            declared_enc = declared_enc.lower()

        if return_declaration:
            return dectected_enc, declared_enc, line
        else:
            return dectected_enc, declared_enc

    @classmethod
    def detect_file_encoding(cls, raw_file):
        """Get the encoding by interpreting the file bytestream with chardetself.

        Args:
            raw_file(bytes): A single line or whole file read as bytes.
        Return:
            str
        """
        detected_enc = chardet.detect(raw_file)["encoding"]
        detected_enc = detected_enc.lower()
        if detected_enc == "ascii":
            prober = chardet.utf8prober.UTF8Prober()
            res = prober.feed(raw_file)
            replacement_enc = "utf-8"
            try:
                raw_file.decode(replacement_enc)
            except UnicodeDecodeError:
                pass
            else:
                detected_enc = replacement_enc
        return detected_enc

    @classmethod
    def grep_declaration_encoding(cls, string, strict=True):
        """Get the encoding substring from the declaration string.

        Args:
            string(str): First line of an XML file.
        Kwargs:
            strict(bool): If True, raise legal exception, otherwise return value is an empty string.
        Return:
            str
        Exceptions:
            exceptions.DeclarationHasNoEncoding (legal)
            exceptions.DeclarationEncodingEmptyString (legal)
            exceptions.DeclarationEncodingBadQuoteSyntax (legal)

            exceptions.DeclarationAbsent (illegal)
            ValueError (illegal)
        """
        # Is declaration?
        if "<?" not in string:
            msg = f"String does not resemble an XML declaration: {string}"
            raise exceptions.DeclarationAbsent(msg)

        pattern = r"""\s*(?:encoding\s*=\s*(?:\"|\'))(?:((?:\\"|[^"])|(?:\\'|[^'])|[^\s>]+)(?:\"|\'))?"""
        rgx = re.compile(pattern)
        result = []
        for match in rgx.finditer(string):
            groups = match.groups()
            if all(groups):
                result.append(groups)
        if not (0 < len(result) < 2):
            try:
                if "encoding" not in string:
                    msg = f"No 'encoding' attribute in declaration: {string}"
                    raise exceptions.DeclarationHasNoEncoding(msg)
                elif 'encoding=\"\"' in string or "encoding=\'\'" in string:
                    msg = f"Declaration 'encoding' attribute is an empty string: {string}"
                    raise exceptions.DeclarationEncodingEmptyString(msg)
                elif 'encoding=\"' in string or "encoding=\'" in string:
                    msg = f"Declaration 'encoding' attribute is malformed string: {string}"
                    raise exceptions.DeclarationEncodingBadQuoteSyntax(msg)
                else:
                    msg = f"Cannot grep the value of the 'encoding' attribute: {string}."
                    raise ValueError(msg)
            except exceptions.EncodingOperationError:
                if strict:
                    raise
                else:
                    value = ""
                    return value
            except ValueError:
                raise
        else:
            value = itertools.chain.from_iterable(result)
            value = list(value).pop()
            return value

MY_PARSER = etree.XMLParser(encoding=None)

def validate_syntax(filename):
    try:
        causalgrp = (etree.XMLSyntaxError, exceptions.EncodingOperationError)
        try:
            etree.parse(str(filename), parser=MY_PARSER)
            # Files with mismatched encodings may silently pass without raising
            # an exception.
            raise_if_mismatched_encodings(filename)
        except causalgrp as cause:
            raise exceptions.SyntaxValidationError() from cause
    except exceptions.SyntaxValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result


def raise_if_mismatched_encodings(filename):
    """Raises an exceptions if the zeroth line encoding & rest of file mismatch.

    Exceptions:
        exceptions.EncodingOperationError
    """
    key = "encoding"
    with open(filename, "rb") as handle:
        # Get zeroth line encoding
        line = handle.readline()
        zeroth_enc = chardet.detect(line)[key]
        # Get encoding of the rest of the file.
        detector = chardet.UniversalDetector()
        for line in handle:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        rest_enc = detector.result[key]

    if zeroth_enc != rest_enc:
        msg = ("The file encoding in the declaration and the encoding differ: "
               "zeroth line={zeroth_enc} & other liens={rest_enc}.")
        raise exceptions.EncodingOperationError(msg)
