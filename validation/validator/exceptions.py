#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validator XML Exception.

Validator of that incorporates XML Schema and Python techniques to ensure JJS
XML is both well formed, valid and sematicly correct.

Copyright Ian Vermes 2018
"""


class NextGenError(Exception):
    """Base exception for this package."""

# File operations

class FileNotFound(NextGenError):
    """Could not find a file within the filesystem."""


class DirNotFound(NextGenError):
    """Could not find a directory within the filesystem."""


class ParentDirNotFound(DirNotFound):
    """Could not find a parent directory of file in the filesystem."""


class UnnaceptableDirName(DirNotFound):
    """Cannot use empty string '' as local directory name, use './' instead."""

# Enum operations

class UnexpectedEnum(NextGenError):
    """Enum is not valid."""

# Encoding operations

class UnexpectedDeclarationAbsent(NextGenError):
    """XML declaration is missing."""

class EncodingOperationError(NextGenError):
    """Base error for the EncodingOperations class."""


class DeclarationEncodingEmptyString(EncodingOperationError):
    """XML declaration has an encoding attribute but its value is empty."""


class DeclarationEncodingBadQuoteSyntax(EncodingOperationError):
    """XML declaration has an encoding attribute with a syntax error."""


class DeclarationHasNoEncoding(EncodingOperationError):
    """XML declaration has no encoding attribute."""

# Validation operations

class ValidationError(NextGenError):
    """Base exception for XML validation."""


class SyntaxValidationError(ValidationError):
    """Validation error raised due to XML syntax errors."""


class SchemaValidationError(ValidationError):
    """Validation error raised due to XML failing against a Schema."""


class RuleValidationError(ValidationError):
    """Validation error raised due to XML failing bespoke Python rules."""
