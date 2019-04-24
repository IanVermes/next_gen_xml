#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML against a Schema doc.


Classes:
    SchemaOperations

Functions:
    validate_schema

Copyright Ian Vermes 2019
"""

from helpers.result import ValidationResult
from helpers.settings_handler import get_settings
import exceptions

from lxml import etree


SETTINGS = get_settings()
SCHEMA = SETTINGS.schema


class SchemaOperations:
    pass


def validate_schema(filename):
    try:
        try:
            tree = etree.parse(filename)
            SCHEMA.assertValid(tree)
        except etree.DocumentInvalid as cause:
            raise exceptions.SchemaValidationError() from cause
        except etree.XMLSyntaxError:
            # ignore - other validation functions handle this criteria
            pass
    except exceptions.SchemaValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result
