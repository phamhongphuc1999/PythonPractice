import logging

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
MY_LOG = 25
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

logging.addLevelName(MY_LOG, "MY_LOG")


class MyLogger(logging.Logger):
    def __init__(self, name: str):
        """
        The constructor of TravaLogger

        :param name: The logger name
        """
        super().__init__(name)

    def trava_log(self, msg):
        """
        Log message with TRAVA_LOG level

        :param msg: The logging message
        """
        self.log(MY_LOG, msg)
