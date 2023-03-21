from peewee import *

from config import DATABASE
from deletion.tables import DeletionTable
from general.tables import MainTable


class DeletionDB:
    def __init__(self, *, chat_id=None, ids_to_delete=None):
        self.ids_to_delete = ids_to_delete
        self.chat_id = chat_id

    def obtainig_for_deletion(self):
        DATABASE.drop_tables([DeletionTable(self.chat_id).interaction()])
        confirmation_string = ""

        for id_to_delete in self.ids_to_delete:
            data = {"del_id": id_to_delete}

            DATABASE.create_tables([DeletionTable(self.chat_id).interaction()])
            with DATABASE.atomic():
                DeletionTable(self.chat_id).interaction().create(**data)

            main_table_query = MainTable(self.chat_id).interaction().select().where(MainTable(self.chat_id).interaction().id == id_to_delete)

            for row in main_table_query:
                list_for_deletion = f"\n{row.id}. {row.word} - {row.translate}"
                confirmation_string += list_for_deletion

        return confirmation_string

    def completing_deletion(self):
        del_table_query = DeletionTable(self.chat_id).interaction().select()

        for row in del_table_query:
            MainTable(self.chat_id).interaction().delete().where(MainTable(self.chat_id).interaction().id == row.del_id).execute()
        DATABASE.drop_tables([DeletionTable(self.chat_id).interaction()])
        DeletionDB(chat_id=self.chat_id).organize_ids()

    def organize_ids(self):
        main_table_query = MainTable(self.chat_id).interaction().select()
        main_table_list = [row.id for row in main_table_query]

        for item in main_table_list:
            right_id = main_table_list.index(item) + 1
            if item != right_id:
                MainTable(self.chat_id).interaction().update(id=right_id).where(MainTable(self.chat_id).interaction().id == item).execute()
