from peewee import *
from config import DATABASE

from general.tables import MainTable


class SessionTable(Model):
    chat_id = IntegerField()
    main_table_id = IntegerField()
    word = CharField()
    translate = CharField()
    round_number = IntegerField()
    number_of_mistakes = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "SessionTable"



class CyclePoint(Model):
    chat_id = IntegerField()
    start = IntegerField()
    finish = IntegerField()
    step = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "CyclePoint"

