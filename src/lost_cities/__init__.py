"""Top-level package for Lost Cities card game."""
import logging

__author__ = """Mathis Nicoli"""
__email__ = "mathis.nicoli@gmail.com"
VERSION = (0, 2, 0)
__version__ = ".".join(map(str, VERSION))

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(console_handler)
