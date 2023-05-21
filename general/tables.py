from peewee import *

from config import DATABASE


class MainTable(Model):
    chat_id = IntegerField()
    word_id = IntegerField(default=1)
    word = CharField()
    translate = CharField()
    date = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "Word"


class UserTable(Model):
    chat_id = IntegerField()
    premium_status = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "User"
