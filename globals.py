# -*- coding: utf-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

GROUP_ID = '217222460'
GROUP_TOKEN = 'vk1.a.suoSnNlueJ1hWhGYtpGG6uarMBrHr6QI6VsxPRRMb4G2hMFCkm2Mc6xEIuCoT0ofD8p11R8CeqbMa0NTrSGx06cDjYV7YEvhHQ8v9fT6PSzV0uV_YfX4WQ96_P_6XNU4LiLDdcw83s-CQy7ZKDL5MwUPTFuFHey1m_zM-ASB5hidaZ2jSvwAmU6_iCqITxU9kdlRM1u00JYcIoXI2swpLQ'
API_VERSION = '5.131'
DEFAULT_START_MESSAGE = f"ПРИВЕТ, я бот. Жди сообщения от админа"
OWNER_ID = 54442110
DB = None
VK_SESSION = None
VK = None
LONGPOLL = None
DELTA_TIME_SERVER = 0
ANSWER_TO_USER = 'Не знаю такой команды'
# VK_SESSION = vk_api.VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
# VK = VK_SESSION.get_api()
# LONGPOLL = VkBotLongPoll(VK_SESSION, group_id=GROUP_ID)