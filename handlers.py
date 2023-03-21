from datetime import datetime
from random import choice

from telegram.ext import ConversationHandler

from db_conventer import Adding, Deletion, Practice, db_content_shower
from utils import ReplyKeyboard


class BotCommands:
    async def start(update, context) -> None:
        user = update.effective_user
        await update.message.reply_html(rf"hi {user.mention_html()}", reply_markup=ReplyKeyboard.main_keyboard())


    async def main_page(update, context):
        await update.message.reply_text("You are at the main page", reply_markup=ReplyKeyboard.main_keyboard())


    async def dict_shower(update, context) -> None:
        await update.message.reply_text(db_content_shower("without_translate"))


    async def echo(update, context) -> None:
        # print(update)
        # print("#" * 20)
        # print(update.message.text)
        # await update.message.reply_text(update.message.chat.username)
        await update.message.reply_text("it doesn't look like one of our commands")


class AddingHandler:
    async def adding_start(update, context) -> str:
        await update.message.reply_text('''Write a new word, please!\nAdd the separator (:-) beetween the term and its meaning''')
        return "adding_start"


    async def get_data(update, context) -> None:
        user_text = update.message.text
        splited_text = user_text.split(":-")
        if len(splited_text) > 1:
            ch1_dict = {}
            ch1_dict["word"] = splited_text[0].strip().capitalize()
            translate = ""
            for element in splited_text[1:]:
                translate += element.strip()
            ch1_dict["translate"] = translate.capitalize()
            ch1_dict["date"] = datetime.now().strftime("%Y%m%d%H%M%S")
            Adding(data=ch1_dict).creating_adding_table()

            checking_uniqueness = Adding.checking_uniqueness_of_new_word()
            adding_confirmation = f'''Are you sure you want to add the word:\n{ch1_dict["word"]} - {ch1_dict["translate"]}\n(Yes/No)'''
            if len(checking_uniqueness) == 0:
                await update.message.reply_text(adding_confirmation, reply_markup=ReplyKeyboard.yn_keyboard()) 
            
            else:
                user_alike = ""
                for row in checking_uniqueness:
                    user_alike += f"\n{row[0]}. {row[1]} - {row[2]}"
                await update.message.reply_text(f"It looks alike:\n{user_alike}.\n\nMaybe you would like to delete this(these) record(s) later")
                await update.message.reply_text(adding_confirmation, reply_markup=ReplyKeyboard.yn_keyboard())
            return "adding_confirmation"
        else:
            await update.message.reply_text("Something went  wrong! Please, try again\nMaybe you forgot to use the separator(:-)")
            return ConversationHandler.END


    async def get_adding_confirmation(update, context):
        user_text = update.message.text.lower()
        if user_text == "yes":
            Adding(command="yes").main_table_converter()
            await update.message.reply_text("The word was added successfully.\nCongratulations!!!", reply_markup=ReplyKeyboard.main_keyboard())
        else:
            await update.message.reply_text("You cancelled adding", reply_markup=ReplyKeyboard.main_keyboard())
        return ConversationHandler.END


class PracticingHandler:
    async def practice_start(update, context):
        try:
            if Practice.checking_availability() >= 4:
                Practice.creating_practice_table()
                practice_item = Practice.first_round()
                print(practice_item)
                options_list = practice_item[1]
                await update.message.reply_text(f"Write translate to the word:\n{practice_item[0][2]}", reply_markup=ReplyKeyboard.options_keyboard(options_list))
                return "practice"

            else:
                await update.message.reply_text("You need to add at least 4 words")
                return ConversationHandler.END


        except TypeError:
            if Practice.checking_availability() == "No data":
                await update.message.reply_text("You don't have any dictionary")
                return ConversationHandler.END

    async def practice_checking(update, context):
        try:
            user_text = update.message.text
            checking_answer = Practice(answer_to_check=user_text).checking_for_correctness()
            if checking_answer == "right":

                await update.message.reply_text("You are right")
            else:
                await update.message.reply_text("You are wrong")
            practice_item = Practice.first_round()
            print(practice_item)

            options_list = practice_item[1]
            await update.message.reply_text(f"Write translate to the word:\n{practice_item[0][2] if practice_item[2]==1 else practice_item[0][3]}", reply_markup=ReplyKeyboard.options_keyboard(options_list))
            return "practice"


                
        except TypeError:
            Practice.session_table_deletion()
            await update.message.reply_text("Practice is over", reply_markup=ReplyKeyboard.main_keyboard())
            return ConversationHandler.END


class DeletionHandler():
    async def deletion_start(update, context):
        await update.message.reply_text(db_content_shower("with_translate"))
        await update.message.reply_text('''Enter ordinar nubers of records you want to delete through the sign (,)''')
        return "deletion_start"

    async def get_data_for_deletion(update, context):
        user_text = update.message.text.split(",")
        splited_user_text = []
        print(user_text)
        try:
            for item in user_text:
                splited_user_text.append(int(item))

            print(splited_user_text)
            await update.message.reply_text(Deletion(words_ids=splited_user_text).obtainig_for_deletion(), reply_markup=ReplyKeyboard.yn_keyboard())
            return "deletion_confirmation"
        except ValueError:
            await update.message.reply_text("Something went wrong.\nMaybe you didn't enter the number")


    async def get_deletion_confirmation(update, context):
        user_text = update.message.text.lower()
        if user_text == "yes":
            Deletion(command="yes").completing_deletion()
            await update.message.reply_text("The word is deleted", reply_markup=ReplyKeyboard.main_keyboard())
        else:
            Deletion(command="no").completing_deletion()
            await update.message.reply_text("You cancelled the deletion", reply_markup=ReplyKeyboard.main_keyboard())
        return ConversationHandler.END




