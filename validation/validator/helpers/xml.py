#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of XML functions and classes that validate xml.

Copyright Ian Vermes 2018
"""

import exceptions

from lxml import etree

import os
import enum

class OrderedEnum(enum.Enum):
    """An ordered enumeration that is not based on IntEnumself.

    From: https://docs.python.org/3/library/enum.html#orderedenum
    """
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Passing(OrderedEnum):
    """Enum for evaluating the various pass/failure validation states of XML.

    The Enum members allow comparison but do not otherwise behave like its.

    Class Methods:
        from_exception(Exception, None): Generate an Enum instance appropriate
            to the specific exception.
    """
    PASSING = 50
    RULES = 40
    SCHEMA = 30
    SYNTAX = 20
    FAILS = 10

    @classmethod
    def from_exception(cls, exc):
        """Generate an Enum instance appropriate to the specific exception.

        Args:
            exc(Exception, None)
        """
        exc_types = {type(None): 50,
                     exceptions.RuleValidationError: 40,
                     exceptions.SchemaValidationError: 30,
                     exceptions.SyntaxValidationError: 20,
                     exceptions.ValidationError: 10}
        value = exc_types[type(exc)]
        return Passing(value)


class ValidationResult(object):
    """Result object spawned by validation functions and methods.

    Validation by its nature raises exceptions, hence the result captures legal
    or expected exceptions.

    The result object is boolean, being True when there is no captured
    exception otherwise False when None. Hence True means XML is valid.

    It also exposed the detailed status of which validation implementations
    it has thus far passed (if any).

    Args:
        filename(str): XML filename.
        exception(Exception, None): Package validation errors or None if no
            exception was raised.

    Attrs:
        filename(string)
        exception(Exception, None): Exceptions are package validation error
            or None. The exception is explicit and hence has an implicit
            __cause__().
        passed_syntax(bool)
        passed_schema(bool)
        passed_rules(bool)
    """
    def __init__(self, filename, exc):
        self._filename = filename
        self._issuitable_exception(exc)
        self._exc = exc
        self._this_enum = Passing.from_exception(exc)

    def __bool__(self):
        flag = all([self.passed_syntax, self.passed_schema, self.passed_rules])
        return flag

    def _issuitable_exception(self, exc):
        suitable = isinstance(exc, (type(None), exceptions.ValidationError))
        if suitable:
            return
        else:
            name = self.__class__.__name__
            exc = repr(exc)
            msg = f"{name} accepts NoneType or ValidationError instances, got {exc}."
            raise TypeError(msg)

    @property
    def filename(self):
        return self._filename

    @property
    def exception(self):
        return self._exc

    @property
    def passed_syntax(self):
        flag = self._this_enum > Passing.SYNTAX
        return flag

    @property
    def passed_schema(self):
        flag = self._this_enum > Passing.SCHEMA
        return flag

    @property
    def passed_rules(self):
        flag = self._this_enum > Passing.RULES
        return flag

    def __repr__(self):
        address = hex(id(self))
        name = self.__class__.__name__
        detail = f"file: .../{os.path.basename(self.filename)}, exc: {repr(self.exception)}"
        string = f"<{name} object at {address} {detail}>"
        return string

    def __str__(self):
        return str(repr(self))


def validate_syntax(filename):
    try:
        try:
            etree.parse(filename)
        except etree.XMLSyntaxError as cause:
            raise exceptions.SyntaxValidationError() from cause
    except exceptions.SyntaxValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result
