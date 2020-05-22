import asyncio
import configparser

from aiohttp import web
from json import dump, loads
from hashlib import sha224
from os import mkdir
from os.path import isdir, isfile

from miscellaneous.config import config_file, set_config_default

# checks if s is in date format (YYYY-MM-DD)
def isdate(s):
    for c in s:
        if c != '-' and not c.isdigit():
            return False
    return True

# redirects request to a given route
def redirect(request, route):
    url = request.app.router[route].url_for()
    raise web.HTTPFound(url)

async def result_to_json_file(res):
    """
    :param res: dict to write into file
    :return: file address
    """
    if isinstance(res, dict):
        # getting results dir from config file
        config = configparser.ConfigParser()
        # if there's no config file, make one
        if not isfile(config_file):
            set_config_default()

        # reading config file
        config.read(config_file)
        # reading result dir address settings
        dir_name = config['results_dir']['dir']
        if not isdir(dir_name):
            mkdir(dir_name)
        file_name = sha224(str(res).encode()).hexdigest()
        file_path = dir_name+'/'+file_name+'.json'
        if not isfile(file_path):
            with open(file_path, 'w') as json_file:
                dump(res, json_file, ensure_ascii=False)
        return file_path
    else:
        print('Input is not a valid object')
        return TypeError