import sqlite3
import sys
import traceback

class admin:
    id: int
    state: int
    id_show_delay_message: int

    table_name = 'admin'

    def get_query_create_table(self) -> str:
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY NOT NULL, state INTEGER, id_show_delay_message INTEGER);"

    def get_query_drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.table_name}"

    def get_query_insert_into_table(self) -> str:
        return f"""INSERT INTO {self.table_name} VALUES ({self.id}, {self.state}, 0)"""

    def get_query_delete_all(self) -> str:
        return f"DELETE FROM {self.table_name}"

    def get_query_delete_from_id(self) -> str:
        return f"DELETE FROM {self.table_name} WHERE id = {self.id}"

    def get_query_is_admin(self) -> str:
        return f"SELECT COUNT() FROM {self.table_name} WHERE id = {self.id}"

    def get_query_state(self):
        return f"SELECT state FROM {self.table_name} WHERE id = {self.id}"

    def get_query_update_state(self):
        return f"UPDATE {self.table_name} SET state = {self.state} WHERE id = {self.id}"

    def get_query_update_show_message(self):
        return f"UPDATE {self.table_name} SET id_show_delay_message = {self.id_show_delay_message} WHERE id = {self.id}"

    def get_query_id_show_message(self) -> str:
        return f"SELECT id_show_delay_message FROM {self.table_name} WHERE id = {self.id}"

class user:
    id: int
    table_name = 'user'

    def get_query_create_table(self) -> str:
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY NOT NULL);"

    def get_query_drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.table_name}"

    def get_query_insert_into_table(self) -> str:
        return f"""INSERT INTO {self.table_name} VALUES ({self.id})"""

    def get_query_delete_all(self) -> str:
        return f"DELETE FROM {self.table_name}"
    
    def get_query_select_all_users(self) -> str:
        return f"SELECT * FROM {self.table_name}"

class message:
    id: int
    text: str
    media_attachments: str
    id_audio_message_str: str
    id_admin: int
    send_time: str
    table_name = 'message'

    def __init__(self) -> None:
        self.text = "''"
        self.media_attachments = "''" 
        self.id_audio_message_str = "''"
        self.send_time = "''"

    def get_query_create_table(self) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,text VARCHAR (2000),media_attachments VARCHAR (2000), id_audio_message_str VARCHAR (255), id_admin INTEGER REFERENCES admin (id), send_time  DATETIME);"""

    def get_query_drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.table_name}"

    def get_query_insert_into_table(self) -> str:
        return f"""INSERT INTO {self.table_name} (text, media_attachments, id_audio_message_str, id_admin) VALUES ({self.text}, {self.media_attachments}, {self.id_audio_message_str}, {self.id_admin})"""

    def get_query_delete_all(self) -> str:
        return f"DELETE FROM {self.table_name}"

    def get_query_last_message(self) -> str:
        return f"select * from {self.table_name} where id_admin = {self.id_admin} and id <= (select seq from sqlite_sequence where name = '{self.table_name}') order by id DESC LIMIT 1"

    def get_query_update_attachments(self) -> str:
        return f"UPDATE {self.table_name} SET media_attachments = '{self.media_attachments}' where id = {self.id}"

    def get_query_delete_last_message_for_admin(self) -> str:
        return f"DELETE FROM {self.table_name} WHERE id = (select id from {self.table_name} where id_admin = {self.id_admin} and id <= (select seq from sqlite_sequence where name = '{self.table_name}') order by id DESC LIMIT 1)"

    def get_query_delay_early_message(self) -> str:
        return f"select * from {self.table_name} WHERE datetime(send_time) IS NOT NULL ORDER BY send_time ASC LIMIT 1;"

    def get_query_delete_for_id(self) -> str:
        return f"DELETE FROM {self.table_name} WHERE id = {self.id}"

    def get_query_set_datetime_last_message(self) -> str:
        return f"UPDATE {self.table_name} SET send_time = '{self.send_time}' WHERE id = (select id from {self.table_name} where id_admin = {self.id_admin} and id <= (select seq from sqlite_sequence where name = '{self.table_name}') order by id DESC LIMIT 1)"

    def get_query_all_delay_messages(self) -> str:
        return f"SELECT * FROM {self.table_name} WHERE datetime(send_time) IS NOT NULL ORDER BY send_time ASC"

    def get_query_set_datetime_for_id(self) -> str:
        return f"UPDATE {self.table_name} SET send_time = '{self.send_time}' WHERE id = {self.id};"
    
    def get_query_update_id_voise_message(self) -> str:
        return f"UPDATE {self.table_name} SET id_audio_message_str = '{self.id_audio_message_str}' WHERE id = {self.id}"

class DBWorker:

    def update_state(self, id_admin, state):
        adm = admin()
        adm.id = id_admin
        adm.state = state
        self.execute_query(adm.get_query_update_state())

    def is_admin(self, id_admin: int) -> bool:
        adm = admin()
        adm.id = id_admin
        res = self.execute_query_select(adm.get_query_is_admin())
        return res[0][0] != 0

    def get_admin_state(self, id_admin) -> int:
        adm = admin()
        adm.id = id_admin
        if self.is_admin(id_admin):
            res = self.execute_query_select(adm.get_query_state())
            return int(res[0][0])
        else:
            return -1

    def drop_tables(self):
        adm = admin()
        usr = user()
        msg = message()
        self.execute_query(adm.get_query_drop_table())
        self.execute_query(usr.get_query_drop_table())
        self.execute_query(msg.get_query_drop_table())

    def execute_query_select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            self.connection.close()
            

    def execute_query(self, query: str):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            self.connection.close()

    def create_tables(self):
        adm = admin()
        usr = user()
        msg = message()
        self.execute_query(adm.get_query_create_table())
        self.execute_query(usr.get_query_create_table())
        self.execute_query(msg.get_query_create_table())

        #TODO DELETE
        adm.id = 54442110
        adm.state = 0
        self.execute_query(adm.get_query_insert_into_table())
        usr.id = 54442110
        self.execute_query(usr.get_query_insert_into_table())

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('vk_bot.db')
            self.cursor = self.connection.cursor()
            self.drop_tables() #TODO DELETE THIS
            res = self.execute_query_select("SELECT COUNT() FROM sqlite_master WHERE type='table';")
            if res[0][0] <= 1:
                self.create_tables()
        except sqlite3.Error as er:
            print("Ошибка при подключении к sqlite", er)
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            self.connection.close()


    def __del__(self):
        if(self.connection):
            self.connection.close()
            print("Connection closed")

    def add_new_admin(self, id_new_admin):
        adm = admin()
        adm.id = id_new_admin
        adm.state = 0
        self.execute_query(adm.get_query_insert_into_table())

    def delete_admin(self, id_delete_admin):
        adm = admin()
        adm.id = id_delete_admin
        self.execute_query(adm.get_query_delete_from_id())

    def save_text_message(self, text, id_admin):
        adm = admin()
        adm.id = id_admin
        msg = message()
        msg.id_admin = id_admin
        msg.text = "'"+text+"'"

        if self.is_admin(id_admin):
            print(msg.get_query_insert_into_table())
            self.execute_query(msg.get_query_insert_into_table())

    def get_last_message(self, id) -> str:
        msg = message()
        msg.id_admin = id
        last_msg = self.execute_query_select(msg.get_query_last_message())
        return last_msg[0][1]

    def save_media(self, id, attachments):
        msg = message()
        msg.id_admin = id
        last_msg = self.execute_query_select(msg.get_query_last_message())
        last_attachment = last_msg[0][2]
        id_msg = last_msg[0][0]
        msg.id = id_msg
        if last_attachment != '':
            msg.media_attachments = last_attachment + "," + attachments
        else:
            msg.media_attachments = attachments
        self.execute_query(msg.get_query_update_attachments())
        return msg.media_attachments

    def get_last_attachments(self, id):
        msg = message()
        msg.id_admin = id
        last_msg = self.execute_query_select(msg.get_query_last_message())
        return last_msg[0][2]

    def get_all_users(self):
        usr = user()
        return self.execute_query_select(usr.get_query_select_all_users())

    def delete_message_for_admin_edit(self, id):
        msg = message()
        msg.id_admin = id
        self.execute_query(msg.get_query_delete_last_message_for_admin())

    def get_early_delay_message(self):
        msg = message()
        return self.execute_query_select(msg.get_query_delay_early_message())
        
    def delete_message_for_it_id(self, id):
        msg = message()
        msg.id = id
        self.execute_query(msg.get_query_delete_for_id())

    def update_datetime_message_edit(self, id: int, send_time: str):
        msg = message()
        msg.id_admin = id
        msg.send_time = send_time
        self.execute_query(msg.get_query_set_datetime_last_message())

    def update_datetime_message(self, id_admin: int, send_time: str):
        id_message = self.get_id_show_delay_message(id_admin)[0][0]
        msg = message()
        msg.id = id_message
        msg.send_time = send_time
        self.execute_query(msg.get_query_set_datetime_for_id())

    def get_next_delay_message(self, id):
        adm = admin()
        adm.id = id
        msg = message()
        prev_id = self.execute_query_select(adm.get_query_id_show_message())
        all_delay_messages = self.execute_query_select(msg.get_query_all_delay_messages())
        if len(all_delay_messages) == 0:
            return []
        if prev_id[0][0] == 0: #первое
            return all_delay_messages[0]
        for i in range(len(all_delay_messages)):
            if all_delay_messages[i][0] == prev_id[0][0]:
                if i+1 < len(all_delay_messages):
                    return all_delay_messages[i+1]
                else:
                    return []
        
    def get_prev_delay_message(self, id):
        adm = admin()
        adm.id = id
        msg = message()
        prev_id = self.execute_query_select(adm.get_query_id_show_message())
        all_delay_messages = self.execute_query_select(msg.get_query_all_delay_messages())
        if prev_id[0][0] == -1: #последнее
            return all_delay_messages[len(all_delay_messages)-1]
        for i in range(len(all_delay_messages)):
            if all_delay_messages[i][0] == prev_id[0][0]:
                if i-1 >= 0:
                    return all_delay_messages[i-1]
                else:
                    return []

    def update_id_show_delay_message(self, id, id_delay_message):
        adm = admin()
        adm.id = id
        adm.id_show_delay_message = id_delay_message
        self.execute_query(adm.get_query_update_show_message())

    def get_id_show_delay_message(self, id):
        adm = admin()
        adm.id = id
        return self.execute_query_select(adm.get_query_id_show_message())

    def update_audio_message(self, id, id_voise_message):
        msg = message()
        msg.id_admin = id
        msg.id = self.execute_query_select(msg.get_query_last_message())[0][0]
        msg.id_audio_message_str = id_voise_message
        self.execute_query(msg.get_query_update_id_voise_message())

    def get_id_forward_message(self, id):
        msg = message()
        msg.id_admin = id
        return self.execute_query_select(msg.get_query_last_message())[0][3]

    def delete_show_delay_message(self, id):
        id_msg = self.get_id_show_delay_message(id)[0][0]
        self.delete_message_for_it_id(id_msg)

if __name__ == "__main__":
    db = DBWorker()