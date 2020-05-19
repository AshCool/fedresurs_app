from json import dump

config_file = 'config.json'

config_data = {
    'messages_guid_url': 'https://services.fedresurs.ru/SignificantEvents/MessageServiceDemo/api/Messages/all?',
    'message_info_url' : 'https://services.fedresurs.ru/SignificantEvents/MessageServiceDemo/api/Messages/',
    'login': 'demo',
    'password': 'Ax!761BN',
    'messages_types': 'messageType=CreditorIntentionGoToCourt&messageType=DebtorIntentionGoToCourt'
                      '&messageType=AppearanceOfBankruptcySigns&messageType=BankruptcyArticle8&'
                      'messageType=BankruptcyArticle9&messageType=DebtorBankruptcyCourtNotification'
}

def set_config():
    with open(config_file, 'w') as config:
        dump(config_data, config)


set_config()