#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML against a Schema doc.


Classes:
    SchemaOperations
    validate_schema

Copyright Ian Vermes 2019
"""

from helpers.result import ValidationResult
from helpers.settings_handler import get_settings
from helpers.enum import Passing
from helpers._check_shared import SortableCallable, parse_xml
import exceptions

from lxml import etree


SETTINGS = get_settings()
SCHEMA = SETTINGS.schema


class SchemaOperations:
    pass


class validate_schema(metaclass=SortableCallable):
    """Check that an XML file is valid against the schema file.

    Precondition: The schema file location is set in the package config file.

    Attr:
        key(Passing enum): This is a sortable function-like class.
    Arg:
        filename(str, pathlib.Path)
    Return:
        ValdiationResult
    """

    key = Passing.SCHEMA

    @classmethod
    def _veneer(cls, filename):
        return _validate_schema(filename)


def _validate_schema(filename):
    try:
        try:
            tree = parse_xml(filename)
            SCHEMA.assertValid(tree)
        except etree.DocumentInvalid as cause:
            raise exceptions.SchemaValidationError() from cause
    except exceptions.SchemaValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result
