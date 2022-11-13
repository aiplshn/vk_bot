import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from db_worker import DBWorker


GROUP_ID = '217125658'
GROUP_TOKEN = 'vk1.a.DoW2Qze3bc0GXGJPQkTlWGc1lsWPzs6x90FPXCntW8S6NNpPi4Cz-rZbFjdDixxoSBrMtP5qtyilUxYDKJ_SmFd_V_uocFgabBS4mFNuKDxdmfzYmdDrpusam2hj2zWESCm926QexMsS71QzzRfl9M5n6r0mMUEjkwaMCjyKA26T16jhnDr7x06jen2Qrx--R1jRphG3zoT1h_nv2usy0g'
API_VERSION = '5.131'

DB = DBWorker()
VK_SESSION = vk_api.VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
VK = VK_SESSION.get_api()
LONGPOLL = VkBotLongPoll(VK_SESSION, group_id=GROUP_ID)


