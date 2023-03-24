from telegram import ReplyKeyboardMarkup


class ReplyKeyboard:
    def main_keyboard():
        keyboard = ReplyKeyboardMarkup([
            ["OneToFour", "YesNo"],
            ["Add new\nword", "Delete records"]
        ], resize_keyboard=True)
        return keyboard

    def options_keyboard(options):
        keyboard = ReplyKeyboardMarkup([
            [f"{option}" for option in options[:2]],
            [f"{option}" for option in options[2:4]]
        ], resize_keyboard=True)
        return keyboard

    def yn_practice_keyboard(option):
        keyboard = ReplyKeyboardMarkup([
            [option, f"Not {option}"],
        ], resize_keyboard=True)
        return keyboard

    def yn_keyboard():
        keyboard = ReplyKeyboardMarkup([
            ["Yes", "No"],
        ], resize_keyboard=True)
        return keyboard
