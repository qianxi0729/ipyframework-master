# -*- coding: utf-8 -*-
import logging

try:
    from robot.api import logger
except ImportError as err:
    pass
from robot.running.context import EXECUTION_CONTEXTS


class Logger(object):
    def __init__(self):
        self._robot_run = False
        if EXECUTION_CONTEXTS.current:
            self._robot_run = True
        self.robot_logger = logger
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = logging.getLogger('RobotFileLogger')
            self._logger.setLevel(level=logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler('RobotLibraryOut.log', 'a')            
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)

            self._logger.addHandler(fh)
            self._logger.addHandler(ch)
        return self._logger

    def debug(self, msg, html=False):
        if self._robot_run:
            self.robot_logger.debug(msg, html)
        else:
            self.logger.debug(msg)

    def trace(self, msg, html=False):
        if self._robot_run:
            self.robot_logger.trace(msg, html)
        else:
            self.logger.debug(msg)

    def info(self, msg, html=False):
            if self._robot_run:
                self.robot_logger.info(msg, html)
            else:
                self.logger.info(msg)

    def warning(self, msg, html=False):
        if self._robot_run:
            self.robot_logger.warn(msg, html)
        else:
            self.logger.warning(msg)

    def error(self, msg, html=False):
        if self._robot_run:
            self.robot_logger.error(msg, html)
        else:
            self.logger.error(msg)


LOGGER = Logger()

