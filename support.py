from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import globals
import datetime
from vk_api.utils import get_random_id

def send_media(peer_id, attachments, msg='',keyboard = None, edit = False, message_id = 0, forward_message=''):
    random_id=get_random_id()
    if keyboard == None:
        if edit:
            globals.VK.messages.edit(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            globals.VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, forward_messages=forward_message)
    else:
        if edit:
            globals.VK.messages.edit(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, keyboard=keyboard, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            globals.VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, keyboard=keyboard, forward_messages=forward_message)

def send_msg(peer_id, msg, keyboard = None, edit = False, message_id = 0, forward_message=''):
    random_id=get_random_id()
    if keyboard == None:
        if edit:
            globals.VK.messages.edit(peer_id=peer_id, message=msg, random_id=random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:
            globals.VK.messages.send(peer_id=peer_id, message=msg, random_id=random_id, forward_messages=forward_message)
    else:
        if edit:
            globals.VK.messages.edit(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id, conversation_message_id = message_id, forward_messages=forward_message)
        else:    
            globals.VK.messages.send(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id, forward_messages=forward_message)

def get_keyboard_edit_start_message():
    return gen_keyboard([
                        'Добавить фото',
                        'Добавить видео',
                        'Добавить аудио',
                        'Готово',
                        'Назад'],
                        [
                        'add_photo_start',
                        'add_video_start',
                        'add_audio_start',
                        'apply_edit_msg_start',
                        'back_enter_message_start'])


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
                        'back_enter_message'])

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

def send_start_message(id, edit = False, message_id=0):
    keyboard = gen_keyboard(
                        ['Сообщение для рассылки',
                         'Отложенные сообщения',
                         'Админы',
                         'Стартовое сообщение'],
                        ['create_messages',
                         'show_delays_messages',
                         'operations_admin',
                         'update_start_message'])
    admin_start_message = "Привет, Админ. Что нужно сделать?"

    send_msg(id, admin_start_message, keyboard, edit, message_id, 0)