from json import load
from config import config_file, set_config

import requests
from requests.auth import HTTPBasicAuth

import re

# loading config data
# handling absence of config file
try:
    open(config_file, 'r')
except FileNotFoundError:
    set_config()
finally:
    # kinda awkward
    with open(config_file, 'r') as config:
        config_data = load(config)
        # API URLs
        # URL for getting GUID's of messages
        MESSAGES_GUID_URL = config_data['messages_guid_url']
        # URL for getting info from messages
        MESSAGE_INFO_URL = config_data['message_info_url']
        # login and password for test service authentication
        LOGIN = config_data['login']
        PASSWORD = config_data['password']
        # all types of bankruptcy messages as a string of parameters
        TYPES = config_data['messages_types']

# storing authentication object
auth = HTTPBasicAuth(LOGIN, PASSWORD)

# requesting messages
response = requests.get(MESSAGES_GUID_URL + 'begin=2019-07-01&end=2019-07-30&'+TYPES, auth=auth)
print('response', response, '\n')
# response will contain strings of messages' GUIDs or will be empty string
raw_response_data = response.text.strip('[]')
# splitting string by individual GUIDs and storing them in a list
response_data = [item.strip('\"') for item in raw_response_data.split(',')]

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

