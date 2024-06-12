import logging

__all__ = ('create_logger',)


def create_logger(name: str) -> logging.Logger:
    """Create logger which doesn't propagate messages to the root logger."""
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger
