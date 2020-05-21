import configparser
from datetime import datetime
from os.path import isfile
from time import time

from miscellaneous.config import config_file, set_config_default


# asynchronously logs given string along w/ current time
async def log(s):
    config = configparser.ConfigParser()
    # if there's no config file, make one
    if not isfile(config_file):
        set_config_default()

    # reading config file
    config.read(config_file)
    # reading db settings
    log_file = config['log_file']['file']

    with open(log_file, 'a') as lf:
        # logs message w/ current time
        lf.write(str(datetime.fromtimestamp(time())) + ': ' + s + '\n')

