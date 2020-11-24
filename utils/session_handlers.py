import json
import logging
import datetime
import time

# Using the 'sys.path' hack until I find a cleaner one
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


from loggers import AssessLogger


""" Returns the current time and timezone  """
def get_current_time():
    # takes no params
    return datetime.datetime.now(), time.tzname[time.daylight]


""" Wraps up a session before it closes  """
def wrapup_all():
    files_to_close = ['logs/assess.log', 'logs/errors.log', 'logs/warnings.log', 'logs/commands.log']
    with open('./data/session/overview.json') as f:
            stats = json.load(f)
    # log some assessement info
    AssessLogger.log(f'{stats["commands_ran"]} Commands Executed in Session.')
    AssessLogger.log(f'Session Lasted for {stats["ses_end_time"] - stats["ses_start_time"]}.')
    AssessLogger.log('Closing Session ...')
    wrap_time, tzname = get_current_time()
    for f in files_to_close:
        wrapup_logger = logging.getLogger(f)
        if not wrapup_logger.hasHandlers():
            f_handler = logging.FileHandler(f)
            f_format = logging.Formatter('%(message)s')
            f_handler.setFormatter(f_format)
            wrapup_logger.addHandler(f_handler)
            wrapup_logger.setLevel('DEBUG') # set to show up
        # send assess logger a list commands run
        wrapup_logger.debug(f'Session Terminated ~ {wrap_time} ({tzname}).')
        wrapup_logger.info('==========') # add a divider to make it more readable
    print('Closing after error ...')
    sys.exit()


