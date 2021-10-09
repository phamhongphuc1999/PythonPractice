import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter('%(log_color)s[%(asctime)s] [%(levelname)s]: %(message)s (%(pathname)s:%(lineno)d)', log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }))

logger = colorlog.getLogger('example')
logger.addHandler(handler)

logger.debug("This is debug")
logger.info("This is info")
logger.warning("This is warning")
logger.error("This is error")
logger.critical("This is critical")
