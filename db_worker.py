import sqlite3

class admin:
    id: int
    state: int
    table_name = 'admin'

    def get_query_create_table(self) -> str:
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY NOT NULL, state INTEGER);"

    def get_query_drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.table_name}"

    def get_query_insert_into_table(self) -> str:
        return f"""INSERT INTO {self.table_name} VALUES ({self.id}, {self.state})"""

    def get_query_delete_all(self) -> str:
        return f"DELETE FROM {self.table_name}"

    def get_query_is_admin(self) -> str:
        return f"SELECT COUNT() FROM {self.table_name} WHERE id = {self.id}"

    def get_query_state(self):
        return f"SELECT state FROM {self.table_name} WHERE id = {self.id}"

    def get_query_update_state(self):
        return f"UPDATE {self.table_name} SET state = {self.state} WHERE id = {self.id}"

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

class message:
    # id: int
    text: str
    media_attachments: str
    audio_path: str
    id_admin: int
    table_name = 'message'

    def __init__(self) -> None:
        self.text = "''"
        self.media_attachments = "''" 
        self.audio_path = "''"

    def get_query_create_table(self) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,text VARCHAR (2000),media_attachments VARCHAR (255), audio_path VARCHAR (255), id_admin INTEGER REFERENCES admin (id));"""

    def get_query_drop_table(self) -> str:
        return f"DROP TABLE IF EXISTS {self.table_name}"

    def get_query_insert_into_table(self) -> str:
        return f"""INSERT INTO {self.table_name} (text, media_attachments, audio_path, id_admin) VALUES ({self.text}, {self.media_attachments}, {self.audio_path}, {self.id_admin})"""

    def get_query_delete_all(self) -> str:
        return f"DELETE FROM {self.table_name}"

    def get_query_last_text(self) -> str:
        return f"select text from {self.table_name} where id_admin = {self.id_admin} and id <= (select seq from sqlite_sequence where name = '{self.table_name}') order by id DESC LIMIT 1"



class DBWorker:

    def update_state(self, id_admin, state):
        adm = admin()
        adm.id = id_admin
        adm.state = state
        self.execute_query(adm.get_query_update_state())

    def is_admin(self, adm: admin) -> bool:
        res = self.execute_query_select(adm.get_query_is_admin())
        return res[0][0] != 0

    def get_admin_state(self, id_admin) -> int:
        adm = admin()
        adm.id = id_admin
        if self.is_admin(adm):
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
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_query(self, query: str):
        self.cursor.execute(query)
        self.connection.commit()

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

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('vk_bot.db')
            self.cursor = self.connection.cursor()
            self.drop_tables() #TODO DELETE THIS
            res = self.execute_query_select("SELECT COUNT() FROM sqlite_master WHERE type='table';")
            if res[0][0] <= 1:
                self.create_tables()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def __del__(self):
        if(self.connection):
            self.connection.close()
            print("Connection closed")

    def save_text_message(self, text, id_admin):
        adm = admin()
        adm.id = id_admin
        msg = message()
        msg.id_admin = id_admin
        msg.text = "'"+text+"'"

        if self.is_admin(adm):
            print(msg.get_query_insert_into_table())
            self.execute_query(msg.get_query_insert_into_table())

    def get_message(self, id) -> str:
        msg = message()
        msg.id_admin = id
        text = self.execute_query_select(msg.get_query_last_text())
        return text[0][0]
if __name__ == "__main__":
    db = DBWorker()