from config import States
from globals import *
from support import *
import datetime

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


def apply_edit_msg(id, message_id):
    attach = DB.get_last_attachments(id)
    msg = DB.get_last_message(id)
    if msg == '' and attach == '':
        send_msg(id, 'Ничего не добавлено!')
        return
    
    keyboard = gen_keyboard(['Отправить сейчас',
                             'Отложить',
                             'Назад'],
                            ['send_now',
                             'delay_message',
                             'back_send_to_edit'])


    send_msg(id, 'Принято. Выберите дальнейшее действие:',keyboard=keyboard)


def send_now(id, message_id):
    send_msg(id, 'Ожидай...', edit=True, message_id=message_id)
    attach = DB.get_last_attachments(id)
    msg = DB.get_last_message(id)
    mailing(msg, attachments=attach, db=DB)
    send_msg(id, 'Готово!')
    DB.update_state(id, States.S_START)
    DB.delete_message_for_admin(id)

def delay_message(id, message_id):
    delay_message_set_datetime(id, message_id)
    DB.update_state(id, States.S_DATE_TIME)

def delay_today(id, message_id):
    delay_message_set_time_today(id, message_id)
    DB.update_state(id, States.S_TIME_TODAY)

def delay_tomorrow(id, message_id):
    delay_message_set_time_tomorrow(id, message_id)
    DB.update_state(id, States.S_TIME_TOMORROW)

def delay_day_after(id, message_id):
    delay_message_set_time_day_after(id, message_id)
    DB.update_state(id, States.S_TIME_AFTER_TOMORROW)

def show_message(delay_message, id, message_id, edit=True):
    keyboard = gen_keyboard(['Следующее',
                              'Предыдущее',
                              'Изменить время',
                              'Удалить сообщение',
                              'Назад'],
                             ['next_show_delay_message',
                              'prev_show_delay_message',
                              'delay_message_for_show',
                              'delete_delay_message',
                              'back_to_start'])
    dt = datetime.datetime.strptime(delay_message[5], "%Y-%m-%d %H:%M:%S")
    info = f"Дата и время рассылки: {dt.day}.{dt.month}.{dt.year} {dt.hour}:{dt.minute}\n----------\n"+delay_message[1]
    if delay_message[2] != None:
        send_media(id, delay_message[2], info, keyboard, edit=edit, message_id=message_id)
    else:
        send_msg(id, info, keyboard, edit=edit, message_id=message_id)
    DB.update_id_show_delay_message(id, delay_message[0])


def show_delays_messages(id, message_id):
    delay_message = DB.get_next_delay_message(id)
    if len(delay_message) == 0:
        keyboard1 = gen_keyboard(['Назад'],
                                 ['back_to_start'])
        send_msg(id, 'Нет отложенных сообщений', keyboard=keyboard1, edit=True, message_id=message_id)
        return
    DB.update_state(id, States.S_SHOW_DELAY)
    show_message(delay_message, id, message_id)
    

def next_show_delay_message(id, message_id):
    delay_message = DB.get_next_delay_message(id)
    keyboard = gen_keyboard(['Предыдущее',
                              'Назад'],
                             ['prev_show_delay_message',
                              'back_to_start'])
    if len(delay_message) == 0:
        send_msg(id, 'Дальше нет отложенных сообщений', keyboard=keyboard, edit=True, message_id=message_id)
        DB.update_id_show_delay_message(id, -1)
        return
    show_message(delay_message, id, message_id)

def prev_show_delay_message(id, message_id):
    delay_message = DB.get_prev_delay_message(id)
    keyboard = gen_keyboard(['Следующее',
                              'Назад'],
                             ['next_show_delay_message',
                              'back_to_start'])
    if len(delay_message) == 0:
        send_msg(id, 'Это первое сообщение', keyboard=keyboard, edit=True, message_id=message_id)
        DB.update_id_show_delay_message(id, 0)
        return
    show_message(delay_message, id, message_id)


def add_audio(id, message_id):
    DB.update_state(id, States.S_SEND_AUDIO)
    send_msg(id, 'Отправь голосовое', edit=True, message_id=message_id)

def delay_message_for_show(id, message_id):
    DB.update_state(id, States.S_DATE_TIME_DELAY)
    delay_message_set_datetime(id, message_id, True)

def delay_message_for_show(id, message_id):
    delay_message_set_datetime(id, message_id, True)
    DB.update_state(id, States.S_DATE_TIME_DELAY)

def delay_today_for_show(id, message_id):
    delay_message_set_time_today(id, message_id, True)
    DB.update_state(id, States.S_TIME_TODAY_DELAY)

def delay_tomorrow_for_show(id, message_id):
    delay_message_set_time_tomorrow(id, message_id, True)
    DB.update_state(id, States.S_TIME_TOMORROW_DELAY)

def delay_day_after_for_show(id, message_id):
    delay_message_set_time_day_after(id, message_id, True)
    DB.update_state(id, States.S_TIME_AFTER_TOMORROW_DELAY)