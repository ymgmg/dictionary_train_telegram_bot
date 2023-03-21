from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from config import API_KEY
from handlers import *


def main() -> None:
    bot = Application.builder().token(API_KEY).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.Regex("(Show my\ndictionary)"), dict_shower))
    bot.add_handler(MessageHandler(filters.Regex("(Main page)"), main_page))

    
    ch1_new_word = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Add new\nword)"), ch1_start)],
        states={
            "adding":[MessageHandler(filters.TEXT, ch1_get_word)],
            "adding_confirmation": [MessageHandler(filters.TEXT, ch1_get_confirmation)]
        },
        fallbacks=[],
        conversation_timeout=120
    )
    bot.add_handler(ch1_new_word)

    ch2_practice = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Practice)"), ch2_start)],
        states={
            "practice": [MessageHandler(filters.TEXT, ch2_checking)]
        },
        fallbacks=[],
        conversation_timeout=60
    )
    bot.add_handler(ch2_practice)
    #переделать таблицу с добавлением столбца с ошибками), добавить возможность избрать лимит
    #сделать данетку

    ch3_delete_records = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("(Delete records)"), ch3_deleting)],
        states={
            "delete": [MessageHandler(filters.TEXT, ch3_confirmation)],
            "confirmation": [MessageHandler(filters.TEXT, ch3_finish)]
            },
        fallbacks=[],
        conversation_timeout=140
        )
    bot.add_handler(ch3_delete_records)
    #сделать смену индексов когда удаляется слово из середины


    #добавить клавиатуры confirmation (mb inline)


    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    bot.run_polling()


if __name__ == "__main__":
    main()

