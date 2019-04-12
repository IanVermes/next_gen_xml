#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""OS and Path related convenience functions.

Copyright Ian Vermes 2018
"""

from helpers.enum import Check
import exceptions

import pathlib


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
               f"dir_exists={dir_exists}, "
               f"exists={exists}.")
        raise ValueError(msg)

    filename = pathlib.Path(filename).expanduser()

    if check is Check.PARENT_ONLY:
        dirname = filename.parent
        extant = dirname.exists()
    elif check is Check.EXISTS:
        extant = filename.exists()
    elif check is Check.DONT:
        extant = True
    else:
        raise exceptions.UnexpectedEnum(repr(check))

    if not extant:
        msg = "{file} does not exist."
        if check is Check.EXISTS:
            raise exceptions.FileNotFound(msg.format(file=filename))
        elif check is Check.PARENT_ONLY:
            raise exceptions.ParentDirNotFound(msg.format(file=filename.parent))
    else:
        return str(filename.absolute())
