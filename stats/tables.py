from peewee import *

from config import DATABASE


class StatModel(Model):
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "_stat_table"


class StatTable:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def interaction(self):
        new_table = StatModel
        new_table._meta.table_name = f"{self.chat_id}_stat_table"
        return new_table


class SessionStatModel(Model):
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "_session_stat_table"


class SessionStatTable:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def interaction(self):
        new_table = SessionStatModel
        new_table._meta.table_name = f"{self.chat_id}_session_stat_table"
        return new_table




