class States():
    S_START = 0  # Начало нового диалога
    S_SEND_TEXT = 1 # отправка текста
    S_SEND_VIDEO = 2 # отправка видео
    S_SEND_PIC = 3 # отправка фото
    S_SEND_AUDIO = 4 # отправка аудио
    S_START_ADD_ADMIN = 5 # добавление админа
    S_SHOW_DELAY = 6 # показать отложенные