from peewee import *

from config import DATABASE


class DeletionTableModel(Model):
    del_id = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "_deletion_table"


class DeletionTable:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def db(self):
        new_table = DeletionTableModel
        new_table._meta.table_name = f"{self.chat_id}_deletion_table"
        return new_table
