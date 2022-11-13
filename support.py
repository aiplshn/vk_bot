from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from globals import *

def send_media(peer_id, attachments, msg='',keyboard = None, random_id=0,):
    if keyboard == None:
        VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id)
    else:
        VK.messages.send(peer_id=peer_id, message=msg, attachment= attachments, random_id = random_id, keyboard=keyboard)

def send_msg(peer_id, msg, keyboard = None, edit = False, message_id = 0, random_id=0, ):
    if keyboard == None:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, random_id=random_id, conversation_message_id = message_id)
        else:
            VK.messages.send(peer_id=peer_id, message=msg, random_id=random_id)
    else:
        if edit:
            VK.messages.edit(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id, conversation_message_id = message_id)
        else:    
            VK.messages.send(peer_id=peer_id, message=msg, keyboard=keyboard, random_id=random_id)

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