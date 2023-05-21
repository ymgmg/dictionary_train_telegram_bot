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
        AddingTable.delete().where(AddingTable.chat_id == self.chat_id).execute()
        adding_data = self.adding_data
        adding_data["chat_id"] = self.chat_id
        with DATABASE.atomic():
            AddingTable.create(**self.adding_data)
        return True

    def checking_uniqueness_of_new_word(self):
        collecter = AddingDB(chat_id=self.chat_id).collect_addition()
        looks_alike = []
        try:
            quey = MainTable.select().where(MainTable.chat_id == self.chat_id)
            for row in quey:
                answer = [row.id, row.word, row.translate]

                word_condition = answer[1] == collecter["word"]
                translate_condition = answer[2] == collecter["translate"]

                if word_condition or translate_condition:
                    looks_alike.append(answer)
            return looks_alike
        except OperationalError:
            return looks_alike

    def collect_addition(self):
        adding_stuff = AddingTable.get(AddingTable.chat_id == self.chat_id)
        # for row in adding_table_query:
        query_answer = {
            "chat_id" : self.chat_id,
            "word": adding_stuff.word,
            "translate": adding_stuff.translate,
            "date": int(datetime.now().timestamp())
        }
        return query_answer

    def main_table_converter(self) -> None:
        if self.command == "yes":
            with DATABASE.atomic():
                MainTable.create(
                    **AddingDB(chat_id=self.chat_id).collect_addition())
        AddingTable.delete().where(AddingTable.chat_id == self.chat_id).execute()
        AddingDB(chat_id=self.chat_id).organize_ids()

    def organize_ids(self):
        main_table_query = MainTable.select().where(MainTable.chat_id == self.chat_id)
        user_words_list = [row.id for row in main_table_query]

        for row in user_words_list:
            right_id = user_words_list.index(row) + 1
            actual_word_id = MainTable.get(MainTable.id == row).word_id
            if actual_word_id != right_id:
                MainTable.update(word_id=right_id).where(
                    MainTable.id == row).execute()
