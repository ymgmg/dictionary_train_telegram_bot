from peewee import *

from config import DATABASE


class AddingTable(Model):
    chat_id = IntegerField()
    word = CharField()
    translate = CharField()

    class Meta:
        database = DATABASE
        table_name = "Addition"
