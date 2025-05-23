from hate.logger import logging
#logging.info("This is a test log message.")

from hate.exception import CustomException
import sys

try:
    a = 1 / 0
except Exception as e:
    raise CustomException(e, sys) from e
