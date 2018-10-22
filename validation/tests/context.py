# -*- coding: utf-8 -*-

# Insert module directory into sys.path Use a simple (but explicit) path
# modification to resolve the package properly. I highly recommend the latter.
# Requiring a developer to run setup.py develop to test an actively changing
# codebase also requires them to have an isolated environment setup for each
# instance of the codebase.

import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import validator
