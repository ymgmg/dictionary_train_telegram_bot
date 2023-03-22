from peewee import *

from config import DATABASE


class AddingTableModel(Model):
    word = CharField()
    translate = CharField()

    class Meta:
        database = DATABASE
        table_name = "_adding_table"


class AddingTable:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def db(self):
        new_table = AddingTableModel
        new_table._meta.table_name = f"{self.chat_id}_adding_table"
        return new_table
