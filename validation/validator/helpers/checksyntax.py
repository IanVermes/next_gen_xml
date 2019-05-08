#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML syntax.


Classes:
    EncodingOperations

Copyright Ian Vermes 2018
"""

from helpers.result import ValidationResult
import exceptions

import chardet
from lxml import etree

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