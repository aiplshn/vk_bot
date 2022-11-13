from config import States
from globals import *
from support import *

def own_type(user_id):
    print('success')

def create_messages(user_id, message_id):
    #get state
    state = DB.get_admin_state(user_id)
    if user_id == -1:
        return
    elif state == States.S_START:

       
        keyboard = gen_keyboard([
                                'Без текста',
                                'Назад'],
                                [
                                'send_without_text',
                                'back_messages'])
        DB.update_state(user_id, States.S_SEND_TEXT)
        VK.messages.edit(
                        user_id=user_id,
                        random_id=0,
                        keyboard = keyboard,
                        peer_id=user_id,
                        conversation_message_id = message_id,
                        message='Напиши любое текстовое сообщение без вложений')
    #switch case state
    #call func
    print('created')

def add_photo(user_id, message_id):
    add_media(user_id, message_id, States.S_SEND_PIC, 'Отправь одно или несколько фото', 'back_send_photo')
    print('photo added')

def show_delays_messages(user_id):
    print('show delay msg')

def add_admin(user_id):
    print('add admin')

def add_video(user_id, message_id):
    add_media(user_id, message_id, States.S_SEND_VIDEO, 'Отправь одно или несколько видео', 'back_send_video')
    print('video added')

def add_media(user_id, message_id, state, message, callback_name_back_btn):
    DB.update_state(user_id, state)
    keyboard = gen_keyboard(['Назад'], [callback_name_back_btn])
    VK.messages.edit(
                    user_id=user_id,
                    random_id=0,
                    keyboard = keyboard,
                    peer_id=user_id,
                    conversation_message_id = message_id,
                    message=message)

def send_without_text(id, message_id):
    DB.update_state(id, States.S_WAIT)
    DB.save_text_message('',id)
    keyboard = get_keyboard_edit_message()
    VK.messages.edit(
                    user_id=id,
                    random_id=0,
                    keyboard = keyboard,
                    peer_id=id,
                    conversation_message_id = message_id,
                    message='Выбери действие:')