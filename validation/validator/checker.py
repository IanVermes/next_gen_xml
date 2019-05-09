#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unifies the various checking modules and result module as a single class.

class:
    Checker

Copyright Ian Vermes 2019
"""

from helpers.checkschema import validate_schema
from helpers.checksyntax import validate_syntax
import exceptions

import os

class Checker():
    """Validate XML and generate reports on in valid XML.

    Methods:
        feed_in

    Attrs:
        validators
    """

    def __init__(self):
        validators = [validate_schema, validate_syntax]
        validators.sort()
        self.validators = tuple(validators)

    def feed_in(self, filename):
        if not os.path.isfile(filename):
            raise exceptions.FileNotFound(str(filename))
        else:
            for validation_func in self.validators:
                result = validation_func(filename)
                if not result:
                    break
            return result
