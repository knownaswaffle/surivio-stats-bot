# Using the 'sys.path' hack until I find a cleaner one
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from loggers import WarningLogger

class ErrorHandler:
