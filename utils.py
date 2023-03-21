from telegram import ReplyKeyboardMarkup

# -> <class 'function'>
def main_keyboard():
    keyboard = ReplyKeyboardMarkup([
        ["Add new\nword", "Show my\ndictionary"],
        ["Delete records", "Practice"]
    ], resize_keyboard=True)
    return keyboard


def options_keyboard(options_list):
    keyboard = ReplyKeyboardMarkup([
        [f"{options_list_item}" for options_list_item in options_list[:2]],
        [f"{options_list_item}" for options_list_item in options_list[2:4]],
        ["Main page"]

    ], resize_keyboard=True)
    return keyboard

