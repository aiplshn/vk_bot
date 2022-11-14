from config import *
from support import *
from globals import *
import datetime

def processing_state(event, user_id, state):
    if state == States.S_SEND_TEXT:
        save_text(user_id, event.obj.message['text'])
    elif state == States.S_SEND_PIC:
        #TODO проверка на фото
        save_media(user_id, collect_attachments(event, 'photo'))
    elif state == States.S_SEND_VIDEO:
        #TODO проверка на видео
        save_media(user_id, collect_attachments(event, 'video'))
    elif state == States.S_SEND_AUDIO:
        save_voise_message(user_id, event.message['id'])
    # elif state == States.S_SHOW_DELAY:
        # pass
    elif state == States.S_START_ADD_ADMIN:
        pass
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
    elif state == States.S_WAIT:
        click_on_btn(user_id)

def save_text(id, msg):
    keyboard = get_keyboard_edit_message()
    VK.messages.send(
                    user_id=id,
                    random_id=0,
                    keyboard = keyboard,
                    peer_id=id,
                    message=msg)
    DB.save_text_message(msg, id)
    DB.update_state(id, States.S_WAIT)


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
    msg = DB.get_last_message(id)
    keyboard = get_keyboard_edit_message()
    attach_new = DB.save_media(id, attachments)
    send_media(id, attach_new, msg, keyboard)
    DB.update_state(id, States.S_WAIT)

def click_on_btn(id):
    send_msg(id, 'Выбери действие')

def save_date_time(id, datetime_str, show = False):
    date_time_msg = check_format_datetime(datetime_str)
    if date_time_msg != None:
        if show:
            DB.update_datetime_message(id, str(date_time_msg))
            DB.update_id_show_delay_message(id, 0)
        else:
            DB.update_datetime_message_edit(id,str(date_time_msg))
        DB.update_state(id, States.S_START)
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
            DB.update_datetime_message(id, str(date_time_msg))
            DB.update_id_show_delay_message(id, 0)
        else:
            DB.update_datetime_message_edit(id,str(date_time_msg))
        DB.update_state(id, States.S_START)
        send_msg(id, 'Готово')
    else:
        send_msg(id, "Неверный формат. Введите в формате 'ЧЧ:мм'.")


def save_voise_message(id, id_message):
    DB.update_audio_message(id, id_message)
    attach = DB.get_last_attachments(id)
    msg = DB.get_last_message(id)
    keyboard = get_keyboard_edit_message()
    send_media(id, attach, msg, keyboard, forward_message=str(id_message))