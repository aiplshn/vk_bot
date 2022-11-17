import configparser
import globals
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

def read_config() -> bool:        
    try:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        cfg_default = config['DEFAULT']
        globals.GROUP_TOKEN = cfg_default['Token']
        globals.GROUP_ID = cfg_default['GroupId']
        globals.OWNER_ID = cfg_default['OwnerId']
        globals.DEFAULT_START_MESSAGE = cfg_default['DefaultStartMessage']
        globals.API_VERSION = cfg_default['ApiVersion']
        return True
    except:
        print('Не удалось загрузить конфиг')
        return False

def init() -> bool:
    res = read_config()
    if res:
        globals.VK_SESSION = vk_api.VkApi(token=globals.GROUP_TOKEN, api_version=globals.API_VERSION)
        globals.VK = globals.VK_SESSION.get_api()
        globals.LONGPOLL = VkBotLongPoll(globals.VK_SESSION, group_id=globals.GROUP_ID)
    return res