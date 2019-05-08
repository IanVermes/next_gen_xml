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
import exceptions

from lxml import etree


SETTINGS = get_settings()
SCHEMA = SETTINGS.schema


class SchemaOperations:
    pass


class validate_schema(object):

    def __new__(self, filename):
        return _validate_schema(filename)

    key = Passing.SCHEMA


def parse_xml(filename, *args, **kwargs):
    if isinstance(filename, etree._Element):
        tree = filename.getroottree()
    elif isinstance(filename, etree._ElementTree):
        tree = filename
    else:
        filename = str(filename)
        tree = etree.parse(filename, *args, **kwargs)
    return tree


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
