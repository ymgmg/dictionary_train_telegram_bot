from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from config import API_KEY
from handlers import AddingHandler, BotCommands, DeletionHandler, PracticingHandler


def main() -> None:
    bot = Application.builder().token(API_KEY).build()

    bot.add_handler(CommandHandler("start", BotCommands.start))
    bot.add_handler(CommandHandler("main", BotCommands.main_page))
    bot.add_handler(MessageHandler(filters.Regex("(Show my\ndictionary)"), BotCommands.dict_shower))
    
    ch1_adding_new_word = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Add new\nword)"), AddingHandler.adding_start)],
        states={
            "adding_start":[MessageHandler(filters.TEXT, AddingHandler.get_data)],
            "adding_confirmation": [MessageHandler(filters.TEXT, AddingHandler.get_adding_confirmation)]
        },
        fallbacks=[],
        conversation_timeout=120
    )
    bot.add_handler(ch1_adding_new_word)

    ch2_practice = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Practice)"), PracticingHandler.practice_start)],
        states={
            "practice": [MessageHandler(filters.TEXT, PracticingHandler.practice_checking)]
        },
        fallbacks=[],
        conversation_timeout=60
    )
    bot.add_handler(ch2_practice)
    #переделать таблицу с добавлением столбца с ошибками), добавить возможность избрать лимит
    #сделать данетку

    ch3_delete_records = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Delete records)"), DeletionHandler.deletion_start)],
        states={
            "deletion_start": [MessageHandler(filters.TEXT, DeletionHandler.get_data_for_deletion)],
            "deletion_confirmation": [MessageHandler(filters.TEXT, DeletionHandler.get_deletion_confirmation)]
            },
        fallbacks=[],
        conversation_timeout=140
        )
    bot.add_handler(ch3_delete_records)


    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, BotCommands.echo))
    bot.run_polling()


if __name__ == "__main__":
    main()

