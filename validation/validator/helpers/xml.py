#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of XML functions and classes that validate xml.

Copyright Ian Vermes 2018
"""

import exceptions

import chardet
from lxml import etree

import os
import enum
import re
import itertools

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
    ENCODING = 15
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
                     exceptions.EncodingValidationError: 15,
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


class EncodingOperations(object):
    """A collection of operations for examining file encodingsself.

    Methods:
        get_detected_and_declared_encoding
        detect_file_encoding
        grep_declaration_encoding
    """

    @classmethod
    def get_detected_and_declared_encoding(cls, filename, return_declaration=False):
        """Get the 'chardet' detected encoding and the one in the delcaration.

        Get the file encoding by interpreting the bytestream and reading
        the XML declaration. Optionally also return the declaration.

        If the declaration lacks an encoding it will return as an empty string,

        Args:
            filname(str)
        Kwargs:
            return_declaration(bool): False by defaultself.

        Return:
            str, str
        or with kwarg
            str, str, str
        """
        with open(filename, "rb") as handle:
            raw_file = handle.read()
            handle.seek(0, 0)
            raw_line = handle.readline()

        dectected_enc = cls.detect_file_encoding(raw_file).lower()

        try:
            line = raw_line.decode(dectected_enc)
        except UnicodeDecodeError as too_strict_exc:
            line = raw_line.decode(dectected_enc, "replace")

        try:
            declared_enc = cls.grep_declaration_encoding(line)
        except exceptions.EncodingOperationError:
            declared_enc = ""
        except exceptions.UnexpectedDeclarationAbsent:
            raise
        else:
            declared_enc = declared_enc.lower()

        if return_declaration:
            return dectected_enc, declared_enc, line
        else:
            return dectected_enc, declared_enc

    @classmethod
    def detect_file_encoding(cls, raw_file):
        """Get the encoding by interpreting the file bytestream with chardetself.

        Args:
            raw_file(bytes): A single line or whole file read as bytes.
        Return:
            str
        """
        detected_enc = chardet.detect(raw_file)["encoding"]
        detected_enc = detected_enc.lower()
        if detected_enc == "ascii":
            prober = chardet.utf8prober.UTF8Prober()
            res = prober.feed(raw_file)
            replacement_enc = "utf-8"
            try:
                raw_file.decode(replacement_enc)
            except UnicodeDecodeError:
                pass
            else:
                detected_enc = replacement_enc
        return detected_enc

    @classmethod
    def grep_declaration_encoding(cls, string, strict=True):
        """Get the encoding substring from the declaration string.

        Args:
            string(str): First line of an XML file.
        Kwargs:
            strict(bool): If True, raise legal exception, otherwise return value is an empty string.
        Return:
            str
        Exceptions:
            exceptions.DeclarationHasNoEncoding (legal)
            exceptions.DeclarationEncodingEmptyString (legal)
            exceptions.DeclarationEncodingBadQuoteSyntax (legal)

            exceptions.DeclarationAbsent (illegal)
            ValueError (illegal)
        """
        # Is declaration?
        if "<?" not in string:
            msg = f"String does not resemble an XML declaration: {string}"
            raise exceptions.DeclarationAbsent(msg)

        pattern = r"""\s*(?:encoding\s*=\s*(?:\"|\'))(?:((?:\\"|[^"])|(?:\\'|[^'])|[^\s>]+)(?:\"|\'))?"""
        rgx = re.compile(pattern)
        result = []
        for match in rgx.finditer(string):
            groups = match.groups()
            if all(groups):
                result.append(groups)
        if not (0 < len(result) < 2):
            try:
                if "encoding" not in string:
                    msg = f"No 'encoding' attribute in declaration: {string}"
                    raise exceptions.DeclarationHasNoEncoding(msg)
                elif 'encoding=\"\"' in string or "encoding=\'\'" in string:
                    msg = f"Declaration 'encoding' attribute is an empty string: {string}"
                    raise exceptions.DeclarationEncodingEmptyString(msg)
                elif 'encoding=\"' in string or "encoding=\'" in string:
                    msg = f"Declaration 'encoding' attribute is malformed string: {string}"
                    raise exceptions.DeclarationEncodingBadQuoteSyntax(msg)
                else:
                    msg = f"Cannot grep the value of the 'encoding' attribute: {string}."
                    raise ValueError(msg)
            except exceptions.EncodingOperationError:
                if strict:
                    raise
                else:
                    value = ""
                    return value
            except ValueError:
                raise
        else:
            value = itertools.chain.from_iterable(result)
            value = list(value).pop()
            return value

MY_PARSER = etree.XMLParser(encoding=None)

def validate_syntax(filename):
    try:
        try:
            etree.parse(filename, parser=MY_PARSER)
        except etree.XMLSyntaxError as cause:
            raise exceptions.SyntaxValidationError() from cause
    except exceptions.SyntaxValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result


def validate_encoding(filename):
    get_encodings = EncodingOperations.get_detected_and_declared_encoding
    try:
        try:
            detected_enc, declared_enc = get_encodings(filename)
        except exceptions.EncodingOperationError as cause:
            msg = ""
            raise exceptions.EncodingValidationError(msg) from cause
        except exceptions.UnexpectedDeclarationAbsent as cause:
            msg = ""
            raise exceptions.EncodingValidationError(msg) from cause
        except ValueError as cause:
            msg = ""
            raise exceptions.EncodingValidationError(msg) from cause
        mismatched_encoding = (detected_enc != declared_enc)
        if mismatched_encoding:
            msg = ""
            cause = exceptions.EncodingOperationError()
            raise exceptions.EncodingValidationError(msg) from cause
    except exceptions.EncodingValidationError as exc:
        exception = exc
    else:
        exception = None
    result = ValidationResult(filename, exception)
    return result
