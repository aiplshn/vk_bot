from support import *
from vk_api.bot_longpoll import VkBotEventType
import button_handlers.admin_buttons as bh
from globals import *
from config import *
from processing_state import processing_state
import threading
import time
import datetime

id_admin = 54442110
id_kate = 292576789
def monitor_delay_messages():
    i = 0
    db = DBWorker()
    while True:
        time.sleep(1)
        row_msg = db.get_early_delay_message()
        if len(row_msg) != 0:
            date_time_msg = datetime.datetime.strptime(row_msg[0][5],"%Y-%m-%d %H:%M:%S")
            date_time_now = datetime.datetime.now()
            delta = (date_time_msg - date_time_now).total_seconds()
            print(delta)
            if delta <= 0:
                mailing(row_msg[0][1], row_msg[0][2], row_msg[0][3], db=db)
                db.delete_message_for_it_id(row_msg[0][0])


def send_text(id, text, keyboard=None):
    post = {'user_id': id,
            'message': text,
            'random_id': 0
            }
    if keyboard != None:
        post['keyboard'] = keyboard
    # print(keyboard)
    VK_SESSION.method('messages.send', post)

x = threading.Thread(target=monitor_delay_messages)
x.start()
print('start')
for event in LONGPOLL.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            id = event.obj.message['from_id']
            print(id)
            #Админ
            if id == id_admin or id == id_kate:
                state = DB.get_admin_state(id)
                if state == States.S_START:
                    keyboard = gen_keyboard(
                        ['Создать сообщение для рассылки',
                         'Посмотреть отложенные сообщения',
                         'Добавить админа'],
                        ['create_messages',
                         'show_delays_messages',
                         'add_admin'])
                    admin_start_message = "Привет, Админ. Что нужно сделать?"
                    VK.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=0,
                                keyboard = keyboard,
                                peer_id=event.obj.message['from_id'],
                                message=admin_start_message)

                    msg = event.obj.message['text']


                    if msg == 's':
                        # keyboard = VkKeyboard(inline=True)
                        # keyboard.add_line()
                        # keyboard.add_location_button('BTN')
                        # keyboard.add_button('BTN', VkKeyboardColor.SECONDARY)
                        # keyboard_1 = VkKeyboard(one_time=False, inline=True)
                        # keyboard_1 = gen_keyboard(['Откртыть Url', 'random'], ['own_type','o2'])
                        # keyboard_1.add_callback_button(label='Откртыть Url', color=VkKeyboardColor.POSITIVE, payload={"type": "callback_type_edit"})
                        # keyboard_1.add_line()

                        # send_text(id, 'hello', keyboard_1)
                        pass
                    if msg == 'p' or msg == 'п':
                        send_text(id, 'hello')
                        send_text(id, f"{id}")

                else:
                    #Обработка состояния
                    if state == States.S_SEND_AUDIO:
                        attach = 'audio{}_{}_{}'.format(
                            event.message['attachments'][0]['audio_message']['owner_id'],
                            event.message['attachments'][0]['audio_message']['id'],
                            event.message['attachments'][0]['audio_message']['access_key'],
                        )
                        # send_media(event.obj['message']['from_id'], attach)
                        # VK.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=event.message['attachments'])
                        print(f"FWD: {event.message['id']}")
                        # VK.messages.send(peer_id=id_admin, user_id = id_admin, random_id=0, forward_messages=[event.message['id']])
                        # for item in event.object['attachments']:
                            # if item['type'] == 'photo':
                                # send_photo1(event.user_id, 'photo{}_{}'.format(item['owner_id'], item['id']))
                        # attachments = ''
                        # count_photos = len(event.message['attachments'])
                        # for i in range(count_photos):
                        #     attachments +='photo{}_{}_{}'.format(
                        #         event.message['attachments'][i]['photo']['owner_id'],
                        #         event.message['attachments'][i]['photo']['id'],
                        #         event.message['attachments'][i]['photo']['access_key'])
                        #     if i != count_photos-1:
                        #         attachments += ','

                        # send_photo1(event.obj['message']['from_id'], attachments)
                    processing_state(event, id, state)

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            #TODO add try catch
            print(event.object.payload.get('type'))
            print(event.obj['user_id'])
            getattr(bh, event.object.payload.get('type'))(int(event.obj['user_id']), event.obj.conversation_message_id)

    except:
        print('stop_bot')
        break
