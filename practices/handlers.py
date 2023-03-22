from telegram.ext import ConversationHandler

from general.db_interaction import show_necessary_words
from practices.db_interaction import PracticeOneToFour
from utils.reply_keyboards import ReplyKeyboard


class PracticingHandler:
    async def start(update, context):
        chat_id = update.message.chat.id
        try:
            if PracticeOneToFour(chat_id=chat_id).checking_availability() >= 4:
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
            if PracticeOneToFour.checking_availability() == "No data":
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
            print(practice_item)
            options_list = practice_item["choosed_options"]
            await update.message.reply_text(
                f"""Write translate to the word:\n{practice_item["word"]}""",
                reply_markup=ReplyKeyboard.options_keyboard(options_list))
            return "practice"
        except ValueError:
            await update.message.reply_text(
                "Something went wrong!!\nMaybe you didn't enter a number")
            ConversationHandler.END

    async def checking(update, context):
        user_text = update.message.text
        chat_id = update.message.chat.id
        try:
            checking_answer = PracticeOneToFour(
                chat_id=chat_id, answer_to_check=user_text
                ).checking_for_correctness()
            print(checking_answer)
            if checking_answer == "right":
                await update.message.reply_text("You are right")
            else:
                await update.message.reply_text("You are wrong")

            practice_item = PracticeOneToFour(chat_id=chat_id).process()

            if practice_item["round_number"] == 1:
                question_item = practice_item["word"]
            else:
                question_item = practice_item["translate"]
            options_list = practice_item["choosed_options"]
            await update.message.reply_text(
                f"Write translate to the word:\n{question_item}",
                reply_markup=ReplyKeyboard.options_keyboard(options_list))
            return "practice"

        except TypeError:
            PracticeOneToFour(chat_id=chat_id).session_table_deletion()
            stat = PracticeOneToFour(chat_id=chat_id).process_stat()
            try:
                result = round(
                    stat["right_answers"] / stat["all_answers"] * 100, 2)
            except ZeroDivisionError:
                result = 0
            await update.message.reply_text("Practice is over")
            await update.message.reply_text(
                f"Your result is {result}%",
                reply_markup=ReplyKeyboard.main_keyboard())
            return ConversationHandler.END
