from peewee import *

from config import DATABASE


class Stat(Model):
    chat_id = IntegerField()
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE


class SessionStat(Model):
    right_answers = IntegerField()
    all_answers = IntegerField()

    class Meta:
        database = DATABASE

