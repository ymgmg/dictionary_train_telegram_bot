from peewee import *
from config import DATABASE

from general.tables import MainTable


class SessionModel(Model):
    main_table_id = IntegerField()
    word = CharField()
    translate = CharField()
    round_number = IntegerField()
    number_of_mistakes = IntegerField()

    class Meta:
        database = DATABASE

class SessionTable:
    def __init__(self, *, chat_id):
        self.chat_id = chat_id

    def interaction(self):
        new_table = SessionModel
        new_table._meta.table_name = f"{self.chat_id}_session_table"
        return new_table


