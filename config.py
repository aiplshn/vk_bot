class States():
    S_START = 0  # Начало нового диалога
    S_SEND_TEXT = 1 # отправка текста
    S_SEND_VIDEO = 2 # отправка видео
    S_SEND_PIC = 3 # отправка фото
    S_SEND_AUDIO = 4 # отправка аудио
    S_START_ADD_ADMIN = 5 # добавление админа
    S_SHOW_DELAY = 6 # показать отложенные
    S_WAIT = 7 # ждем нажатия на кнопку
    S_DATE_TIME = 8 #отправка даты и времени
    S_TIME_TODAY = 9 #отправка времени сегодня
    S_TIME_TOMORROW = 10 #отправка времени завтра
    S_TIME_AFTER_TOMORROW = 11 #отправка времени послезавтра