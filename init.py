import configparser
from globals import *

def read_config():
    global GROUP_TOKEN
    global GROUP_ID
    global OWNER_ID
    global DEFAULT_START_MESSAGE
    global API_VERSION
        
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        cfg_default = config['DEFAULT']
        GROUP_TOKEN = cfg_default['Token']
        GROUP_ID = cfg_default['GroupId']
        OWNER_ID = cfg_default['OwnerId']
        DEFAULT_START_MESSAGE = cfg_default['DefaultStartMessage']
        API_VERSION = cfg_default['ApiVersion']
        return True
    except:
        print('Не удалось загрузить конфиг')
        return False