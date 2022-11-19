from support import *
from vk_api.bot_longpoll import VkBotEventType
import button_handlers.admin_buttons as bh
import globals
from states import *
from processing_state import processing_state
import threading
import time
import datetime
from datetime import timedelta
from db_worker import DBWorker
from init import init


def monitor_delay_messages():
    db = DBWorker(globals.OWNER_ID)
    while True:
        time.sleep(5)
        row_msg = db.get_early_delay_message()
        if len(row_msg) != 0:
            date_time_msg = datetime.datetime.strptime(row_msg[0][5],"%Y-%m-%d %H:%M:%S")
            date_time_now = datetime.datetime.now() + timedelta(hours=int(globals.DELTA_TIME_SERVER))
            delta = (date_time_msg - date_time_now).total_seconds()
            
            if delta <= 0:
                mailing(row_msg[0][1], row_msg[0][2], row_msg[0][3], db=db)
                db.delete_message_for_it_id(row_msg[0][0])

def start_polling():
    inited = init()
    globals.DB = DBWorker(globals.OWNER_ID, globals.DEFAULT_START_MESSAGE)
    mailing_thread = threading.Thread(target=monitor_delay_messages)
    mailing_thread.start()
    print('start')
    while inited:
        try:
            for event in globals.LONGPOLL.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        id = event.obj.message['from_id']
                        # send_hello_message(id)
                        print(id)
                        #Админ
                        if globals.DB.is_admin(id):
                            state = globals.DB.get_admin_state(id)
                            processing_state(event, state)
                        else:
                            globals.DB.add_user(id)
                            if 'payload' in event.obj.message:
                                if event.obj.message['payload'] == '{"command":"start"}':
                                    continue
                            send_msg(id, globals.ANSWER_TO_USER)

                    elif event.type == VkBotEventType.MESSAGE_EVENT:
                        #TODO add try catch
                        user_id = event.obj['user_id']
                        print(event.object.payload.get('type'))
                        if globals.DB.is_admin(user_id):
                            getattr(bh, event.object.payload.get('type'))(int(user_id), event.obj.conversation_message_id)
                        else:
                            globals.DB.add_user(user_id)
                            if 'payload' in event.obj.message:
                                if event.obj.message['payload'] == '{"command":"start"}':
                                    continue
                            send_msg(user_id, globals.ANSWER_TO_USER)

                    elif event.type == VkBotEventType.MESSAGE_ALLOW:
                        user_id = int(event.obj['user_id'])
                        send_hello_message(user_id)
                        
                    # id = event.obj.message['from_id']
                    # start_message = globals.DB.get_start_message()
                    # send_msg(id, start_message)
                    # globals.DB.add_user(id)
        except:
            print('exception')
            pass

if __name__ == '__main__':
    start_polling()