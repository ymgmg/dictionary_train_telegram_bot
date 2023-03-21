from datetime import datetime
from random import choice

from peewee import *

from config import DATABASE
from general.tables import MainTable
from practices.tables import SessionTable
from stats.tables import SessionStatTable, StatTable


class Practice:
    def __init__(self, answer_to_check=None, answer_to_change=None,
                chat_id=None, element=None, options=None, session_amount=None):
        self.answer_to_check = answer_to_check
        self.answer_to_change = answer_to_change
        self.chat_id = chat_id
        self.element = element
        self.options = options
        self.session_amount = session_amount


    def checking_availability(self):
        try:
            main_table_query = MainTable(self.chat_id).interaction().select()
            return len(main_table_query)
        except OperationalError:
            return "No data"

    def creating_practice_table(self) -> list:
        DATABASE.drop_tables([SessionTable(chat_id=self.chat_id).interaction()])
        DATABASE.drop_tables([SessionStatTable(chat_id=self.chat_id).interaction()])
        DATABASE.create_tables([SessionTable(chat_id=self.chat_id).interaction()])
        DATABASE.create_tables([StatTable(chat_id=self.chat_id).interaction()])
        DATABASE.create_tables([SessionStatTable(chat_id=self.chat_id).interaction()])

        main_table_query = MainTable(self.chat_id).interaction().select().order_by(MainTable(self.chat_id).interaction().date).limit(self.session_amount)

        for row in main_table_query:
            session_row = {
                "main_table_id": row.id,
                "word": row.word,
                "translate": row.translate,
                "round_number": 1,
                "number_of_mistakes": 0}

            with DATABASE.atomic():
                SessionTable(chat_id=self.chat_id).interaction().create(**session_row)
        default_stat = {
            "all_answers": 0,
            "right_answers": 0,
        }
        with DATABASE.atomic():
            SessionStatTable(chat_id=self.chat_id).interaction().create(**default_stat)

    def session_table_deletion(self):
        session_query = SessionTable(chat_id=self.chat_id).interaction().select()
        for row in session_query:
            MainTable(self.chat_id).interaction().update(date=int(datetime.now().timestamp())).where(MainTable(self.chat_id).interaction().id == row.main_table_id).execute()
        DATABASE.drop_tables([SessionTable(chat_id=self.chat_id).interaction()])

    def process(self):
        return NotImplementedError

    def checking_for_correctness(self):
        return NotImplementedError

    def choicer(self):
        return NotImplementedError

    def process_round_updater(self):
        return NotImplementedError

    def process_stat(self):
        return NotImplementedError


class PracticeOneToFour(Practice):
    def __init__(self, *, answer_to_check=None, answer_to_change=None,
                chat_id=None, element=None, options=None, session_amount=None):
        super().__init__(answer_to_check, answer_to_change, chat_id, element, options, session_amount)

    def process(self):
        for round_number in range(1, 3):
            session_query = SessionTable(chat_id=self.chat_id).interaction().select().where(SessionTable(chat_id=self.chat_id).interaction().round_number == round_number).order_by(SessionTable(chat_id=self.chat_id).interaction().number_of_mistakes, SessionTable(chat_id=self.chat_id).interaction().main_table_id.desc())
            main_table_options_query = MainTable(self.chat_id).interaction().select()
            options = [option.translate for option in main_table_options_query] if round_number == 1 else [option.word for option in main_table_options_query]
            for row in session_query:
                session_row = {
                    "id": row.id,
                    "main_table_id": row.main_table_id,
                    "word": row.word,
                    "translate": row.translate,
                    "table_round_number": row.round_number,
                    "mistakes_number": row.number_of_mistakes,
                    "choosed_options": PracticeOneToFour(options=options, element=row.translate
                        if round_number == 1 else row.word).choicer(),
                    "round_number": round_number,
                }
                return session_row

    def checking_for_correctness(self):
        row_to_check = PracticeOneToFour(chat_id=self.chat_id).process()
        print(row_to_check)
        round1_condition = row_to_check["round_number"] == 1 and self.answer_to_check == row_to_check["translate"]
        round2_condition = row_to_check["round_number"] == 2 and self.answer_to_check == row_to_check["word"]

        if round1_condition or round2_condition:
            evaluation = "right"
        else:
            evaluation = "wrong"
        PracticeOneToFour(chat_id=self.chat_id, answer_to_change=evaluation).process_round_updater()
        return evaluation

    def choicer(self):
        final_options = [self.element]
        while len(final_options) < 4:
            option = choice(self.options)
            if option not in final_options:
                final_options.append(option)
        final_options.sort()
        return final_options

    def process_round_updater(self):
        row_to_change = PracticeOneToFour(chat_id=self.chat_id).process()
        print(row_to_change)
        right_code_number = row_to_change["table_round_number"] + 1
        right_number_of_mistakes = row_to_change["mistakes_number"] + 1

        stat_answers_counter = PracticeOneToFour(chat_id=self.chat_id).process_stat()
        SessionStatTable(chat_id=self.chat_id).interaction().update(all_answers=stat_answers_counter["all_answers"] + 1).execute()
        if self.answer_to_change == "right":
            SessionTable(chat_id=self.chat_id).interaction().update(round_number=right_code_number).where(SessionTable(chat_id=self.chat_id).interaction().id == row_to_change["id"]).execute()
            SessionStatTable(chat_id=self.chat_id).interaction().update(right_answers=stat_answers_counter["right_answers"] + 1).execute()
        else:
            SessionTable(chat_id=self.chat_id).interaction().update(number_of_mistakes=right_number_of_mistakes).where(SessionTable(chat_id=self.chat_id).interaction().id == row_to_change["id"]).execute()

    def process_stat(self):
        session_stat_table_query = SessionStatTable(chat_id=self.chat_id).interaction().select()
        for row in session_stat_table_query:
            stat = {
                "all_answers": row.all_answers,
                "right_answers": row.right_answers
                }

        return stat

