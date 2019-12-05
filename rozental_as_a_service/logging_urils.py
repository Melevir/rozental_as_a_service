import logging


def set_logging_level(verbosity: int, logger: logging.Logger, max_logging: int = 3) -> None:
    logger.setLevel(max(max_logging - verbosity, 0) * 10)
