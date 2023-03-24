from telegram.ext import (
    Application, CommandHandler, ConversationHandler, MessageHandler, filters)

from config import API_KEY
from general.handlers import BotCommands
from adding.handlers import AddingHandler
from deletion.handlers import DeletionHandler
from practices.handlers import OneToFourHandler, YesNoHandler


def main() -> None:
    bot = Application.builder().token(API_KEY).build()

    bot.add_handler(CommandHandler("start", BotCommands.start))
    bot.add_handler(CommandHandler("main", BotCommands.main_page))
    bot.add_handler(CommandHandler("show_dictionary", BotCommands.dict_shower))
    bot.add_handler(CommandHandler(
        "needs_to_train", BotCommands.necessity_counter))

    adding_new_word = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex("(Add new\nword)"), AddingHandler.start)],
        states={
            "start": [MessageHandler(filters.TEXT, AddingHandler.get_data)],
            "confirmation": [MessageHandler(
                filters.TEXT, AddingHandler.get_confirmation)]
        },
        fallbacks=[],
        conversation_timeout=120
    )
    bot.add_handler(adding_new_word)

    delete_records = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex("(Delete records)"), DeletionHandler.start)],
        states={
            "start": [MessageHandler(filters.TEXT, DeletionHandler.get_data)],
            "confirmation": [MessageHandler(
                filters.TEXT, DeletionHandler.confirmation)]
        },
        fallbacks=[],
        conversation_timeout=140
    )
    bot.add_handler(delete_records)

    practice_one_to_four = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex("(OneToFour)"), OneToFourHandler.start)],
        states={
            "select_number": [MessageHandler(
                filters.TEXT, OneToFourHandler.select_number)],
            "practice": [MessageHandler(
                filters.TEXT, OneToFourHandler.checking)],
        },
        fallbacks=[],
        conversation_timeout=60
    )
    bot.add_handler(practice_one_to_four)

    practice_yes_no = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex("(YesNo)"), YesNoHandler.start)],
        states={
            "select_number": [MessageHandler(
                filters.TEXT, YesNoHandler.select_number)],
            "practice": [MessageHandler(
                filters.TEXT, YesNoHandler.checking)],
        },
        fallbacks=[],
        conversation_timeout=60
    )
    bot.add_handler(practice_yes_no)

    bot.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, BotCommands.echo))
    bot.run_polling()


if __name__ == "__main__":
    main()
