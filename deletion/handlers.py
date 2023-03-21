from telegram.ext import ConversationHandler

from deletion.db_interaction import DeletionDB
from general.db_interaction import db_content_shower
from utils.reply_keyboards import ReplyKeyboard



class DeletionHandler:
    async def deletion_start(update, context):
        chat_id = update.message.chat.id
        await update.message.reply_text(db_content_shower(chat_id=chat_id, command="with_translate"))
        await update.message.reply_text("""Enter ordinar numbers of the records \
            you want to delete through the sign (,)""")
        return "deletion_start"

    async def get_data_for_deletion(update, context):
        user_text = update.message.text
        user_text = DeletionHandler.user_text_checker(user_text=user_text.split(","))
        chat_id = update.message.chat.id
        if user_text is False:
            await update.message.reply_text("""Something went wrong.\n
                Maybe you didn't enter the number""")
            return ConversationHandler.END

        else:
            confirmation_string = "Are you sure you wanna delete the records below:\n"
            confirmation_string += DeletionDB(chat_id=chat_id, ids_to_delete=user_text).obtainig_for_deletion()
            confirmation_string += "\n\nYes/No"

            await update.message.reply_text(confirmation_string,
                reply_markup=ReplyKeyboard.yn_keyboard())
            return "deletion_confirmation"

    async def get_deletion_confirmation(update, context):
        user_text = update.message.text.lower()
        chat_id = update.message.chat.id
        if user_text == "yes":
            DeletionDB(chat_id=chat_id).completing_deletion()
            await update.message.reply_text("The record is deleted",
                reply_markup=ReplyKeyboard.main_keyboard())

        else:
            await update.message.reply_text("You cancelled the deletion",
                reply_markup=ReplyKeyboard.main_keyboard())
        return ConversationHandler.END

    def user_text_checker(*, user_text):
        try:
            for item in user_text:
                if user_text.count(item) > 1:
                    user_text.remove(item)
                else:
                    item_index = user_text.index(item)
                    user_text.remove(item)
                    user_text.insert(item_index, (int(item)))
            user_text.sort()
            return user_text

        except ValueError:
            return False
