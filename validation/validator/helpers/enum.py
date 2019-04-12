#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""This package uses enums for a variety of uses:
* Describing the validity of an XML in greater detail than True or False
*

Classes:
    OrderedEnum
    Passing

Copyright Ian Vermes 2019
"""

import exceptions

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
