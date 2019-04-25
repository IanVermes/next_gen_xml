#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A TestCase for XML validation that depends on resource files."""

import tests.base_testcases

import functools


class ValidationTestCase():

    def test_validator_passes_valid_files(self):
        self.fail("not written")

    def test_validator_fails_illegal_files(self):
        self.fail("not written")

    def test_validator_input_arg_does_not_raise_TypeError(self):
        self.fail("not written")

    @classmethod
    def preSetup(cls, directory, validator):
        pass

    @classmethod
    def get_resources(cls):
        pass

    @classmethod
    def get_valid_resources(cls):
        pass

    @classmethod
    def get_illegal_resources(cls):
        pass


def preSetupCheck(func):
    functools.wraps(func)
    def magic(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            raise
        return result
    return magic
