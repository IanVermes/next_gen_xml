#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of XML functions and classes that validate xml.

Copyright Ian Vermes 2018
"""

class ValidationResult(object):
    """Result object spawned by validation functions and methods.

    Attrs:
        filename
        exception
        passed_syntax
        passed_schema
        passed_rules
    """
    def __init__(self, filename, exc):
        self._filename = filename
        self._exc = exc

    @property
    def filename(self):
        return self._filename

def validate_syntax(filename):
    return bool(filename)
