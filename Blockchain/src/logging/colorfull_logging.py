import logging
from color_config import (
    fgCyan,
    fgWhite,
    fgGreen,
    fgYellow,
    fgRed,
    reset,
    bold,
    fgMagenta,
)

COLORS = {
    "DEBUG": fgWhite,
    "INFO": fgGreen,
    "WARNING": fgYellow,
    "ERROR": fgRed,
    "CRITICAL": fgMagenta,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        level_name = record.levelname
        if self.use_color and level_name in COLORS:
            level_name_color = COLORS[level_name] + f"[{level_name}]" + reset
            record.levelname = level_name_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = f"{bold}[%(asctime)s]{reset} %(levelname)s: {bold}%(message)s{reset} {fgCyan}(%(filename)s:%(lineno)d){reset}"

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        return


logging.setLoggerClass(ColoredLogger)

if __name__ == "__main__":
    abc = ColoredLogger("abc")
    abc.debug("This is debug")
    abc.info("This is info")
    abc.warning("This is warning")
    abc.error("This is error")
    abc.critical("this is critical")
