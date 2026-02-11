import logging

def set_screen_logger(logger: logging.Logger):

    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s:%(name)s:%(filename)s:%(lineno)d: %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)


def set_file_logger(logger: logging.Logger,
                    filename: str,
                    level: int = logging.ERROR) -> None:

    handler = logging.FileHandler(filename)
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s:%(name)s:%(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(fmt)
    handler.setLevel(level)

    logger.setLevel(level)
    logger.addHandler(handler)