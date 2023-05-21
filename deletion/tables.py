from peewee import *

from config import DATABASE


class DeletionTable(Model):
    chat_id = IntegerField()
    del_id = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "Deletion"
