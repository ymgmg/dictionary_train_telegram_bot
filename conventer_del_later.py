# // 5443405146
from datetime import datetime
from peewee import *

from config import DATABASE


class MainModel(Model):
    word = CharField()
    translate = CharField()
    date = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "MainDict"


class SecondModel(Model):
    word = CharField()
    translate = CharField()
    date = IntegerField()

    class Meta:
        database = DATABASE
        table_name = "5443405146_main_table"


# def run_mf():
#     main_query = MainModel.select()
#     for row in main_query:
#         data = {
#             "word": row.word,
#             "translate": row.translate,
#             "date": row.date}
#         conventer(data)

# def conventer(data):
#     with DATABASE.atomic():
#         SecondModel.create(**data)

# run_mf()

def date_changer():
    main_query = SecondModel.select()
    for row in main_query:
        a = datetime.strptime(str(row.date), "%Y%m%d%H%M%S").timestamp()
        SecondModel.update(date=int(a)).where(SecondModel.id == row.id).execute()
        print(int(a))
print("now", datetime.now().timestamp())
date_changer()
# 

