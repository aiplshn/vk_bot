# -*- coding: utf-8 -*-

class States():
    S_START = 0  # Начало нового диалога

    S_SEND_TEXT = 1 # отправка текста
    S_SEND_VIDEO = 2 # отправка видео
    S_SEND_PIC = 3 # отправка фото
    S_SEND_AUDIO = 4 # отправка аудио

    S_START_ADMIN = 5 # 
    S_SHOW_DELAY = 6 # показать отложенные
    
    S_WAIT = 7 # ждем нажатия на кнопку

    S_DATE_TIME = 8 #отправка даты и времени
    S_TIME_TODAY = 9 #отправка времени сегодня
    S_TIME_TOMORROW = 10 #отправка времени завтра
    S_TIME_AFTER_TOMORROW = 11 #отправка времени послезавтра

    S_DATE_TIME_DELAY = 12 #отправка даты и времени при просмотре отложенных
    S_TIME_TODAY_DELAY = 13 #отправка времени сегодня при просмотре отложенных
    S_TIME_TOMORROW_DELAY = 14 #отправка времени завтра при просмотре отложенных
    S_TIME_AFTER_TOMORROW_DELAY = 15 #отправка времени послезавтра при просмотре отложенных

    S_ADD_NEW_ADMIN = 16 # добавление админа
    S_DELETE_ADMIN = 17 # удаление админа

    S_UPDATE_START_MESSAGE = 18 #добавление нового сообщения
    # S_SEND_TEXT_START_MESSAGE = 19 # отправка текста стартового сообщения
    S_SEND_VIDEO_START_MESSAGE = 19 # отправка видео стартового сообщения
    S_SEND_PIC_START_MESSAGE = 20 # отправка фото стартового сообщения
    S_SEND_AUDIO_START_MESSAGE = 21 # отправка аудио стартового сообщения
