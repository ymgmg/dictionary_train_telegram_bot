from datetime import datetime
from random import choice

from telegram.ext import ConversationHandler

from db_conventer import (db_adding_checking_uniqueness, db_adding_collecter, db_amount_checker, db_content_shower, db_deleting_finishing, db_deleting_record_collecting,
    db_main_table_conventer, db_nw_conventer, db_practice_table_creator, db_practice_first, db_session_deleter, db_session_updater_first)


from utils import *


async def start(update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"hi {user.mention_html()}", reply_markup=main_keyboard())


async def dict_shower(update, context) -> None:
    await update.message.reply_text(db_content_shower("without_translate"))


async def main_page(update, context):
    await update.message.reply_text("You are at the main page", reply_markup=main_keyboard())




async def ch1_start(update, context) -> str:
    await update.message.reply_text('''Write a new word, please!\nAdd the sign ":-" beetween the term and its meaning''')
    return "adding"

async def ch1_get_word(update, context) -> None:
    user_text = update.message.text
    splited_text = user_text.split(":-")
    if len(splited_text) > 1:
        ch1_dict = {}
        ch1_dict["word"] = splited_text[0].strip().capitalize()
        translate = ""
        for element in splited_text[1:]:
            translate += element.strip()
        ch1_dict["translate"] = translate.capitalize()
        ch1_dict["date"] = datetime.now().strftime("%Y%m%d%H%M")
        db_nw_conventer(ch1_dict)
        print(ch1_dict)



        adding_to_main = db_adding_checking_uniqueness()
        adding_confirmation = f'''Are you sure you want to add the word:\n{ch1_dict["word"]} - {ch1_dict["translate"]}\n(Yes/No)'''
        if len(adding_to_main) == 0:
            await update.message.reply_text(adding_confirmation) 
        
        else:
            user_alike = ""
            for el in adding_to_main:
                user_alike += f"\n{el[0]}. {el[1]} - {el[2]}"
            await update.message.reply_text(f"It looks alike:\n{user_alike}.\n\nMaybe you would like to delete this(these) record(s) later")
            await update.message.reply_text(adding_confirmation)
        return "adding_confirmation"
    else:
        await update.message.reply_text("Something went  wrong! Please, try again\nMaybe you forgot to use the separator(:-)")
        return ConversationHandler.END


async def ch1_get_confirmation(update, context):
    user_text = update.message.text.lower()
    # adding_data = 
    if user_text == "yes":
        db_main_table_conventer(db_adding_collecter(), "yes")
        await update.message.reply_text("The word was added successfully.\nCongratulations!!!")
    else:
        await update.message.reply_text("You cancelled adding")
    return ConversationHandler.END








async def ch2_start(update, context):
    try:
        if db_amount_checker() >= 4:
            db_practice_table_creator()
            practice_item = db_practice_first()
            print(practice_item)
            options_list = practice_item[1]
            await update.message.reply_text(f"Write translate to the word:\n{practice_item[0][2]}", reply_markup=options_keyboard(options_list))
            return "practice"

        else:
            await update.message.reply_text("You need to add at least 4 words")
            return ConversationHandler.END


    except TypeError:
        if db_amount_checker() == "No data":
            await update.message.reply_text("You don't have any dictionary")
            return ConversationHandler.END

async def ch2_checking(update, context):
    try:
        user_text = update.message.text.lower()

        if user_text == db_practice_first()[0][3].lower():
            db_session_updater_first()

            await update.message.reply_text("You are right")

            practice_item = db_practice_first()
            print(practice_item)

            options_list = practice_item[1]
            await update.message.reply_text(f"Write translate to the word:\n{practice_item[0][2]}", reply_markup=options_keyboard(options_list))
            return "practice"

        else:
            await update.message.reply_text("You are wrong")
            
            practice_item = db_practice_first()
            print(practice_item)
            options_list = practice_item[1]
            await update.message.reply_text(f"Write translate to the word:\n{practice_item[0][2]}", reply_markup=options_keyboard(options_list))
            return "practice"
    except TypeError:
        db_session_deleter()
        await update.message.reply_text("Practice is over", reply_markup=main_keyboard())
        return ConversationHandler.END









async def ch3_deleting(update, context):
    await update.message.reply_text(db_content_shower("with_translate"))
    await update.message.reply_text('''Enter ordinar nubers of records you want to delete through the sign ","''')
    return "delete"

async def ch3_confirmation(update, context):
    user_text = update.message.text
    print(user_text)
    user_list = user_text.split(",")
    print(user_list)
    await update.message.reply_text(db_deleting_record_collecting(user_list))
    return "confirmation"

async def ch3_finish(update, context):
    user_text = update.message.text.lower()
    if user_text == "yes":
        db_deleting_finishing("yes")
        await update.message.reply_text("The word is deleted")
    else:
        db_deleting_finishing("no")
        await update.message.reply_text("You cancelled deleting")
    return ConversationHandler.END




async def echo(update, context) -> None:
    print(update)
    print("#" * 20)
    print(update.message.text)
    await update.message.reply_text(update.message.chat.username)


