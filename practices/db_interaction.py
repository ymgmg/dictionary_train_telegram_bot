from datetime import datetime
from random import choice

from peewee import *

from config import DATABASE
from general.tables import MainTable
from practices.tables import CyclePoint, SessionTable
from stats.tables import SessionStat, Stat


class Practice:
    def __init__(
        self, answer_to_check=None, chat_id=None, element=None,
        is_correct=None, options=None, session_amount=None
    ):
        self.answer_to_check = answer_to_check
        self.is_correct = is_correct
        self.chat_id = chat_id
        self.element = element
        self.options = options
        self.session_amount = session_amount

    def dictionary_checking(self):
        try:
            main_table_query = MainTable(self.chat_id).db().select()
            return len(main_table_query)
        except OperationalError:
            return "No data"

    def creating_practice_table(self) -> list:
        Practice(chat_id=self.chat_id).what_starts_first()

        DATABASE.drop_tables([SessionTable(self.chat_id).db()])
        DATABASE.drop_tables([SessionStat(self.chat_id).db()])

        DATABASE.create_tables([SessionTable(self.chat_id).db()])
        DATABASE.create_tables([SessionStat(self.chat_id).db()])
        DATABASE.create_tables([Stat])

        start_point = CyclePoint(self.chat_id).db().get(
            CyclePoint(self.chat_id).db().id == 1).start
        main_table_query = MainTable(self.chat_id).db().select().order_by(
            MainTable(self.chat_id).db().date).limit(self.session_amount)

        for row in main_table_query:
            session_row = {
                "main_table_id": row.id,
                "word": row.word,
                "translate": row.translate,
                "round_number": start_point,
                "number_of_mistakes": 0}

            with DATABASE.atomic():
                SessionTable(self.chat_id).db().create(**session_row)
        with DATABASE.atomic():
            SessionStat(self.chat_id).db().create(
               all_answers=0, right_answers=0)

    def what_starts_first(self):
        DATABASE.drop_tables([CyclePoint(self.chat_id).db()])

        decision = choice(["word", "translate"])
        if decision == "word":
            path_data = {"start": 1, "finish": 3, "step": 1}
        else:
            path_data = {"start": 2, "finish": 0, "step": -1}
        DATABASE.create_tables([CyclePoint(self.chat_id).db()])
        with DATABASE.atomic():
            CyclePoint(self.chat_id).db().create(**path_data)

    def get_session_data(self):
        point = CyclePoint(self.chat_id).db().get(
            CyclePoint(self.chat_id).db().id == 1)
        for round_num in range(point.start, point.finish, point.step):
            session_filter = SessionTable(
                self.chat_id).db().round_number == round_num
            session_query = SessionTable(self.chat_id).db().select(
                ).where(session_filter).order_by(
                SessionTable(self.chat_id).db().number_of_mistakes,
                SessionTable(self.chat_id).db().main_table_id.desc())

            for row in session_query:
                session_row = {
                    "id": row.id,
                    "main_table_id": row.main_table_id,
                    "word": row.word,
                    "translate": row.translate,
                    "table_round_number": row.round_number,
                    "mistakes_number": row.number_of_mistakes,
                    "round_number": round_num,
                }
                return session_row

    def session_data_updater(self):
        data_row = Practice(chat_id=self.chat_id).get_session_data()
        path_query = CyclePoint(
            self.chat_id).db().get(CyclePoint(self.chat_id).db().id == 1)

        right_code_number = data_row["table_round_number"] + path_query.step
        right_mistakes_number = data_row["mistakes_number"] + 1

        stat_answers_counter = Practice(
            chat_id=self.chat_id).process_stat()
        SessionStat(self.chat_id).db().update(
            all_answers=stat_answers_counter["all_answers"] + 1
            ).execute()
        if self.is_correct is True:
            SessionTable(self.chat_id).db().update(
                round_number=right_code_number).where(
                SessionTable(self.chat_id).db().id == data_row["id"]
                ).execute()

            SessionStat(self.chat_id).db().update(
                right_answers=stat_answers_counter["right_answers"] + 1
                ).execute()
        else:
            SessionTable(self.chat_id).db().update(
                number_of_mistakes=right_mistakes_number).where(
                SessionTable(self.chat_id).db().id == data_row["id"]
                ).execute()

    def process_stat(self):
        session_stat_table_query = SessionStat(self.chat_id).db().select()
        for row in session_stat_table_query:
            session_stat = {
                "all_answers": row.all_answers,
                "right_answers": row.right_answers
                }
            return session_stat

    def final_stat(self):
        session_stat = PracticeOneToFour(chat_id=self.chat_id).process_stat()

        session_result = round(
            session_stat["right_answers"]
            / session_stat["all_answers"] * 100, 2)

        overall_result = Practice(
            chat_id=self.chat_id).all_time_stat(session_stat)

        if overall_result is None:
            session_stat["chat_id"] = self.chat_id
            with DATABASE.atomic():
                Stat.create(**session_stat,)
            stats_to_user = {
                "session_stat": session_result,
                "overall_stat": session_result,
            }
            return stats_to_user
        else:
            stats_to_user = {
                "session_stat": session_result,
                "overall_stat": overall_result,
            }
            return stats_to_user

    def all_time_stat(self, session_stat):
        query = Stat.select().where(Stat.chat_id == self.chat_id)
        if len(query) == 0:
            return None
        else:
            for row in query:
                all_answers = row.all_answers + session_stat["all_answers"]
                right_answers = (
                    row.right_answers + session_stat["right_answers"])
            Stat.update(
                all_answers=all_answers, right_answers=right_answers
                ).where(Stat.chat_id == self.chat_id).execute()
            return round(right_answers / all_answers * 100, 2)

    def session_table_deletion(self):
        session_query = SessionTable(self.chat_id).db().select()
        for row in session_query:
            MainTable(self.chat_id).db().update(
                date=int(datetime.now().timestamp())).where(
                MainTable(self.chat_id).db().id == row.main_table_id
                ).execute()
        DATABASE.drop_tables([SessionTable(self.chat_id).db()])
        DATABASE.drop_tables([SessionStat(self.chat_id).db()])
        DATABASE.drop_tables([CyclePoint(self.chat_id).db()])

    def process(self):
        return NotImplementedError

    def correctness_checking(self):
        return NotImplementedError

    def choicer(self):
        return NotImplementedError


class PracticeOneToFour(Practice):
    def __init__(
        self, *, answer_to_check=None, chat_id=None, element=None,
        is_correct=None, options=None, session_amount=None
    ):
        super().__init__(
            answer_to_check, chat_id, element,
            is_correct, options, session_amount)

    def process(self):
        session_data = PracticeOneToFour(
            chat_id=self.chat_id).get_session_data()
        if session_data is not None:
            options_query = MainTable(self.chat_id).db().select(
                MainTable(self.chat_id).db().word,
                MainTable(self.chat_id).db().translate)

            if session_data["round_number"] == 1:
                options = [option.translate for option in options_query]
                element = session_data["translate"]
            else:
                options = [option.word for option in options_query]
                element = session_data["word"]

            session_data["choosed_options"] = PracticeOneToFour(
                            options=options, element=element).choicer()
            return session_data
        else:
            return None

    def correctness_checking(self):
        row_to_check = PracticeOneToFour(
            chat_id=self.chat_id).get_session_data()
        round1_condition1 = row_to_check["round_number"] == 1
        round1_condition2 = self.answer_to_check == row_to_check["translate"]
        first_round = round1_condition1 and round1_condition2

        round2_condition1 = row_to_check["round_number"] == 2
        round2_condition2 = self.answer_to_check == row_to_check["word"]
        second_round = round2_condition1 and round2_condition2

        if first_round or second_round:
            evaluation = True
        else:
            evaluation = False
        PracticeOneToFour(
            chat_id=self.chat_id, is_correct=evaluation
            ).session_data_updater()
        return evaluation

    def choicer(self):
        final_options = [self.element]
        while len(final_options) < 4:
            option = choice(self.options)
            if option not in final_options:
                final_options.append(option)
        final_options.sort()
        return final_options


class PracticeYesNo(Practice):
    def __init__(
        self, *, answer_to_check=None, chat_id=None, element=None,
        is_correct=None, options=None, session_amount=None
    ):
        super().__init__(
            answer_to_check, chat_id, element,
            is_correct, options, session_amount)

    def process(self):
        session_data = PracticeYesNo(
            chat_id=self.chat_id).get_session_data()
        if session_data is not None:
            options_query = MainTable(self.chat_id).db().select(
                MainTable(self.chat_id).db().word,
                MainTable(self.chat_id).db().translate)

            if session_data["round_number"] == 1:
                options = [option.translate for option in options_query]
                element = session_data["translate"]
            else:
                options = [option.word for option in options_query]
                element = session_data["word"]

            session_data["choosed_options"] = PracticeYesNo(
                            options=options, element=element).choicer()
            return session_data
        else:
            return None

    def correctness_checking(self):
        row_to_check = PracticeOneToFour(
            chat_id=self.chat_id).get_session_data()
        round1_condition1 = row_to_check["round_number"] == 1
        round2_condition1 = row_to_check["round_number"] == 2

        round1_condition2 = self.answer_to_check == row_to_check["translate"]
        round2_condition2 = self.answer_to_check == row_to_check["word"]

        try:
            round1_condition3 = (
                self.answer_to_check.split(" ", 1)[1] !=
                row_to_check["translate"])
            round2_condition3 = (
                self.answer_to_check.split(" ", 1)[1] != row_to_check["word"])
        except IndexError:
            round2_condition3 = False
            round1_condition3 = False

        first_round = round1_condition1 and \
            (round1_condition2 or round1_condition3)
        second_round = round2_condition1 and \
            (round2_condition2 or round2_condition3)

        if first_round or second_round:
            evaluation = True
        else:
            evaluation = False
        PracticeYesNo(
            chat_id=self.chat_id, is_correct=evaluation
            ).session_data_updater()
        return evaluation

    def choicer(self):
        yn = choice([True, False])
        if yn is True:
            return self.element
        else:
            status = False
            for attempt in self.options:
                option = choice(self.options)
                if option != self.element:
                    return option
