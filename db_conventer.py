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


class AddingTable(Model):
	word = CharField()
	translate = CharField()
	date = IntegerField()

	class Meta:
		database = db
		table_name = "adding"


class DelTable(Model):
	del_id = IntegerField()

	class Meta:
		database = db
		table_name = "deleting"


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
	def __init__(self, *, data=None, command=None):
		self.data = data
		self.command = command

	def creating_adding_table(self) -> None:
		db.drop_tables([AddingTable])
		db.create_tables([AddingTable])
		with db.atomic():
			AddingTable.create(**self.data)


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


	def main_table_converter(self) -> None:
		if self.command == "yes":
			db.create_tables([Word])
			with db.atomic():
				Word.create(**Adding.collect_addition())
		db.drop_tables([AddingTable])


# ch2_practicing
class Practice:
	def checking_availability():
		try:
			main_table_query = Word.select()
			return len(main_table_query)
		except OperationalError:
			return "No data"


	def creating_practice_table() -> list:
		db.drop_tables([Session])
		db.create_tables([Session])
		main_table_query = Word.select().order_by(Word.date).limit(3)
		for row in main_table_query:
			session_row = {
				"main_table_id": row.id,
				"word": row.word,
				"translate": row.translate,
				"code_number": 1,
				"number_of_mistakes": 0}
			with db.atomic():
				Session.create(**session_row)


	def first_round():
		for round_number in range(1, 3):
			session_query = Session.select().where(Session.code_number==round_number).order_by(Session.number_of_mistakes, Session.main_table_id.desc())
			main_table_options_query = Word.select()
			options = [option.translate for option in main_table_options_query]
			for row in session_query:
				session_row = [[row.id, row.main_table_id, row.word, row.translate, row.code_number, row.number_of_mistakes],
					Practice.choicer(options, row.translate), round_number]
				return session_row


	# def checking_for_correctness()


	def first_round_updater(answer):
		row_to_change = Practice.first_round()
		right_code_number = row_to_change[0][4] + 1
		right_number_of_mistakes = row_to_change[0][5] + 1

		if answer == "right":
			Session.update(code_number=right_code_number).where(Session.id==row_to_change[0][0]).execute()

		else:
			Session.update(number_of_mistakes=right_number_of_mistakes).where(Session.id==row_to_change[0][0]).execute()
		

	def choicer(options, translate):
		final_options = [translate]
		while len(final_options) < 4:
			option = choice(options)
			if option not in final_options:
				final_options.append(option)
		final_options.sort()
		return final_options


	def session_table_deletion():
		session_query = Session.select()
		for row in session_query:
			Word.update(date=datetime.now().strftime("%Y%m%d%H%M%S")).where(Word.id==row.main_table_id).execute()
		db.drop_tables([Session])


# ch3_deleting
class Deletion:
	def __init__(self, *, words_ids=None, command=None):
		self.words_ids = words_ids
		self.command = command

	def obtainig_for_deletion(self):
		db.drop_tables([DelTable])
		confirmation_string = "Are you sure you wanna delete the records below:\n"
		for word_id in self.words_ids:
			data = {"del_id": word_id}

			db.create_tables([DelTable])
			with db.atomic():
				DelTable.create(**data)

			main_table_query = Word.select().where(Word.id==word_id)
			for row in main_table_query:
				list_for_deletion = f"\n{row.id}. {row.word} - {row.translate}"
				confirmation_string += list_for_deletion
		confirmation_string += "\nYes/No"
		return confirmation_string


	def completing_deletion(self):
		if self.command == "yes":
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



# Session.update(code_number=2).where(Session.id==row_to_change[0][0]).execute()










