import configparser

config = configparser.ConfigParser()

# API section
config['API'] = {
    'messages_guid_url': 'https://services.fedresurs.ru/SignificantEvents/MessageServiceDemo/api/Messages/all?',
    'message_info_url' : 'https://services.fedresurs.ru/SignificantEvents/MessageServiceDemo/api/Messages/',
    'login': 'demo',
    'password': 'Ax!761BN',
    'messages_types': 'messageType=CreditorIntentionGoToCourt&messageType=DebtorIntentionGoToCourt'
                      '&messageType=AppearanceOfBankruptcySigns&messageType=BankruptcyArticle8&'
                      'messageType=BankruptcyArticle9&messageType=DebtorBankruptcyCourtNotification'
}

# DB section
config['postgresql'] = {
    'host': 'dumbo.db.elephantsql.com',
    'database': 'wnjfngyp',
    'user': 'wnjfngyp',
    'password': 'UDqXfNC_gzUnWCckadYeH7k7xtQ28uvj',
    'port': '5432'
}

config['log_file'] = {
    'file': 'log.txt'
}

config['results_dir'] = {
    'dir': 'request_results'
}

# config file
config_file = 'configs/config.ini'

def set_config_default():
    with open(config_file, 'w') as cf:
        config.write(cf)
