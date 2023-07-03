from peewee import *

from config import DATABASE
from deletion.tables import DeletionTable
from general.tables import MainTable


class DeletionDB:
    def __init__(self, *, chat_id=None, ids_to_delete=None):
        self.ids_to_delete = ids_to_delete
        self.chat_id = chat_id

    def obtainig_for_deletion(self):
        DeletionTable.delete().where(DeletionTable.chat_id == self.chat_id).execute()
        confirmation_string = ""

        for id_to_delete in self.ids_to_delete:
            data = {
                "chat_id": self.chat_id,
                "del_id": id_to_delete
                }

            with DATABASE.atomic():
                DeletionTable.create(**data)

            main_table_query = MainTable.select().where(
                MainTable.chat_id == self.chat_id, MainTable.word_id == id_to_delete)

            for row in main_table_query:
                list_for_deletion = f"\n{row.word_id}. {row.word} - {row.translate}"
                confirmation_string += list_for_deletion

        return confirmation_string

    def completing_deletion(self):
        del_table_query = DeletionTable.select().where(DeletionTable.chat_id == self.chat_id)

        for row in del_table_query:
            MainTable.delete().where(
                MainTable.chat_id == self.chat_id, MainTable.word_id == row.del_id).execute()
        DeletionDB(chat_id=self.chat_id).organize_ids()
        DeletionTable.delete().where(DeletionTable.chat_id == self.chat_id).execute()

    def organize_ids(self):
        main_table_query = MainTable.select().where(MainTable.chat_id == self.chat_id)
        user_words_list = [row.id for row in main_table_query]

        for row in user_words_list:
            right_id = user_words_list.index(row) + 1
            actual_word_id = MainTable.get(MainTable.id == row).word_id
            if actual_word_id != right_id:
                MainTable.update(word_id=right_id).where(
                    MainTable.id == row).execute()
