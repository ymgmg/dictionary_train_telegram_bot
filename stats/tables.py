from peewee import *

from config import DATABASE


class Stat(Model):
    chat_id = IntegerField()
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE


class SessionStatModel(Model):
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "_stat_table"


class SessionStat:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def db(self):
        new_table = SessionStatModel
        new_table._meta.table_name = f"{self.chat_id}_session_stat_table"
        return new_table
