import logging 
from config.settings import LOG_FILE

def get_logger(name="EPLProject"):
    logger = logging.getLogger(name)

    # unviker dubbletter
    #if logger.handlers: 
    #    return logger
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    # loggning och format
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger