from telegram.ext import ConversationHandler

from adding.db_interaction import AddingDB
from general.db_interaction import create_user_table
from utils.reply_keyboards import ReplyKeyboard


class AddingHandler:
    async def adding_start(update, context) -> str:
        await update.message.reply_text("""Write a new word, please!\
            \nAdd the separator (:-) beetween the term and its meaning""")
        return "adding_start"

    async def get_data(update, context) -> None:
        user_text = update.message.text.split(":-")
        chat_id = update.message.chat.id
        if len(user_text) > 1:
            create_user_table(chat_id)
            AddingDB(chat_id=chat_id, data=user_text).creating_adding_table()
            checking_uniqueness = AddingDB(chat_id=chat_id).checking_uniqueness_of_new_word()
            addition = AddingDB(chat_id=chat_id).collect_addition()
            adding_confirmation = f"""Are you sure you want to add the word:\n
                {addition["word"]} - {addition["translate"]}\n(Yes/No)"""
            if len(checking_uniqueness) == 0:
                await update.message.reply_text(adding_confirmation, 
                    reply_markup=ReplyKeyboard.yn_keyboard())
            else:
                alike_rows = ""
                for row in checking_uniqueness:
                    alike_rows += f"\n{row[0]}. {row[1]} - {row[2]}"
                await update.message.reply_text(f"""It looks alike:\n{alike_rows}.\n\n
                    Maybe you would like to delete this(these) record(s) later""")
                await update.message.reply_text(adding_confirmation,
                    reply_markup=ReplyKeyboard.yn_keyboard())
            return "adding_confirmation"
        else:
            await update.message.reply_text("""Something went  wrong! Please, try again\n
                Maybe you forgot to use the separator(:-)""")
            return ConversationHandler.END

    async def get_adding_confirmation(update, context):
        user_text = update.message.text.lower()
        chat_id = update.message.chat.id
        if user_text == "yes":
            await update.message.reply_text("The word was added successfully.\nCongratulations!!!",
                reply_markup=ReplyKeyboard.main_keyboard())
        else:
            await update.message.reply_text("You cancelled adding",
                reply_markup=ReplyKeyboard.main_keyboard())
        AddingDB(chat_id=chat_id, command=user_text).main_table_converter()
        return ConversationHandler.END
