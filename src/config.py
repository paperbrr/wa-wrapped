import json
from json.decoder import JSONDecodeError
import os


CONFIG_FILE_NAME = 'config.json'
PLOTS_DIR_NAME = 'plots'
CONFIG_KEYS = ['MINIMUM_WORD_LENGTH', 'SPECIAL_SEARCH_WORDS', 'CASE_SENSITIVE_SEARCH', 'BLACKLISTED_WORDS']


def create_default_config():

    default_config = {
        'MINIMUM_WORD_LENGTH': 4,
        'SPECIAL_SEARCH_WORDS': [],
        'CASE_SENSITIVE_SEARCH': False,
        'BLACKLISTED_WORDS': []
    }
    with open(CONFIG_FILE_NAME, 'w') as default:
        json.dump(default_config, default)


def check_keys(config):

    for key in CONFIG_KEYS:
        if key not in config:
            print(f'Invalid key "{key}" in config file. Creating with default values.')
            create_default_config()
            return False
    return True


def check_values(config):

    if type(config['MINIMUM_WORD_LENGTH']) != int and type(config['SPECIAL_SEARCH_WORDS']) != list and type(config['CASE_SENSITIVE_SEARCH']) != bool and type(config['BLACKLISTED_WORDS']) != list:
        return False
    
    return True


def get_configs():

    try:
        with open(CONFIG_FILE_NAME, 'r') as cf:
            configs = json.load(cf)
        if not check_keys(configs) or not check_values(configs):
            create_default_config()
            return get_configs()
        return configs
    
    except FileNotFoundError:
        print('Could not find config file. Creating with default values.')
        create_default_config()
        return get_configs()
    
    except JSONDecodeError:
        print('Invalid values provided. Creating new config file with default values.')
        create_default_config()
        return get_configs()
    

def get_file_data(file_name):

    try:
        with open(file_name, 'r', encoding='UTF8') as file:
            data = file.readlines()
        return data
    
    except FileNotFoundError:
        print('Could not find file, exiting.')
        exit()


def make_plots_folder():

    path = PLOTS_DIR_NAME 
    if not os.path.exists(f'{path}'):
        os.makedirs(f'{path}')


def config(file_name):

    file_data = get_file_data(file_name)
    configs = get_configs()
    make_plots_folder()

    return file_data, configs['MINIMUM_WORD_LENGTH'], configs['SPECIAL_SEARCH_WORDS'], configs['CASE_SENSITIVE_SEARCH'], configs['BLACKLISTED_WORDS']