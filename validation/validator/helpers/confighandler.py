#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Reads a data config file to yield a data object with fixed attributes.

Copyright Ian Vermes 2018
"""

import configparser
import os




class ConfigData(object):
    """An object orientated version of the settings config file.

    Args:
        config_filename(str): Path to .INI file.

    Methods:
        log_filename: Generate a path for where the log file is expected to be.
    """

    def __init__(self, config_filename):
        """Initialise. Dependent on being able to read a config file."""
        if not os.path.isfile(config_filename):
            raise FileNotFoundError(f"No file found at {config_filename}.")

        self.config = configparser.ConfigParser()
        self.config.read(config_filename)

        self._section_log_file = "Log File"
        assert self.config.has_section(self._section_log_file)

    # [DEFAULT] RELATED METHODS

    # [log_file] RELATED METHODS

    def log_filename(self, user_directory=None):
        """Generate a path for where the log file is expected to be.

        The log file basename is a default value in the config file.

        Derives a file path based on INI settings and an optional directory. If
        the user provides directory, the log file would reside in it.

        Args:
            user_directory(str): Optional. Default is to use INI settings,
                otherwise the log file will be in the user directory.
        Return:
            str
        """
        section = self._section_log_file

        basename = self.config.get(section, "basename_default")
        local_prefix = self.config.get(section, "local_path_default")
        basename = os.path.join(local_prefix, basename)

        if user_directory is None:
            target_directory = self.config.get(section, "directory_default")
        else:
            target_directory = user_directory
        result = os.path.join(target_directory, basename)
        # result still has a local prefix and may have "~" user folder notation
        result = os.path.abspath(os.path.expanduser(result))

        return result

    # [xslt] RELATED METHODS

    # [schema] RELATED METHODS
