from datetime import datetime
from random import choice

from peewee import *


db = SqliteDatabase("database/dict_bot.db")


#в закладках есть страница про тирпизацию в которой есть мой вопрос по table_name
class Word(Model):
	word = CharField()
	translate = CharField()
	date = IntegerField()

	class Meta:
		database = db
		table_name = "word"
		# table_name = "dictionary"


class Session(Model):
	# a = "bool"
	main_table_id = IntegerField()
	word = CharField()
	translate = CharField()
	code_number = IntegerField()
	number_of_mistakes = IntegerField()

	class Meta:
		database = db
		# table_name = f"session{a}"
		table_name = "session"

class SessionStat(Model):
	amount_of_rounds = IntegerField()
	amount_of_right_answers = IntegerField()

	class Meta:
		database = db
		table_name = "session_stat"

class AddingTable(Model):
	word = CharField()
	translate = CharField()

	class Meta:
		database = db
		table_name = "adding"


class DelTable(Model):
	del_id = IntegerField()

	class Meta:
		database = db
		table_name = "deleting"

#поиграть с наследованием
def db_content_shower(command: str) -> str:
	main_table_query = Word.select()
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


# ch1_adding
class Adding:
	def __init__(self, *, data=None):
		self.data = data
		try:
			adding_dict = {}
			adding_dict["word"] = self.data[0].strip().capitalize()
			adding_dict["translate"] = ""
			for item in self.data[1:]:
				adding_dict["translate"] += item.strip()
			adding_dict["translate"] = adding_dict["translate"].capitalize()
			self.adding_data = adding_dict
		except AttributeError:
			return None

	def creating_adding_table(self) -> None:
		db.drop_tables([AddingTable])
		db.create_tables([AddingTable])
		with db.atomic():
			AddingTable.create(**self.adding_data)
		return True


	def checking_uniqueness_of_new_word():
		adding_collecter = Adding.collect_addition()
		main_table_query = Word.select()
		looks_alike = []
		for row in main_table_query:
			main_query_answer = [row.id, row.word, row.translate]
			if main_query_answer[1] == adding_collecter["word"] or main_query_answer[2] == adding_collecter["translate"]:
				looks_alike.append(main_query_answer)
		return looks_alike


	def collect_addition():
		adding_table_query = AddingTable.select()
		for row in adding_table_query:
			query_answer = {
				"word": row.word,
				"translate":row.translate,
				"date": datetime.now().strftime("%Y%m%d%H%M")
				}
		return query_answer


	def main_table_converter() -> None:
		db.create_tables([Word])
		with db.atomic():
			Word.create(**Adding.collect_addition())
		db.drop_tables([AddingTable])


# ch2_practicing
class Practice:
	def __init__(self, answer_to_check=None, answer_to_change=None, element=None, options=None):
		self.answer_to_check = answer_to_check
		self.answer_to_change = answer_to_change
		self.element = element
		self.options = options


	def checking_availability():
		try:
			main_table_query = Word.select()
			return len(main_table_query)
		except OperationalError:
			return "No data"


	def creating_practice_table() -> list:
		db.drop_tables([Session])
		db.drop_tables([SessionStat])
		db.create_tables([Session])
		db.create_tables([SessionStat])
		main_table_query = Word.select().order_by(Word.date).limit(7)

		for row in main_table_query:
			session_row = {
				"main_table_id": row.id,
				"word": row.word,
				"translate": row.translate,
				"code_number": 1,
				"number_of_mistakes": 0}

			with db.atomic():
				Session.create(**session_row)

		data = {
			"amount_of_rounds": 0,
			"amount_of_right_answers": 0
		}
		with db.atomic():
			SessionStat.create(**data)

	def process():
		return NotImplementedError


	def checking_for_correctness(self):
		return NotImplementedError

		
	def choicer(self):
		return NotImplementedError


	def process_round_updater(self):
		return NotImplementedError

	def process_stat(self):
		return NotImplementedError


	def session_table_deletion():
		session_query = Session.select()
		for row in session_query:
			Word.update(date=datetime.now().strftime("%Y%m%d%H%M%S")).where(Word.id==row.main_table_id).execute()
		db.drop_tables([Session])
		db.drop_tables([SessionStat])


class PracticeOneToFour(Practice):
	def __init__(self, *, answer_to_check=None, answer_to_change=None, element=None, options=None):
		super().__init__(answer_to_check, answer_to_change, element, options)


	def process():
		for round_number in range(1, 3):
			session_query = Session.select().where(Session.code_number==round_number).order_by(Session.number_of_mistakes, Session.main_table_id.desc())
			main_table_options_query = Word.select()
			options = [option.translate for option in main_table_options_query] if round_number==1 else [option.word for option in main_table_options_query]
			for row in session_query:
				session_row = [[row.id, row.main_table_id, row.word, row.translate, row.code_number, row.number_of_mistakes],
					PracticeOneToFour(options=options, element=row.translate if round_number==1 else row.word).choicer(), round_number]
				return session_row


	def checking_for_correctness(self):
		row_to_check = PracticeOneToFour.process()
		if (row_to_check[2] == 1 and self.answer_to_check == row_to_check[0][3]) or (row_to_check[2] == 2 and self.answer_to_check == row_to_check[0][2]):
			evaluation = "right"
		else:
			evaluation = "wrong"
		PracticeOneToFour(answer_to_change=evaluation).process_round_updater()
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
		row_to_change = PracticeOneToFour.process()
		right_code_number = row_to_change[0][4] + 1
		right_number_of_mistakes = row_to_change[0][5] + 1

		session_stat = PracticeOneToFour.process_stat()
		# session_round_counter = session_stat[0] + 1
		# session_right_answers_counter = session_stat[1] + 1
		SessionStat.update(amount_of_rounds=session_stat[0] + 1).where(SessionStat.id==1).execute()

		if self.answer_to_change == "right":
			Session.update(code_number=right_code_number).where(Session.id==row_to_change[0][0]).execute()
			SessionStat.update(amount_of_right_answers=session_stat[1] + 1).where(SessionStat.id==1).execute()

		else:
			Session.update(number_of_mistakes=right_number_of_mistakes).where(Session.id==row_to_change[0][0]).execute()


	def process_stat():
		session_stat_table_query = SessionStat.select()
		for row in session_stat_table_query:
			stat = [row.amount_of_rounds, row.amount_of_right_answers]
			return stat

			
# ch3_deleting
class Deletion:
	def __init__(self, *, ids_to_delete=None):
		self.ids_to_delete = ids_to_delete


	def obtainig_for_deletion(self):
		db.drop_tables([DelTable])
		confirmation_string = ""
		
		for id_to_delete in self.ids_to_delete:
			data = {"del_id": id_to_delete}

			db.create_tables([DelTable])
			with db.atomic():
				DelTable.create(**data)

			main_table_query = Word.select().where(Word.id==id_to_delete)
			for row in main_table_query:
				list_for_deletion = f"\n{row.id}. {row.word} - {row.translate}"
				confirmation_string += list_for_deletion
		
		return confirmation_string


	def completing_deletion():
		del_table_query = DelTable.select()
		for row in del_table_query:
			Word.delete().where(Word.id==row.del_id).execute()
		db.drop_tables([DelTable])
		Deletion.organize_ids()


	def organize_ids():
		main_table_query = Word.select()
		main_table_list = [row.id for row in main_table_query]
		for item in main_table_list:
			right_id = main_table_list.index(item) + 1
			if item != right_id:
				Word.update(id=right_id).where(Word.id==item).execute()










