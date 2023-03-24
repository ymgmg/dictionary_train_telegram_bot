from telegram.ext import ConversationHandler

from deletion.db_interaction import DeletionDB
from general.db_interaction import db_content_shower
from utils.reply_keyboards import ReplyKeyboard


class DeletionHandler:
    async def start(update, context):
        chat_id = update.message.chat.id
        data_content = db_content_shower(
            chat_id=chat_id, command="with_translate")
        if data_content is False:
            await update.message.reply_text(
                "You don't have records to delete")
            return ConversationHandler.END
        else:
            await update.message.reply_text(data_content)
            await update.message.reply_text((
                "Enter ordinar numbers of the records "
                "you want to delete through the sign (,)"
                ))
            return "start"

    async def get_data(update, context):
        user_text = update.message.text
        user_text = DeletionHandler.user_text_checker(
            user_text=user_text.split(","))
        chat_id = update.message.chat.id
        if user_text is False:
            await update.message.reply_text("""Something went wrong.\
                \nMaybe you didn't enter the number""")
            return ConversationHandler.END

        else:
            confirmation = "Are you sure you wanna delete the records below:\n"
            confirmation += DeletionDB(
                chat_id=chat_id, ids_to_delete=user_text
                ).obtainig_for_deletion()
            confirmation += "\n\nYes/No"

            await update.message.reply_text(
                confirmation,
                reply_markup=ReplyKeyboard.yn_keyboard())
            return "confirmation"

    async def confirmation(update, context):
        user_text = update.message.text.lower()
        chat_id = update.message.chat.id
        if user_text == "yes":
            DeletionDB(chat_id=chat_id).completing_deletion()
            await update.message.reply_text(
                "The record is deleted",
                reply_markup=ReplyKeyboard.main_keyboard())
        else:
            await update.message.reply_text(
                "You cancelled the deletion",
                reply_markup=ReplyKeyboard.main_keyboard())
        return ConversationHandler.END

    def user_text_checker(*, user_text):
        for item in user_text:
            if user_text.count(item) > 1:
                user_text.remove(item)
            else:
                item_index = user_text.index(item)
                user_text.remove(item)
                try:
                    user_text.insert(item_index, (int(item)))
                except ValueError:
                    continue
        if len(user_text) == 0:
            return False
        else:
            user_text.sort()
            return user_text
