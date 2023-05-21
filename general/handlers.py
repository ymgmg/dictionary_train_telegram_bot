from general.db_interaction import db_content_shower, show_necessary_words
from utils.reply_keyboards import ReplyKeyboard


class BotCommands:
    async def start(update, context) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"hi {user.mention_html()}",
            reply_markup=ReplyKeyboard.main_keyboard())

    async def main_page(update, context):
        await update.message.reply_text(
            "You are at the main page",
            reply_markup=ReplyKeyboard.main_keyboard())

    async def dict_shower(update, context) -> None:
        chat_id = update.message.chat.id
        text = db_content_shower(chat_id=chat_id, command="without_translate")
        if not text:
            await update.message.reply_text("You don't have dictionary")
        else:
            await update.message.reply_text(text)

    async def echo(update, context) -> None:
        await update.message.reply_text(
            "it doesn't look like any of our commands",
            reply_markup=ReplyKeyboard.main_keyboard())

    async def necessity_counter(update, context):
        await update.message.reply_text(
            show_necessary_words(update.message.chat.id))
