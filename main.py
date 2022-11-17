from support import *
from vk_api.bot_longpoll import VkBotEventType
import button_handlers.admin_buttons as bh
from globals import *
from states import *
from processing_state import processing_state
import threading
import time
import datetime
from init import read_config


def monitor_delay_messages():
    db = DBWorker()
    while True:
        time.sleep(1)
        row_msg = db.get_early_delay_message()
        if len(row_msg) != 0:
            date_time_msg = datetime.datetime.strptime(row_msg[0][5],"%Y-%m-%d %H:%M:%S")
            date_time_now = datetime.datetime.now()
            delta = (date_time_msg - date_time_now).total_seconds()
            if delta <= 0:
                mailing(row_msg[0][1], row_msg[0][2], row_msg[0][3], db=db)
                db.delete_message_for_it_id(row_msg[0][0])


def start_polling():
    mailing_thread = threading.Thread(target=monitor_delay_messages)
    mailing_thread.start()
    print('start')
    init = read_config()
    while init:
        for event in LONGPOLL.listen():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    id = event.obj.message['from_id']
                    print(id)
                    #Админ
                    if DB.is_admin(id):
                        state = DB.get_admin_state(id)
                        processing_state(event, state)
                    else:
                        DB.add_user(id)
                        send_msg(id, 'Не знаю такой команды')

                elif event.type == VkBotEventType.MESSAGE_EVENT:
                    #TODO add try catch
                    user_id = event.obj['user_id']
                    print(event.object.payload.get('type'))
                    if DB.is_admin(user_id):
                        getattr(bh, event.object.payload.get('type'))(int(user_id), event.obj.conversation_message_id)
                    else:
                        DB.add_user(user_id)
                        send_msg(user_id, 'Не знаю такой команды')

                elif event.type == VkBotEventType.MESSAGE_ALLOW:
                    user_id = int(event.obj['user_id'])
                    send_msg(user_id, 'ЗДАРОВА')
                    DB.add_user(user_id)
            except:
                print('stop_bot')
                continue

if __name__ == '__main__':
    start_polling()