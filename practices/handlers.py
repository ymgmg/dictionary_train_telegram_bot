from telegram.ext import ConversationHandler

from general.db_interaction import show_necessary_words
from practices.db_interaction import PracticeOneToFour, PracticeYesNo
from utils.reply_keyboards import ReplyKeyboard


class OneToFourHandler:
    async def start(update, context):
        chat_id = update.message.chat.id
        dict_condition = PracticeOneToFour(
            chat_id=chat_id).dictionary_checking()
        try:
            if dict_condition >= 4:
                await update.message.reply_text(show_necessary_words(chat_id))
                await update.message.reply_text(
                    "Please choose amount of words you want to train",
                    reply_markup=ReplyKeyboard.main_keyboard())
                return "select_number"

            else:
                await update.message.reply_text(
                    "You need to add at least 4 words")
                return ConversationHandler.END

        except TypeError:
            if dict_condition == "No data":
                await update.message.reply_text(
                    "You don't have any dictionary")
                return ConversationHandler.END

    async def select_number(update, context):
        user_text = update.message.text
        chat_id = update.message.chat.id

        try:
            PracticeOneToFour(
                chat_id=chat_id, session_amount=int(user_text)
                ).creating_practice_table()
            practice_item = PracticeOneToFour(chat_id=chat_id).process()
            if practice_item["round_number"] == 1:
                question_item = practice_item["word"]
            else:
                question_item = practice_item["translate"]

            options = practice_item["choosed_options"]
            await update.message.reply_text(
                f"""Write translate to the word:\n{question_item}""",
                reply_markup=ReplyKeyboard.options_keyboard(options))
            return "practice"
        except ValueError:
            await update.message.reply_text(
                "Something went wrong!!\nMaybe you didn't enter a number")
            ConversationHandler.END

    async def checking(update, context):
        user_text = update.message.text
        chat_id = update.message.chat.id
        try:
            is_correct = PracticeOneToFour(
                chat_id=chat_id, answer_to_check=user_text
                ).correctness_checking()
            if is_correct is True:
                await update.message.reply_text("You are right")
            else:
                await update.message.reply_text("You are wrong")

            practice_item = PracticeOneToFour(chat_id=chat_id).process()

            if practice_item["round_number"] == 1:
                question_item = practice_item["word"]
            else:
                question_item = practice_item["translate"]
            options = practice_item["choosed_options"]
            await update.message.reply_text(
                f"Write translate to the word:\n{question_item}",
                reply_markup=ReplyKeyboard.options_keyboard(options))
            return "practice"

        except TypeError:
            result = PracticeOneToFour(chat_id=chat_id).final_stat()
            PracticeOneToFour(chat_id=chat_id).session_table_deletion()

            await update.message.reply_text("Practice is over")
            await update.message.reply_text(
                f"Your practice result is {result['session_stat']}% \
                Your all time result is {result['overall_stat']}%",
                reply_markup=ReplyKeyboard.main_keyboard())
            return ConversationHandler.END


class YesNoHandler:
    async def start(update, context):
        chat_id = update.message.chat.id
        dict_condition = PracticeYesNo(
            chat_id=chat_id).dictionary_checking()
        try:
            if dict_condition >= 4:
                await update.message.reply_text(show_necessary_words(chat_id))
                await update.message.reply_text(
                    "Please choose amount of words you want to train",
                    reply_markup=ReplyKeyboard.main_keyboard())
                return "select_number"

            else:
                await update.message.reply_text(
                    "You need to add at least 4 words")
                return ConversationHandler.END

        except TypeError:
            if dict_condition == "No data":
                await update.message.reply_text(
                    "You don't have any dictionary")
                return ConversationHandler.END

    async def select_number(update, context):
        user_text = update.message.text
        chat_id = update.message.chat.id

        try:
            PracticeYesNo(
                chat_id=chat_id, session_amount=int(user_text)
                ).creating_practice_table()
            practice_item = PracticeYesNo(chat_id=chat_id).process()
            if practice_item["round_number"] == 1:
                question_item = practice_item["word"]
            else:
                question_item = practice_item["translate"]

            option = practice_item["choosed_options"]
            await update.message.reply_text(
                f"""Write translate to the word:\n{question_item}""",
                reply_markup=ReplyKeyboard.yn_practice_keyboard(option))
            return "practice"
        except ValueError:
            await update.message.reply_text(
                "Something went wrong!!\nMaybe you didn't enter a number")
            ConversationHandler.END

    async def checking(update, context):
        user_text = update.message.text
        chat_id = update.message.chat.id
        try:
            is_correct = PracticeYesNo(
                chat_id=chat_id, answer_to_check=user_text
                ).correctness_checking()
            if is_correct is True:
                await update.message.reply_text("You are right")
            else:
                await update.message.reply_text("You are wrong")

            practice_item = PracticeYesNo(chat_id=chat_id).process()

            if practice_item["round_number"] == 1:
                question_item = practice_item["word"]
            else:
                question_item = practice_item["translate"]
            option = practice_item["choosed_options"]
            await update.message.reply_text(
                f"Write translate to the word:\n{question_item}",
                reply_markup=ReplyKeyboard.yn_practice_keyboard(option))
            return "practice"

        except TypeError:
            result = PracticeYesNo(chat_id=chat_id).final_stat()
            PracticeYesNo(chat_id=chat_id).session_table_deletion()

            await update.message.reply_text("Practice is over")
            await update.message.reply_text(
                f"Your practice result is {result['session_stat']}% \
                Your all time result is {result['overall_stat']}%",
                reply_markup=ReplyKeyboard.main_keyboard())
            return ConversationHandler.END
