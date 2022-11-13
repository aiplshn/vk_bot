from config import *
from support import *
from globals import *

def processing_state(event, user_id, state):
    if state == States.S_SEND_TEXT:
        save_text(event.obj.message['text'], user_id)
    elif state == States.S_SEND_PIC:
        #TODO проверка на фото
        save_photo(user_id, collect_attachments_for_photo(event))
    elif state == States.S_SEND_VIDEO:
        pass
    elif state == States.S_SEND_AUDIO:
        pass
    elif state == States.S_SHOW_DELAY:
        pass
    elif state == States.S_START_ADD_ADMIN:
        pass

def get_keyboard_edit_message():
    return gen_keyboard([
                        'Добавить фото',
                        'Добавить видео',
                        'Добавить аудио',
                        'Назад'],
                        [
                        'add_photo',
                        'add_video',
                        'add_audio',
                        'back_messages'])

def save_text(msg, user_id):
    keyboard = get_keyboard_edit_message()
    VK.messages.send(
                    user_id=user_id,
                    random_id=0,
                    keyboard = keyboard,
                    peer_id=user_id,
                    message=msg)
    DB.save_text_message(msg, user_id)


def collect_attachments_for_photo(event) -> str:
    attachments = ''
    count_photos = len(event.message['attachments'])
    for i in range(count_photos):
        attachments +='photo{}_{}_{}'.format(
            event.message['attachments'][i]['photo']['owner_id'],
            event.message['attachments'][i]['photo']['id'],
            event.message['attachments'][i]['photo']['access_key'])
        if i != count_photos-1:
            attachments += ','
    print(attachments)
    return attachments

def save_photo(id, attachments):
    msg = DB.get_message(id)
    keyboard = get_keyboard_edit_message()
    send_photo1(id, attachments, msg, keyboard)
    # DB.save_photo()