#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅

# std lib
import logging
import sys

# project modules
from common.patterns.singleton import Singleton
from common.config_parser.config_manager import ConfigManager


LOG_LEVELS = ['DEBUG', 'INFO', 'ERROR', 'CRITICAL']


@Singleton
class LogHandler:

    def __init__(self):
        if ConfigManager().get_str('LOGGER', 'log_level', 'DEBUG') in LOG_LEVELS:
            self.log_level = ConfigManager().get_str('LOGGER', 'log_level', 'DEBUG')
        else:
            self.log_level = 'DEBUG'

        self.log_time_format = ConfigManager().get_str('LOGGER', 'log_time_format')
        self.log_format = ConfigManager().get_str('LOGGER', 'log_format')

        stdout = logging.StreamHandler(sys.stdout)

        logging.basicConfig(
            level=self.log_level,
            datefmt=self.log_time_format,
            format=self.log_format,
            handlers=[stdout]
        )

        self.stdout_logger = logging.getLogger(__name__)

    def debug(self, message):
        self.stdout_logger.debug(message)

    def info(self, message):
        self.stdout_logger.info(message)

    def error(self, message):
        self.stdout_logger.error(message)

    def critical(self, message):
        self.stdout_logger.critical(message)
