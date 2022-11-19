from states import States
import globals 
from support import *
import datetime
from vk_api.utils import get_random_id

def own_type(user_id):
    print('success')

def create_messages(user_id, message_id):
    #get state
    state = globals.DB.get_admin_state(user_id)
    if user_id == -1:
        return
    elif state == States.S_START:

       
        keyboard = gen_keyboard([
                                'Без текста',
                                'Назад'],
                                [
                                'send_without_text',
                                'back_to_start'])
        globals.DB.update_state(user_id, States.S_SEND_TEXT)
        send_msg(user_id, 'Напиши любое текстовое сообщение без вложений', keyboard, True, message_id, 0)
    print('created')

def add_photo(user_id, message_id):
    add_media(user_id, message_id, States.S_SEND_PIC, 'Отправь одно или несколько фото', 'back_send_to_edit')
    print('photo added')

def operations_admin(id, message_id):
    keyboard = gen_keyboard(['Добавить нового',
                             'Удалить',
                             'Назад'],
                            ['add_new_admin',
                             'delete_admin',
                             'back_to_start'])
    send_msg(id, 'Выбери действие', keyboard, edit=True, message_id=message_id)
    # send_msg(id, 'Перешли любое сообщение от человека, которого нужно добавить в админы.',
    #          keyboard, edit=True, message_id=message_id)
    globals.DB.update_state(id, States.S_WAIT)
    print('operations admin')

def add_video(user_id, message_id):
    add_media(user_id, message_id, States.S_SEND_VIDEO, 'Отправь одно или несколько видео', 'back_send_to_edit')
    print('video added')

def add_media(user_id, message_id, state, message, callback_name_back_btn):
    globals.DB.update_state(user_id, state)
    keyboard = gen_keyboard(['Назад'], [callback_name_back_btn])
    globals.VK.messages.edit(
                    user_id=user_id,
                    random_id=get_random_id(),
                    keyboard = keyboard,
                    peer_id=user_id,
                    conversation_message_id = message_id,
                    message=message)

def send_without_text(id, message_id):
    globals.DB.update_state(id, States.S_WAIT)
    globals.DB.save_text_message('',id)
    keyboard = get_keyboard_edit_message()
    globals.VK.messages.edit(
                    user_id=id,
                    random_id=get_random_id(),
                    keyboard = keyboard,
                    peer_id=id,
                    conversation_message_id = message_id,
                    message='Выбери действие:')


def apply_edit_msg(id, message_id):
    attach = globals.DB.get_last_attachments(id)
    msg = globals.DB.get_last_message(id)
    forward_message = globals.DB.get_id_forward_message(id)
    if msg == '' and attach == '' and forward_message == '':
        send_msg(id, 'Ничего не добавлено!')
        return
    
    keyboard = gen_keyboard(['Отправить сейчас',
                             'Отложить',
                             'Назад'],
                            ['send_now',
                             'delay_message',
                             'back_send_to_edit'])


    send_msg(id, 'Принято. Выберите дальнейшее действие:',keyboard=keyboard, edit=True, message_id=message_id)


def send_now(id, message_id):
    send_msg(id, 'Ожидай...', edit=True, message_id=message_id)
    attach = globals.DB.get_last_attachments(id)
    msg = globals.DB.get_last_message(id)
    fwd_msg = globals.DB.get_id_forward_message(id)
    mailing(msg, attachments=attach,forward_message=fwd_msg, db=globals.DB)
    send_msg(id, 'Готово!')
    globals.DB.update_state(id, States.S_START)
    globals.DB.delete_message_for_admin_edit(id)

def delay_message(id, message_id):
    delay_message_set_datetime(id, message_id)
    globals.DB.update_state(id, States.S_DATE_TIME)

def delay_today(id, message_id):
    delay_message_set_time_today(id, message_id)
    globals.DB.update_state(id, States.S_TIME_TODAY)

def delay_tomorrow(id, message_id):
    delay_message_set_time_tomorrow(id, message_id)
    globals.DB.update_state(id, States.S_TIME_TOMORROW)

def delay_day_after(id, message_id):
    delay_message_set_time_day_after(id, message_id)
    globals.DB.update_state(id, States.S_TIME_AFTER_TOMORROW)

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
    if delay_message[3] != '':
        edit = False
    if delay_message[2] != '':
        send_media(id, delay_message[2], info, keyboard, edit=edit, message_id=message_id, forward_message=str(delay_message[3]))
    else:
        send_msg(id, info, keyboard, edit=edit, message_id=message_id, forward_message=str(delay_message[3]))
    globals.DB.update_id_show_delay_message(id, delay_message[0])


def show_delays_messages(id, message_id):
    delay_message = globals.DB.get_next_delay_message(id)
    if len(delay_message) == 0:
        keyboard1 = gen_keyboard(['Назад'],
                                 ['back_to_start'])
        send_msg(id, 'Нет отложенных сообщений', keyboard=keyboard1, edit=True, message_id=message_id)
        return
    globals.DB.update_state(id, States.S_WAIT)
    show_message(delay_message, id, message_id)
    

def next_show_delay_message(id, message_id):
    delay_message = globals.DB.get_next_delay_message(id)
    keyboard = gen_keyboard(['Предыдущее',
                              'Назад'],
                             ['prev_show_delay_message',
                              'back_to_start'])
    if len(delay_message) == 0:
        send_msg(id, 'Дальше нет отложенных сообщений', keyboard=keyboard, edit=True, message_id=message_id)
        globals.DB.update_id_show_delay_message(id, -1)
        return
    show_message(delay_message, id, message_id)

def prev_show_delay_message(id, message_id):
    delay_message = globals.DB.get_prev_delay_message(id)
    keyboard = gen_keyboard(['Следующее',
                              'Назад'],
                             ['next_show_delay_message',
                              'back_to_start'])
    if len(delay_message) == 0:
        send_msg(id, 'Это первое сообщение', keyboard=keyboard, edit=True, message_id=message_id)
        globals.DB.update_id_show_delay_message(id, 0)
        return
    show_message(delay_message, id, message_id)


def add_audio(id, message_id):
    add_media(id, message_id, States.S_SEND_AUDIO, 'Отправь голосовое', 'back_send_to_edit')
    # globals.DB.update_state(id, States.S_SEND_AUDIO)
    # send_msg(id, 'Отправь голосовое', edit=True, message_id=message_id)

def delay_message_for_show(id, message_id):
    globals.DB.update_state(id, States.S_DATE_TIME_DELAY)
    delay_message_set_datetime(id, message_id, True)

def delay_message_for_show(id, message_id):
    delay_message_set_datetime(id, message_id, True)
    globals.DB.update_state(id, States.S_DATE_TIME_DELAY)

def delay_today_for_show(id, message_id):
    delay_message_set_time_today(id, message_id, True)
    globals.DB.update_state(id, States.S_TIME_TODAY_DELAY)

def delay_tomorrow_for_show(id, message_id):
    delay_message_set_time_tomorrow(id, message_id, True)
    globals.DB.update_state(id, States.S_TIME_TOMORROW_DELAY)

def delay_day_after_for_show(id, message_id):
    delay_message_set_time_day_after(id, message_id, True)
    globals.DB.update_state(id, States.S_TIME_AFTER_TOMORROW_DELAY)

def delete_delay_message(id, message_id):
    globals.DB.delete_message_for_admin_edit(id)
    send_msg(id, 'Готово', edit=True, message_id=message_id)
    globals.DB.update_state(id, States.S_START)

def back_to_start(id, message_id):
    globals.DB.update_state(id, States.S_START)
    globals.DB.update_id_show_delay_message(id, 0)
    send_start_message(id, True, message_id)
    
def back_send_to_edit(id, message_id):
    msg = globals.DB.get_last_message(id)
    keyboard = get_keyboard_edit_message()
    attach_new = globals.DB.get_last_attachments(id)
    fwd_msg = globals.DB.get_id_forward_message(id)
    if fwd_msg == '' or fwd_msg == None:
        send_media(id, attach_new, msg, keyboard, edit=True, message_id=message_id, forward_message=fwd_msg)
    else:
        send_media(id, attach_new, msg, keyboard, forward_message=fwd_msg)

def back_enter_message(id, message_id):
    globals.DB.delete_message_for_admin_edit(id)
    globals.DB.update_state(id, States.S_START)
    create_messages(id, message_id)

def back_delay(id, message_id):
    apply_edit_msg(id, message_id)

def back_delay_for_show(id, message_id):
    globals.DB.update_id_show_delay_message(id, 0)
    show_delays_messages(id, message_id)

def add_new_admin(id, message_id):
    globals.DB.update_state(id, States.S_ADD_NEW_ADMIN)
    keyboard = gen_keyboard(['Назад'],
                            ['back_to_admin_operations'])
    send_msg(id, 'Перешли любое сообщение от человека, которого нужно добавить в админы.',
             keyboard=keyboard, edit=True, message_id=message_id)

def delete_admin(id, message_id):
    globals.DB.update_state(id, States.S_DELETE_ADMIN)
    keyboard = gen_keyboard(['Назад'],
                            ['back_to_admin_operations'])
    send_msg(id, 'Перешли любое сообщение от админа, которого нужно удалить.',
             keyboard=keyboard, edit=True, message_id=message_id)


def back_to_admin_operations(id, message_id):
    globals.DB.update_state(id, States.S_WAIT)
    operations_admin(id, message_id)

def update_start_message(id, message_id):
    globals.DB.update_state(id, States.S_UPDATE_START_MESSAGE)
    keyboard = gen_keyboard(['Без текста',
                             'Назад'],
                            ['start_message_without_text',
                             'back_to_start_from_edit_start_message'])
    start_message = globals.DB.get_start_message()
    edit = True
    info = 'Напиши любое текстовое сообщение без вложений\nТекущее сообщение:\n---------\n'+str(start_message[1])
    if start_message[3] != None:
        edit = False
    if start_message[2] != '':
        send_media(id, start_message[2], info, keyboard, edit=edit, message_id=message_id, forward_message=str(start_message[3]))
    else:
        send_msg(id, info, keyboard, edit=edit, message_id=message_id, forward_message=str(start_message[3]))

def start_message_without_text(id, message_id):
    globals.DB.update_state(id, States.S_WAIT)
    globals.DB.set_text_start_message('')
    globals.DB.set_media_for_start_message('')
    globals.DB.set_voise_message_for_start_message('NULL')
    keyboard = get_keyboard_edit_start_message()
    send_msg(id, 'Выбери действие:', keyboard, edit=True, message_id=message_id)

# def add_photo_start(id, message_id):
    # globals.DB.update_state(id, States.S_SEND_PIC_START_MESSAGE)

def add_photo_start(id, message_id):
    add_media(id, message_id, States.S_SEND_PIC_START_MESSAGE, 'Отправь одно или несколько фото', 'back_send_to_edit_start_message')
    print('video added')
    
def add_video_start(id, message_id):
    add_media(id, message_id, States.S_SEND_VIDEO_START_MESSAGE, 'Отправь одно или несколько видео', 'back_send_to_edit_start_message')
    print('video added')

def add_audio_start(id, message_id):
    add_media(id, message_id, States.S_SEND_AUDIO_START_MESSAGE, 'Отправь голосовое', 'back_send_to_edit_start_message')
    print('video added')

def back_send_to_edit_start_message(id, message_id):
    start_msg = globals.DB.get_start_message()
    attach = start_msg[2]
    msg = start_msg[1]
    fwd_msg = start_msg[3]
    keyboard = get_keyboard_edit_start_message()
    if msg == '':
        msg = 'Выбери действие:'
    edit = True
    if fwd_msg != '':
        edit = False
    if attach != '':
        send_media(id, attach, msg, keyboard, edit=edit, message_id=message_id, forward_message=str(fwd_msg))
    else:
        send_msg(id, msg, keyboard, edit=edit, message_id=message_id, forward_message=str(fwd_msg))

def back_enter_message_start(id, message_id):
        update_start_message(id, message_id)

def back_to_start_from_edit_start_message(id, message_id):
    if check_start_msg():
        back_to_start(id, message_id)
    else:
        send_msg(id, 'Предыдущее сообщение удалено, введи новое!')

def apply_edit_msg_start(id, message_id):
    if check_start_msg():
        back_to_start(id, message_id)
    else:
        send_msg(id, 'Ничего не добавлено!')


def check_start_msg() -> bool:
    start_msg = globals.DB.get_start_message()
    attach = start_msg[2]
    msg = start_msg[1]
    fwd_msg = start_msg[3]
    if (attach == '' or attach == None) and msg == '' and fwd_msg == None:
        return False
    return True

def delete_media_start_message(id, message_id):
    msg = globals.DB.get_start_message()[1]
    keyboard = get_keyboard_edit_start_message()
    globals.DB.set_media_for_start_message('')
    globals.DB.set_voise_message_for_start_message('NULL')
    if msg == '':
        msg = 'Выбери действие:'
    send_msg(id, msg, keyboard, edit=True, message_id=message_id)
    globals.DB.update_state(id, States.S_WAIT)