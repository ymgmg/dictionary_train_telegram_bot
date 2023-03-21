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
	md_id = IntegerField()
	word = CharField()
	translate = CharField()
	code_number = IntegerField()

	class Meta:
		database = db
		# table_name = f"session{a}"
		table_name = "session"


class Adding(Model):
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
	query = Word.select()
	output_str = ""
	if command == "without_translate":
		for row in query:
			query_answer = f"{row.id}. {row.word}\n"
			output_str += query_answer
	elif command == "with_translate":
		for row in query:
			query_answer = f"{row.id}. {row.word} - {row.translate}\n"
			output_str += query_answer
	return output_str






##############################################
# ch1_adding
def db_nw_conventer(data: dict) -> None:
	db.drop_tables([Adding])
	db.create_tables([Adding])
	with db.atomic():
		Adding.create(**data)

def db_adding_checking_uniqueness():
	#not finished
	adding_collecter = db_adding_collecter()
	main_table_query = Word.select()
	looks_alike = []
	for row in main_table_query:
		main_query_answer = [row.id, row.word, row.translate]
		if main_query_answer[1] == adding_collecter["word"] or main_query_answer[2] == adding_collecter["translate"]:
			looks_alike.append(main_query_answer)
	return looks_alike


def db_adding_collecter():
	query = Adding.select()
	for row in query:
		query_answer = {
			"word": row.word,
			"translate":row.translate,
			"date": datetime.now().strftime("%Y%m%d%H%M")
			}
	return query_answer


def db_main_table_conventer(data: dict, command: str) -> None:
	if command == "yes":
		db.create_tables([Word])
		with db.atomic():
			Word.create(**data)
	db.drop_tables([Adding])




##############################################
# ch2_practice

def db_amount_checker():
	try:
		query = Word.select()
		return len(query)
	except OperationalError:
		return "No data"


def db_practice_table_creator() -> list:
	db.drop_tables([Session])
	db.create_tables([Session])
	query = Word.select().order_by(Word.date).limit(3)
	for row in query:
		query_answer = {
			"md_id": row.id,
			"word": row.word,
			"translate": row.translate,
			"code_number": 1}
		with db.atomic():
			Session.create(**query_answer)


def db_practice_first():
	query = Session.select().where(Session.code_number==1).order_by(Session.md_id.desc())
	options_query = Word.select()
	options = [option.translate for option in options_query]
	# print(query)
	# print(type(query))
	for row in query:
		query_answer = [[row.id, row.md_id, row.word, row.translate, row.code_number], choicer(options, row.translate)]
		return query_answer


def db_session_updater_first():
	source = db_practice_first()
	query = Session.update(code_number=2).where(Session.id==source[0][0]).execute()
	

def choicer(options, translate):
	final_options = [translate]
	while len(final_options) < 4:
		option = choice(options)
		if option not in final_options:
			final_options.append(option)
	final_options.sort()
	return final_options


def db_session_deleter():
	db.drop_tables([Session])



################################################
# ch3_deleting

def db_deleting_record_collecting(words_ids):
	db.drop_tables([DelTable])
	just_string = "Are you sure you wanna delete the records below:\n"
	for word_id in words_ids:
		worden_id = int(word_id)
		data = {"del_id": worden_id}

		
		db.create_tables([DelTable])
		with db.atomic():
			DelTable.create(**data)

		query = Word.select().where(Word.id==worden_id)
		for el in query:
			cycle_del_list = f"\n{el.id}. {el.word} - {el.translate}"
			just_string += cycle_del_list
		just_string += "\nYes/No"
	return just_string


def db_deleting_finishing(command: str):
	if command == "yes":
		query = DelTable.select()
		for item in query:
			Word.delete().where(Word.id==item.del_id).execute()
		db.drop_tables([DelTable])
	else:
		db.drop_tables([DelTable])









#удаляет таблицу
# db.drop_tables([Session])

#удаляет строки
# Session.delete().where(table.x==y).execute()





