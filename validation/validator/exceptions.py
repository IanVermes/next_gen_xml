#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validator XML Exception.

Validator of that incorporates XML Schema and Python techniques to ensure JJS
XML is both well formed, valid and sematicly correct.

Copyright Ian Vermes 2018
"""


class NextGenError(Exception):
    """Base exception for this package."""


class FileNotFound(NextGenError):
    """Could not find a file within the filesystem."""


class DirNotFound(NextGenError):
    """Could not find a directory within the filesystem."""


class ParentDirNotFound(DirNotFound):
    """Could not find a parent directory of file in the filesystem."""


class UnnaceptableDirName(DirNotFound):
    """Cannot use empty string '' as local directory name, use './' instead."""


class UnexpectedEnum(NextGenError):
    """Enum is not valid."""


class ValidationError(NextGenError):
    """Base exception for XML validation."""


class SyntaxValidationError(ValidationError):
    """Validation error raised due to XML syntax errors."""


class SchemaValidationError(ValidationError):
    """Validation error raised due to XML failing against a Schema."""


class RuleValidationError(ValidationError):
    """Validation error raised due to XML failing bespoke Python rules."""
