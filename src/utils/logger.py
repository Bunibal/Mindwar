import logging
import os

logging.basicConfig(
    level=os.getenv("LOGLEVEL", "INFO"),
    format="%(asctime)s [%(funcName)s]-[%(lineno)d] [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
