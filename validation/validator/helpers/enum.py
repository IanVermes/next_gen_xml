#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""This package uses enums for a variety of uses:
* Mode: Software mode.
* Passing: Describes the validity of XML in greater detail than True or False
* Check: On-disk file state
* EncodingError: EncodingError <-> etree.XMLParser error codes relationship

Classes:
    Mode
    Check
    Passing
    EncodingErrorCode

Base classes:
    OrderedEnum

Copyright Ian Vermes 2019
"""

import exceptions

import enum


class Mode(enum.Enum):
    """An enumeration of the software environment/mode."""
    LIVE = 1
    TEST = 2

    @classmethod
    def get_default(cls):
        return cls.LIVE


class Check(enum.Enum):
    """An Enum used in validation of fileo peration."""
    DONT = 1
    EXISTS = 2
    PARENT_ONLY = 3
    # Permsissions?


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


class EncodingErrorCode(OrderedEnum):
    NOT_ENCODING_ERR = 0
    ERR_DOCUMENT_EMPTY = 4
    ERR_UNKNOWN_ENCODING = 31
    ERR_UNSUPPORTED_ENCODING = 32
    ERR_ENCODING_NAME = 79
    ERR_INVALID_ENCODING = 81
    ERR_MISSING_ENCODING = 101

    @classmethod
    def _missing_(cls, value):
        default = 0
        for item in cls:
            if item.value == value:
                return item
            else:
                return cls(default)
