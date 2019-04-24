#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML against a Schema doc.


Classes:
    SchemaOperations

Functions:
    validate_schema

Copyright Ian Vermes 2019
"""

from helpers.settings_handler import get_settings

from lxml import etree


SETTINGS = get_settings()
SCHEMA = SETTINGS.schema


class SchemaOperations:
    pass


def validate_schema(file):
    return None
