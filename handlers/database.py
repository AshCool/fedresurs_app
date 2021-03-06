import configparser
from os.path import isfile

import asyncpg

from miscellaneous.config import config_file, set_config_default
from miscellaneous.log import log
from miscellaneous.misc import isdate


# creates and returns connection object
async def get_connection():
    """
    :return: DB connection object
    """
    # getting db connection settings from config file
    config = configparser.ConfigParser()
    # if there's no config file, make one
    if not isfile(config_file):
        set_config_default()

    # reading config file
    config.read(config_file)
    # reading db settings
    db_data = config['postgresql']

    return await asyncpg.connect(host=db_data['host'], port=db_data['port'], user=db_data['user'],
                                 password=db_data['password'], database=db_data['database'])


# function-wrapper for selecting data from table by id
async def select(table, record_id):
    """
    :param table: table to select entry from
    :param record_id: entry id
    :return: selected entry
    """
    await log('Selecting data from table ' + str(table) + ' with id ' + str(record_id))
    await log('Opening connection to DB')
    conn = await get_connection()
    await log('Opened DB connection')

    # we'll call it an SQL injection protection
    if not isinstance(table, str) or not table.isalnum():
        await log('Got incorrect table name, halting select operation')
        return None

    cmd = 'SELECT * FROM ' + table + ' WHERE request_id = ' + str(record_id) + ';'

    try:
        res = await conn.fetch(cmd)
    except asyncpg.exceptions.DataError:
        await log('Got ' + str(asyncpg.exceptions.DataError) + ', halting select operation')
        return None

    await log('Closing DB connection')
    await conn.close()
    await log('DB connection is closed')

    await log('Entry successfully selected')

    return res

# function-wrapper for inserting data into table
async def insert(table, **args):
    """
    :param table: table to insert in
    :param args: dict of inserting fields:values
    :return: inserted entry
    """
    await log('Inserting arguments ' + str(args) + ' into table ' + str(table))
    await log('Opening connection to DB')
    conn = await get_connection()
    await log('Opened DB connection')

    # we'll call it an SQL injection protection
    if not isinstance(table, str) or not table.isalnum():
        await log('Got incorrect table name, halting insert operation')
        return None

    cmd = 'INSERT INTO ' + table + '('

    for key in args.keys():
        cmd += key + ', '
    # removing last ', '
    cmd = cmd[:-2]
    cmd += ') VALUES ('

    for value in args.values():
        if not isinstance(value, str) and not value.isalnum() and not isdate(value):
            await log('Got incorrect value (' + str(value) + '), halting insert operation')
            return None
        else:
            cmd += '\'' + value + '\', '

    cmd = cmd[:-2]
    cmd += ') RETURNING *;'

    try:
        res = await conn.fetch(cmd)
    except asyncpg.exceptions.DataError:
        await log('Got ' + str(asyncpg.exceptions.DataError) + ', halting insert operation')
        return None

    await log('Closing DB connection')
    await conn.close()
    await log('DB connection is closed')

    await log('Entry successfully inserted')

    return res