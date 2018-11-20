#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module simplifies the importing of package modules within testsuites.

Though the top level folder is 'validation' it is not a package in its own
right: there is not validation.__init__.py.

validation.tests and validation.validator cannot 'see' eachother, they are each
packages in their own right and hence to let 'validator' beomce visible to
'tests' and hence 'unittest' itself sys.path has the validator package path
insterted.

This module is used during testing only and is imported by base_testcases,
however you can make use of it by importing it before importing
validator modules.

>>> import context
>>> import <some validator pkg module>

or

>>> from tests.base_testcases import ExtendedTestCase
>>> import <some validator pkg module>
"""


import sys
import os

TARGET_DIR = '../validator/'  # Relative to this file.
package_dir = os.path.join(os.path.dirname(__file__), TARGET_DIR)
if not os.path.isdir(package_dir):
    msg = f"Cannot perform tests, test suite cannot find '{package_dir}'"
    raise NotADirectoryError(msg)

sys.path.insert(0, os.path.abspath(package_dir))

if __name__ == '__main__':

    modulename = 'core'
    import core

    if modulename in sys.modules:
        print(f"""You have imported the '{modulename}' module.""")
