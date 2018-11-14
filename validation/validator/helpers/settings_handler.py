#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Reads a data config file to yield a data object with fixed attributes.

Copyright Ian Vermes 2018
"""

from validator import exceptions

import configparser
import os




class Singleton(type):
    """A meta class for creating instance patterns.

    https://stackoverflow.com/a/6798042

    In general, it makes sense to use a metaclass to implement a singleton. A
    singleton is special because is created only once, and a metaclass is the
    way you customize the creation of a class. Using a metaclass gives you more
    control in case you need to customize the singleton class definitions in
    other ways.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset_singleton(self, class_):
        "Support method for unittesting: reset a preiously instantiated singleton."
        metaclass = type(self)
        if isinstance(class_, metaclass):
            singleton = self._instances.pop(class_)
            del singleton
        else:
            errmsg = ("Expects a class that inherits from the metaclass "
                      "and not an instance of that class i.e. not the "
                      "singleton of that class.")
            raise TypeError(errmsg)



class Settings(metaclass=Singleton):
    """An object orientated version of the settings config file.

    Args:
        config_filename(str): Path to .INI file.

    Methods:
        log_filename: Generate a path for where the log file is expected to be.
    """

    @staticmethod
    def _get_config(filename):
        if not os.path.isfile(filename):
            errmsg = f"No file found at {filename}."
            raise exceptions.FileNotFound(errmsg)
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def __init__(self, config_filename):
        """Initialise, dependent on being able to read a config file."""
        self._config = self._get_config(config_filename)
        self.__log_filename = ""


    # [DEFAULT] RELATED METHODS

    # [Log File] RELATED METHODS
    @property
    def log_filename(self):
        return self.__log_filename


    # [xslt] RELATED METHODS

    # [schema] RELATED METHODS
