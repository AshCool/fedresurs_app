import configparser
import re
from json import loads
from os.path import isfile

import requests
from requests.auth import HTTPBasicAuth

from miscellaneous.config import config_file, set_config_default

# loading config file
config = configparser.ConfigParser()
# if there's no config file, make one
if not isfile(config_file):
    set_config_default()
config.read(config_file)

# reading config file
sections = config.sections()
print(sections)

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

# DG connection
db_data = config['postgresql']

# storing authentication object
auth = HTTPBasicAuth(LOGIN, PASSWORD)

# requesting messages
response = requests.get(MESSAGES_GUID_URL + 'begin=2019-07-01&end=2019-07-30&'+TYPES, auth=auth)
print('response', response, '\n')
# response text is a JSON list
response_data = loads(response.text)

message_data = {}
if response_data:
    # as per API documentary, we can only send 8 request in a second
    for i in range(0, len(response_data), 8):
        for item in response_data[i:i+8]:
            response = requests.get(MESSAGE_INFO_URL + item, auth=auth)
            if response.status_code != 200:
                # TODO: logging
                print('something went wrong')
            else:
                try:
                    date_publish = re.search(r'(?:"datePublish":"(.*?)")', response.text).group(1)
                    message_text = re.search(r'(?:<Text>(.*?)</Text>)', response.text).group(1)
                    message_data[item] = {'date_publish': date_publish, 'message_text': message_text}
                except AttributeError:
                    # crude handling of field absence
                    # most likely, there's no need for that, 'cause there shouldn't be such problem
                    pass

for item in message_data:
    print(item)
    print(message_data[item])
    print()

