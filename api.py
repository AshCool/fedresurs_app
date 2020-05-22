import asyncio
import configparser
import re
import requests

from json import loads
from os.path import isfile
from requests.auth import HTTPBasicAuth
from time import sleep

from miscellaneous.config import config_file, set_config_default

# loading config file
config = configparser.ConfigParser()
# if there's no config file, make one
if not isfile(config_file):
    set_config_default()
config.read(config_file)

# API
api_data = config['API']
# URL for getting GUID's of messages
MESSAGES_GUID_URL = api_data['messages_guid_url']
# URL for getting info from messages
MESSAGE_INFO_URL = api_data['message_info_url']
# login and password for test service authentication
LOGIN = api_data['login']
PASSWORD = api_data['password']
# all types of bankruptcy messages as a string of parameters
TYPES = api_data['messages_types']

# storing authentication object
auth = HTTPBasicAuth(LOGIN, PASSWORD)

# messages' list request
async def request_messages(begin, end, participant_type, participant_id):
    """
    :param begin: begin of search date
    :param end: end of search date
    :param participant_type: type of sender
    :param participant_id: sender's id
    :return: list of messages' ids
    """
    # requesting messages
    if participant_type != 'any':
        request_parameters = 'begin=' + str(begin) + '&end=' + str(end) +'&Participant.Type=' + str(participant_type) \
                             + '&Participant.Code=' + str(participant_id) +'&' + TYPES
    else:
        request_parameters = 'begin=' + str(begin) + '&end=' + str(end) + '&' + TYPES

    response = requests.get(MESSAGES_GUID_URL + request_parameters, auth=auth)

    # response text is a JSON list
    return loads(response.text)

# messages' data request
async def request_messages_data(messages):
    """
    :param messages: list of messages' ids
    :return: dict of messages' content
    """
    messages_data = {}
    if messages:
        # as per API documentation, we can only send 8 request in a second
        for i in range(0, len(messages), 8):
            for item in messages[i:i + 8]:
                response = requests.get(MESSAGE_INFO_URL + item, auth=auth)
                if response.status_code != 200:
                    print('Something went wrong')
                else:
                    try:
                        date_publish = re.search(r'(?:"datePublish":"(.*?)")', response.text).group(1)
                        message_text = re.search(r'(?:<Text>(.*?)</Text>)', response.text).group(1)
                        messages_data[item] = {'date_publish': date_publish, 'message_text': message_text}
                    except AttributeError:
                        # crude handling of field absence
                        # most likely, there's no need for that, 'cause there shouldn't be such problem
                        pass
            sleep(1)

    return messages_data

async def search_for_messages_data(begin, end, participant_type, participant_id):
    """
    :param begin: begin of search date
    :param end: end of search date
    :param participant_type: type of sender
    :param participant_id: sender's id
    :return: dict of messages' content
    """
    return await request_messages_data(await request_messages(begin, end, participant_type, participant_id))
