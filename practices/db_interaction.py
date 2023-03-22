from datetime import datetime
from random import choice

from peewee import *

from config import DATABASE
from general.tables import MainTable
from practices.tables import SessionTable
from stats.tables import SessionStatTable, StatTable


class Practice:
    def __init__(
        self, answer_to_check=None, answer_to_change=None, chat_id=None,
        element=None, options=None, session_amount=None
    ):
        self.answer_to_check = answer_to_check
        self.answer_to_change = answer_to_change
        self.chat_id = chat_id
        self.element = element
        self.options = options
        self.session_amount = session_amount

    def checking_availability(self):
        try:
            main_table_query = MainTable(self.chat_id).db().select()
            return len(main_table_query)
        except OperationalError:
            return "No data"

    def creating_practice_table(self) -> list:
        DATABASE.drop_tables([SessionTable(chat_id=self.chat_id).db()])
        DATABASE.drop_tables([SessionStatTable(chat_id=self.chat_id).db()])
        DATABASE.create_tables([SessionTable(chat_id=self.chat_id).db()])
        DATABASE.create_tables([StatTable(chat_id=self.chat_id).db()])
        DATABASE.create_tables([SessionStatTable(chat_id=self.chat_id).db()])

        main_table_query = MainTable(self.chat_id).db().select().order_by(
            MainTable(self.chat_id).db().date).limit(self.session_amount)

        for row in main_table_query:
            session_row = {
                "main_table_id": row.id,
                "word": row.word,
                "translate": row.translate,
                "round_number": 1,
                "number_of_mistakes": 0}

            with DATABASE.atomic():
                SessionTable(chat_id=self.chat_id).db().create(**session_row)
        default_stat = {
            "all_answers": 0,
            "right_answers": 0,
        }
        with DATABASE.atomic():
            SessionStatTable(chat_id=self.chat_id).db().create(**default_stat)

    def session_table_deletion(self):
        session_query = SessionTable(chat_id=self.chat_id).db().select()
        for row in session_query:
            MainTable(self.chat_id).db().update(
                date=int(datetime.now().timestamp())).where(
                MainTable(self.chat_id).db().id == row.main_table_id
                ).execute()
        DATABASE.drop_tables([SessionTable(chat_id=self.chat_id).db()])

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
    def __init__(
        self, *, answer_to_check=None, answer_to_change=None, chat_id=None,
        element=None, options=None, session_amount=None
    ):
        super().__init__(
            answer_to_check, answer_to_change, chat_id, element,
            options, session_amount)

    def process(self):
        for round_number in range(1, 3):
            session_filter = SessionTable(
                chat_id=self.chat_id).db().round_number == round_number
            session_query = SessionTable(chat_id=self.chat_id).db().select(
                ).where(session_filter).order_by(
                SessionTable(chat_id=self.chat_id).db().number_of_mistakes,
                SessionTable(chat_id=self.chat_id).db().main_table_id.desc())
            options_query = MainTable(self.chat_id).db().select()

            for row in session_query:
                if round_number == 1:
                    options = [option.translate for option in options_query]
                    element = row.translate
                else:
                    options = [option.word for option in options_query]
                    element = row.word

                session_row = {
                    "id": row.id,
                    "main_table_id": row.main_table_id,
                    "word": row.word,
                    "translate": row.translate,
                    "table_round_number": row.round_number,
                    "mistakes_number": row.number_of_mistakes,
                    "choosed_options": PracticeOneToFour(
                        options=options, element=element).choicer(),
                    "round_number": round_number,
                }
                return session_row

    def checking_for_correctness(self):
        row_to_check = PracticeOneToFour(chat_id=self.chat_id).process()
        round1_condition1 = row_to_check["round_number"] == 1
        round1_condition2 = self.answer_to_check == row_to_check["translate"]
        first_round = round1_condition1 and round1_condition2

        round2_condition1 = row_to_check["round_number"] == 2
        round2_condition2 = self.answer_to_check == row_to_check["word"]
        second_round = round2_condition1 and round2_condition2

        if first_round or second_round:
            evaluation = "right"
        else:
            evaluation = "wrong"
        PracticeOneToFour(
            chat_id=self.chat_id, answer_to_change=evaluation
            ).process_round_updater()
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
        data_row = PracticeOneToFour(chat_id=self.chat_id).process()
        print(data_row)
        right_code_number = data_row["table_round_number"] + 1
        right_number_of_mistakes = data_row["mistakes_number"] + 1

        stat_answers_counter = PracticeOneToFour(
            chat_id=self.chat_id).process_stat()
        SessionStatTable(chat_id=self.chat_id).db().update(
            all_answers=stat_answers_counter["all_answers"] + 1
            ).execute()
        if self.answer_to_change == "right":
            SessionTable(chat_id=self.chat_id).db().update(
                round_number=right_code_number).where(SessionTable(
                    chat_id=self.chat_id).db().id == data_row["id"]).execute()
            SessionStatTable(chat_id=self.chat_id).db().update(
                right_answers=stat_answers_counter["right_answers"] + 1
                ).execute()
        else:
            SessionTable(self.chat_id).db().update(
                number_of_mistakes=right_number_of_mistakes).where(
                SessionTable(chat_id=self.chat_id).db().id == data_row["id"]
                ).execute()

    def process_stat(self):
        session_stat_table_query = SessionStatTable(self.chat_id).db().select()
        for row in session_stat_table_query:
            stat = {
                "all_answers": row.all_answers,
                "right_answers": row.right_answers
                }
        return stat
