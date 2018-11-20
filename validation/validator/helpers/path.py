#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""OS and Path related convenience functions.

Copyright Ian Vermes 2018
"""

import exceptions

import os
import enum


class Check(enum.Enum):
    """An Enum used in validation of fileoperation"""
    DONT = 1
    EXISTS = 2
    PARENT_ONLY = 3
    # Permsissions?


def expandpath(filename, exists=False, dir_exists=True):
    """Expand user-provided filenames into extant and valid filenames.

    Args:
        filename(str): File or directory path.
        exists(bool): If True, raise an exception if filename doesn't
            exit, otherwise treat as theoretical filename.
        dir_exists(bool): If True, raise an exception if the directory of
            filename doesn't exist, otherwise treat as a theoretical filename.
            Useful if you wish to validate the target destination before
            writing a file.
    Return
        str
    Exceptions:
        validator.exceptions.FileNotFound
        validator.exceptions.DirNotFound
        validator.exceptions.ParentDirNotFound
    """
    if dir_exists and not exists:
        check = Check.PARENT_ONLY
    elif (dir_exists and exists) or (not dir_exists and exists):
        check = Check.EXISTS
    elif not dir_exists and not exists:
        check = Check.DONT
    else:
        msg = ("Unexpected kwarg combination: "
               f"dir_exists: {dir_exists}, "
               f"exists: {exists}.")
        raise ValueError(msg)

    expandpath = os.path.abspath(os.path.expanduser(filename))

    if check is Check.PARENT_ONLY:
        dirname = os.path.dirname(expandpath)
        extant = os.path.isdir(dirname)
    elif check is Check.EXISTS:
        extant = os.path.exists(expandpath)
    elif check is Check.DONT:
        extant = True
    else:
        raise exceptions.UnexpectedEnum(repr(check))

    if not extant:
        if check is Check.EXISTS:
            raise exceptions.FileNotFound(expandpath)
        elif check is Check.PARENT_ONLY:
            raise exceptions.ParentDirNotFound(expandpath)
    else:
        return expandpath
