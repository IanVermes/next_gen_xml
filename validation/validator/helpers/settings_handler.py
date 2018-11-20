#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Reads a data config file to yield a data object with fixed attributes.

Copyright Ian Vermes 2018
"""

import exceptions
import helpers.path as path

import configparser
import enum
import os


class Mode(enum.Enum):
    LIVE = 1
    TEST = 2

    @classmethod
    def get_default(cls):
        return cls.LIVE


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
    """An object orientated singleton of the settings config file.

    Args:
        config_filename(str): Path to .INI file.
    Kwargs:
        mode(Mode): By default use the Mode.default(),
                    otherwise Mode.LIVE or Mode.TEST.

    Attributes:
        log_filename: The path for where the log file is expected to be written.
        mode: Mode.LIVE or Mode.TEST, used internally and for external operations.
    """

    @staticmethod
    def _get_config(filename):
        if not os.path.isfile(filename):
            errmsg = f"No file found at {filename}."
            raise exceptions.FileNotFound(errmsg)
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def __init__(self, config_filename, mode=None):
        """Initialise, dependent on being able to read a config file.

        Args:
            config_filename(str): Path to config.ini file of package.
        Kwargs:
            mode(Mode): By default use the Mode.default(),
                        otherwise Mode.LIVE or Mode.TEST.
        Exceptions:

        """
        # Dependecy attributes
        self.__mode = self._get_enumareted_mode(mode)
        self.__config = self._get_config(config_filename)
        # Calculated attributes
        self.__log_filename = self._attr_get_log_filename()

    def _get_value_from_config(self, option):
        value = self.__config.get(str(self.mode), option)
        return value

    # mode
    @property
    def mode(self):
        return self.__mode

    def _get_enumareted_mode(self, mode):
        if mode is None:
            mode = Mode.get_default()

        if not isinstance(mode, Mode):
            msg = "Use enums from the Mode class."
            raise TypeError(msg)
        else:
            if mode is Mode.LIVE or mode is Mode.TEST:
                return mode
            else:
                raise exceptions.UnexpectedEnum(mode)

    # log_filename
    @property
    def log_filename(self):
        return self.__log_filename

    def _attr_get_log_filename(self):
        option = "log_filename"
        filename = self._get_value_from_config(option)
        filename = path.expandpath(filename, exists=False, dir_exists=True)
        return filename
