#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Validation results are objects spawned by validation classes and functions.

Copyright Ian Vermes 2019
"""


import exceptions
from helpers.enum import Passing

import os


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

    def __repr__(self):
        address = hex(id(self))
        name = self.__class__.__name__
        detail = (f"file: .../{os.path.basename(self.filename)}, "
                  f"exc: {repr(self.exception)}")
        string = f"<{name} object at {address} {detail}>"
        return string

    def __str__(self):
        return str(repr(self))

    def _issuitable_exception(self, exc):
        suitable = isinstance(exc, (type(None), exceptions.ValidationError))
        if suitable:
            return
        else:
            name = self.__class__.__name__
            exc = repr(exc)
            msg = (f"{name} accepts NoneType or ValidationError instances, "
                   f"got {exc}.")
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
