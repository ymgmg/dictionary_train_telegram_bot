from peewee import *

from config import DATABASE


class MainModel(Model):
    word = CharField()
    translate = CharField()
    date = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "MainDict"


class MainTable:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def db(self):
        new_table = MainModel
        new_table._meta.table_name = f"{self.chat_id}_main_table"
        return new_table


class UserTable(Model):
    chat_id = IntegerField()
    premium_status = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "User"
