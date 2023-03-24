from datetime import datetime

from peewee import *

from general.tables import MainTable, UserTable
from config import DATABASE


def db_content_shower(chat_id: str, command: str) -> str:
    try:
        main_table_query = MainTable(chat_id).db().select()
        output_str = ""
        if command == "without_translate":
            for row in main_table_query:
                query_answer = f"{row.id}. {row.word}\n"
                output_str += query_answer
        elif command == "with_translate":
            for row in main_table_query:
                query_answer = f"{row.id}. {row.word} - {row.translate}\n"
                output_str += query_answer
        return output_str
    except OperationalError:
        return False


def show_necessary_words(chat_id):
    date_now = datetime.now().timestamp()
    main_table_query = MainTable(chat_id).db().select()

    condition = date_now - MainTable(chat_id).db().date
    words_count = main_table_query.count()
    one_day = main_table_query.where(condition > 86400).count()
    three_days = main_table_query.where(condition > 86400 * 3).count()
    five_days = main_table_query.where(condition > 86400 * 5).count()

    data = [words_count, one_day, three_days, five_days,]
    stat_string = f"You got {data[0]} words in your dictionary."
    for day_num in range(1, 4):
        stat_string += f"\n{data[day_num]} words you haven't practiced for \
        \nmore than {day_num * 2 -1} {'day' if day_num < 2 else 'days'}."
    return stat_string


def create_user_table(chat_id):
    user_query = UserTable.select(UserTable.chat_id).where(
        UserTable.chat_id == chat_id)
    user_ids_list = [user_id.chat_id for user_id in user_query]
    if chat_id not in user_ids_list:
        data = {
            "chat_id": chat_id,
            "premium_status": 0
        }
        with DATABASE.atomic():
            UserTable.create(**data)
