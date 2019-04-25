#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions for validating XML against special rules.


Classes:
    SchemaOperations

Functions:
    validate_rules

Copyright Ian Vermes 2019
"""

from helpers.result import ValidationResult
import exceptions


def validate_rules(filename):
    exception = exceptions.RuleValidationError("Not yet written")
    return ValidationResult(filename, exception)
