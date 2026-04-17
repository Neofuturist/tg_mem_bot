from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def remembered_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Запомнил", callback_data="remembered")]]
    )


def answer_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Продолжить", callback_data="continue_training")]]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Начать тренировку", callback_data="start_training")],
            [InlineKeyboardButton(text="Настройки", callback_data="open_settings")],
        ]
    )


def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Язык: English", callback_data="set_lang_en")],
            [InlineKeyboardButton(text="Язык: Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton(text="Длина: фиксированная", callback_data="len_mode_fixed")],
            [InlineKeyboardButton(text="Длина: диапазон", callback_data="len_mode_range")],
            [InlineKeyboardButton(text="Назад", callback_data="back_main")],
        ]
    )
