from datetime import datetime

from peewee import *

from adding.tables import AddingTable
from general.tables import MainTable
from config import DATABASE



class AddingDB:
    def __init__(self, *, data=None, command=None, chat_id=None):
        self.data = data
        self.chat_id = chat_id
        self.command = command

        try:
            adding_dict = {}
            adding_dict["word"] = self.data[0].strip().capitalize()
            adding_dict["translate"] = ""
            for item in self.data[1:]:
                adding_dict["translate"] += item.strip()
            adding_dict["translate"] = adding_dict["translate"].capitalize()
            self.adding_data = adding_dict
        except (AttributeError, TypeError):
            return None

    def creating_adding_table(self) -> None:
        DATABASE.drop_tables([AddingTable(self.chat_id).interaction()])
        DATABASE.create_tables([AddingTable(self.chat_id).interaction()])
        with DATABASE.atomic():
            AddingTable(self.chat_id).interaction().create(**self.adding_data)
        return True

    def checking_uniqueness_of_new_word(self):
        adding_collecter = AddingDB(chat_id=self.chat_id).collect_addition()
        looks_alike = []
        try:
            main_table_query = MainTable(self.chat_id).interaction().select()
            for row in main_table_query:
                main_query_answer = [row.id, row.word, row.translate]
                if main_query_answer[1] == adding_collecter["word"] or main_query_answer[2] == adding_collecter["translate"]:
                    looks_alike.append(main_query_answer)
            return looks_alike
        except OperationalError:
            return looks_alike

    def collect_addition(self):
        adding_table_query = AddingTable(self.chat_id).interaction().select()
        for row in adding_table_query:
            query_answer = {
                "word": row.word,
                "translate": row.translate,
                "date": int(datetime.now().timestamp())
                }
        return query_answer

    def main_table_converter(self) -> None:
        if self.command == "yes":
            DATABASE.create_tables([MainTable(self.chat_id).interaction()])
            with DATABASE.atomic():
                MainTable(self.chat_id).interaction().create(**AddingDB(chat_id=self.chat_id).collect_addition())
        DATABASE.drop_tables([AddingTable(self.chat_id).interaction()])
