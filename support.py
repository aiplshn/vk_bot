from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from globals import *
import datetime

def send_media(peer_id, attachments, msg='',keyboard = None, random_id=0, edit = False, message_id = 0, forward_message=''):
    if keyboard == None:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, forward_messages=forward_message)
    else:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, keyboard=keyboard, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, keyboard=keyboard, forward_messages=forward_message)

def send_msg(peer_id, msg, keyboard = None, edit = False, message_id = 0, random_id=0, forward_message=''):
    if keyboard == None:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, random_id=random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            VK.messages.send(peer_id=peer_id, message=msg, random_id=random_id, forward_messages=forward_message)
    else:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:    
            VK.messages.send(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id, forward_messages=forward_message)

def get_keyboard_edit_message():
    return gen_keyboard([
                        'Добавить фото',
                        'Добавить видео',
                        'Добавить аудио',
                        'Готово',
                        'Назад'],
                        [
                        'add_photo',
                        'add_video',
                        'add_audio',
                        'apply_edit_msg',
                        'back_messages'])

def gen_keyboard(labels, type_edits, vk_colors=None):
    rows = len(labels)
    if rows < 1 or rows != len(type_edits):
        return VkKeyboard()
    keyboard = VkKeyboard(one_time=False, inline=True)
    for i in range(rows):
        color = VkKeyboardColor.POSITIVE
        if vk_colors != None:
            color = vk_colors[i]
        keyboard.add_callback_button(label=labels[i], color=color, payload={"type": f"{type_edits[i]}"})
        if i != rows-1:
            keyboard.add_line()
    return keyboard.get_keyboard()

def mailing(msg, attachments, forward_message, db):
    ids = db.get_all_users()
    for id_users in ids:
        if attachments != '':
            send_media(id_users[0], attachments, msg, forward_message=forward_message)
        else:
            send_msg(id_users[0], msg=msg, forward_message=forward_message)

def check_format_datetime(dt: str):
    try:
        date_time_msg = datetime.datetime.strptime(dt, "%d.%m.%Y %H:%M")
        return date_time_msg
    except:
        return None

def delay_message_set_datetime(id, message_id, show=False):
    suffix = ''
    if show:
        suffix = '_for_show'
    keyboard = gen_keyboard(['*Ввод даты',
                             'Сегодня',
                             'Завтра',
                             'Послезавтра',
                             'Назад'],
                            ['delay_message'+suffix,
                             'delay_today'+suffix,
                             'delay_tomorrow'+suffix,
                             'delay_day_after'+suffix,
                             'back_delay'+suffix])
    send_msg(id,
             "Выберите когда отправить или введите дату и время в формате 'ДД.ММ.ГГГГ ЧЧ:мм'.",
             keyboard=keyboard, edit=True, message_id=message_id)

def delay_message_set_time_today(id, message_id, show=False):
    suffix = ''
    if show:
        suffix = '_for_show'
    keyboard = gen_keyboard(['Ввод даты',
                             '*Сегодня',
                             'Завтра',
                             'Послезавтра',
                             'Назад'],
                            ['delay_message'+suffix,
                             'delay_today'+suffix,
                             'delay_tomorrow'+suffix,
                             'delay_day_after'+suffix,
                             'back_delay'+suffix])
    send_msg(id,
             "Введите время в формате 'ЧЧ:мм'.",
             keyboard=keyboard, edit=True, message_id=message_id)

def delay_message_set_time_tomorrow(id, message_id, show=False):
    suffix = ''
    if show:
        suffix = '_for_show'
    keyboard = gen_keyboard(['Ввод даты',
                             'Сегодня',
                             '*Завтра',
                             'Послезавтра',
                             'Назад'],
                            ['delay_message'+suffix,
                             'delay_today'+suffix,
                             'delay_tomorrow'+suffix,
                             'delay_day_after'+suffix,
                             'back_delay'+suffix])
    send_msg(id,
             "Введите время в формате 'ЧЧ:мм'.",
             keyboard=keyboard, edit=True, message_id=message_id)

def delay_message_set_time_day_after(id, message_id, show=False):
    suffix = ''
    if show:
        suffix = '_for_show'
    keyboard = gen_keyboard(['Ввод даты',
                             'Сегодня',
                             'Завтра',
                             '*Послезавтра',
                             'Назад'],
                            ['delay_message'+suffix,
                             'delay_today'+suffix,
                             'delay_tomorrow'+suffix,
                             'delay_day_after'+suffix,
                             'back_delay'+suffix])
    send_msg(id,
             "Введите время в формате 'ЧЧ:мм'.",
             keyboard=keyboard, edit=True, message_id=message_id)