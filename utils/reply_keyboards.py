from telegram import ReplyKeyboardMarkup


class ReplyKeyboard:
    def main_keyboard():
        keyboard = ReplyKeyboardMarkup([
            ["OneToFour", "YesNo"],
            ["Add new\nword", "Delete records"]
        ], resize_keyboard=True)
        return keyboard

    def options_keyboard(options_list):
        keyboard = ReplyKeyboardMarkup([
            [f"{options_list_item}" for options_list_item in options_list[:2]],
            [f"{options_list_item}" for options_list_item in options_list[2:4]]
        ], resize_keyboard=True)
        return keyboard

    def yn_keyboard():
        keyboard = ReplyKeyboardMarkup([
            ["Yes", "No"],
        ], resize_keyboard=True)
        return keyboard
