from states import *
from support import *
import globals
import datetime

def processing_state(event, state):
    user_id = event.obj.message['from_id']
    if state == States.S_START:
        send_start_message(user_id)
    elif state == States.S_SEND_TEXT:
        if check_content_type(event, 'text'):
            save_text(user_id, event.obj.message['text'])
        else:
            send_msg(user_id, 'Отправь только текст')
    elif state == States.S_SEND_PIC:
        if check_content_type(event, 'photo'):
            save_media(user_id, collect_attachments(event, 'photo'))
        else:
            send_msg(user_id, 'Отправь только фото')
    elif state == States.S_SEND_VIDEO:
        if check_content_type(event, 'video'):
            save_media(user_id, collect_attachments(event, 'video'))
        else:
            send_msg(user_id, 'Отправь только видео')
    elif state == States.S_SEND_AUDIO:
        save_voise_message(user_id, event.message['id'])
    elif state == States.S_ADD_NEW_ADMIN:
        save_new_admin(event)
    elif state == States.S_DELETE_ADMIN:
        delete_from_admin(event)
    elif state == States.S_DATE_TIME:
        save_date_time(user_id, event.obj.message['text'])
    elif state == States.S_TIME_TODAY:
        save_time(user_id, event.obj.message['text'], 0)
    elif state == States.S_TIME_TOMORROW:
        save_time(user_id, event.obj.message['text'], 1)
    elif state == States.S_TIME_AFTER_TOMORROW:
        save_time(user_id, event.obj.message['text'], 2)

    elif state == States.S_DATE_TIME_DELAY:
        save_date_time(user_id, event.obj.message['text'], True)
    elif state == States.S_TIME_TODAY_DELAY:
        save_time(user_id, event.obj.message['text'], 0, True)
    elif state == States.S_TIME_TOMORROW_DELAY:
        save_time(user_id, event.obj.message['text'], 1, True)
    elif state == States.S_TIME_AFTER_TOMORROW_DELAY:
        save_time(user_id, event.obj.message['text'], 2, True)        
    elif state == States.S_UPDATE_START_MESSAGE:
        save_text_start_message(user_id, event.obj.message['text'])
    elif state == States.S_SEND_PIC_START_MESSAGE:
        save_media_start_message(user_id, collect_attachments(event, 'photo'))
    elif state == States.S_SEND_VIDEO_START_MESSAGE:
        save_media_start_message(user_id, collect_attachments(event, 'video'))
    elif state == States.S_SEND_AUDIO_START_MESSAGE:
        save_voise_start_message(user_id, event.message['id'])
    elif state == States.S_WAIT:
        click_on_btn(user_id)

def check_content_type(event, type) -> bool:
    if type == 'text':
        if type in event.obj.message:
            if event.obj.message['text'] != '':
                return True
    elif type == 'photo' or type == 'video':
        if 'attachments' in event.message:
            count_photos = len(event.message['attachments'])
            for i in range(count_photos):
                if type not in event.message['attachments'][i]:
                    return False
                return True
    return False
    


def save_text(id, msg):
    keyboard = get_keyboard_edit_message()
    globals.VK.messages.send(
                    user_id=id,
                    random_id=get_random_id(),
                    keyboard = keyboard,
                    peer_id=id,
                    message=msg)
    globals.DB.save_text_message(msg, id)
    globals.DB.update_state(id, States.S_WAIT)


def collect_attachments(event, media_type) -> str:
    attachments = ''
    count_photos = len(event.message['attachments'])
    for i in range(count_photos):
        attachments +='{}{}_{}_{}'.format(
            media_type,
            event.message['attachments'][i][media_type]['owner_id'],
            event.message['attachments'][i][media_type]['id'],
            event.message['attachments'][i][media_type]['access_key'])
        if i != count_photos-1:
            attachments += ','
    print(attachments)
    return attachments

def save_media(id, attachments):
    msg = globals.DB.get_last_message(id)
    keyboard = get_keyboard_edit_message()
    attach_new = globals.DB.save_media(id, attachments)
    send_media(id, attach_new, msg, keyboard)#TODO add fwd_msg
    globals.DB.update_state(id, States.S_WAIT) 

def save_media_start_message(id, attachments):
    msg = globals.DB.get_start_message()[1]
    keyboard = get_keyboard_edit_start_message()
    attach_new = globals.DB.set_media_for_start_message(attachments)
    send_media(id, attach_new, msg, keyboard)
    globals.DB.update_state(id, States.S_WAIT)

def click_on_btn(id):
    send_msg(id, 'Выбери действие')

def save_date_time(id, datetime_str, show = False):
    date_time_msg = check_format_datetime(datetime_str)
    if date_time_msg != None:
        if show:
            globals.DB.update_datetime_message(id, str(date_time_msg))
            globals.DB.update_id_show_delay_message(id, 0)
        else:
            globals.DB.update_datetime_message_edit(id,str(date_time_msg))
        globals.DB.update_state(id, States.S_START)
        send_msg(id, 'Готово')
    else:
        send_msg(id, "Неверный формат. Введите в формате 'ДД.ММ.ГГГГ ЧЧ:мм'.")

def save_time(id, time_str, day_delay, show = False): #day_delay 0 - сегодня 1 - завтра 2 - послезавтра
    date_delay = datetime.datetime.now()
    date_delay = date_delay + datetime.timedelta(days=day_delay)
    datetime_str = f"{date_delay.day}.{date_delay.month}.{date_delay.year} " + time_str
    date_time_msg = check_format_datetime(datetime_str)
    if date_time_msg != None:
        if show:
            globals.DB.update_datetime_message(id, str(date_time_msg))
            globals.DB.update_id_show_delay_message(id, 0)
        else:
            globals.DB.update_datetime_message_edit(id,str(date_time_msg))
        globals.DB.update_state(id, States.S_START)
        send_msg(id, 'Готово')
    else:
        send_msg(id, "Неверный формат. Введите в формате 'ЧЧ:мм'.")


def save_voise_message(id, id_message):
    globals.DB.update_audio_message(id, id_message)
    attach = globals.DB.get_last_attachments(id)
    msg = globals.DB.get_last_message(id)
    keyboard = get_keyboard_edit_message()
    send_media(id, attach, msg, keyboard, forward_message=str(id_message))

def save_voise_start_message(id, id_message):
    globals.DB.set_voise_message_for_start_message(id_message)
    start_msg = globals.DB.get_start_message()
    attach = start_msg[2]
    msg = start_msg[1]
    keyboard = get_keyboard_edit_start_message()
    send_media(id, attach, msg, keyboard, forward_message=str(id_message))
 

def save_new_admin(event):
    from_id = event.obj.message['from_id']
    id_new_admin = check_admin_operation(event)
    if id_new_admin == -1:
        fail_check_admin(from_id, False)
    else:
        if globals.DB.is_admin(id_new_admin):
            keyboard = gen_keyboard(['Назад'],
                                    ['back_to_admin_operations'])
            send_msg(from_id, 'Админ уже добавлен', keyboard)
        else:
            globals.DB.add_new_admin(id_new_admin)
            send_msg(from_id, 'Готово')
            globals.DB.update_state(from_id, States.S_START)
            send_start_message(from_id)


def delete_from_admin(event):
    from_id = event.obj.message['from_id']
    id_delete_admin = check_admin_operation(event)
    if id_delete_admin == -1:
        fail_check_admin(from_id, False)
    else:
        if globals.DB.is_admin(id_delete_admin):
            globals.DB.delete_admin(id_delete_admin)
            send_msg(from_id, 'Готово')
            globals.DB.update_state(from_id, States.S_START)
            send_start_message(from_id)
        else:
            keyboard = gen_keyboard(['Назад'],
                                    ['back_to_admin_operations'])
            send_msg(from_id, 'Такого админа нет', keyboard)

        

def check_admin_operation(event) -> int:
    try:
        id_admin = event.message['fwd_messages'][0]['from_id']
        if id_admin <= 0:
            raise
        return id_admin
    except:
        return -1

def fail_check_admin(id, del_add: bool): # del_add = True - del, False - add
    action = ''
    if del_add:
        action = 'удалить'
    else:
        action = 'добавить'    
    send_msg(id, f"Не удалось {action} админа.\nПерешлите любое сообщение от человека, которого хотите добавить")

def save_text_start_message(id, text):
    globals.DB.set_text_start_message(text)
    globals.DB.update_state(id, States.S_WAIT)
    keyboard = get_keyboard_edit_start_message()
    send_msg(id, text, keyboard)