# just some utitlity loggers

import logging

class GeneralLogger:
    @classmethod
    def log(cls, msg: str, time_used: str = ''):
        if logging.getLogger(cls.__name__).hasHandlers(): # add this to prevent weird behavior
            tempLogger = logging.getLogger(cls.__name__) # unique lo
            getattr(tempLogger, cls.level.lower())(msg)
        else:    
            tempLogger = logging.getLogger(cls.__name__) # unique logger per logging utility
            f_handler = logging.FileHandler(cls.path)
            f_format = logging.Formatter(cls.format)
            f_handler.setFormatter(f_format)
            tempLogger.addHandler(f_handler)
            getattr(tempLogger, cls.level.lower())(msg)

# simple to create loggers after that

class AssessLogger(GeneralLogger):
    """ Class that handles any assessement logs  """
    path = 'logs/assess.log'
    format = '%(message)s'
    level = 'WARNING' # labeled as this to show up
 
class WarningLogger(GeneralLogger):
    """ Class that handles warning logs (too many requests, data leaks, etc.)  """
    path = 'logs/warnings.log'
    format = '%(message)s'
    level = 'WARNING'

class ErrorLogger(GeneralLogger):
    """ Class that handles and exceptions thrown in the code  """
    path = 'logs/errors.log'
    format = '%(message)s'
    level = 'ERROR'

class StreamLogger(GeneralLogger):
    """ Class that logs the stream of commands  """
    path = 'logs/commands.log'
    format = '%(message)s'
    level = 'WARNING' # labeled as this to show up
