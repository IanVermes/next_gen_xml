#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes & functions shared by the check*.py modules.


Meta classes:
    SortableCallable

Functions:
    parse_xml

Copyright Ian Vermes 2019
"""

from lxml import etree

import functools

@functools.total_ordering
class SortableCallable(type):
    """Create class objects that behave like functions and are sortable.

    A call of class dependent on this metaclass will NOT instatiate a new object
    but instead call a curried function, wrapped in the class method ._veneer,
    hence calls of __new__ and __init__ methods will be ignored.

    The class objects are sorted by their class attribute .key.
    """

    def __call__(clsobj, *arg, **kwargs):
        result = clsobj._veneer(*arg, **kwargs)
        return result

    def __lt__(this_clsobj, other_clsobj):
        """Sort by the .key attribute."""
        return this_clsobj.key < other_clsobj.key

    def __eq__(this_clsobj, other_clsobj):
        """Equality related to the .key attribute."""
        return this_clsobj.key == other_clsobj.key


def parse_xml(filename, *args, **kwargs):
    """Convenience function of etree.parse, supporting pathlib.Path arguments.

    Arg:
        filename (str, pathlib.Path)
        *args
    Kwargs:
        **kwargs
    Returns:
        etree.ElementTree
    """
    if isinstance(filename, etree._Element):
        tree = filename.getroottree()
    elif isinstance(filename, etree._ElementTree):
        tree = filename
    else:
        filename = str(filename)
        tree = etree.parse(filename, *args, **kwargs)
    return tree
