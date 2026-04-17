from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from keyboards.inline import (
    main_menu_keyboard,
    remembered_keyboard,
    settings_keyboard,
)
from models.user_state import DialogState, Lang, LengthMode
from services.sequence_service import generate_sequence
from storage.user_state_repository import UserStateRepository


def build_callbacks_handlers(repo: UserStateRepository) -> list[CallbackQueryHandler]:
    async def _send_training_sequence(message, user_id: int) -> None:
        state = repo.get_or_create(user_id)
        sequence = generate_sequence(
            state.lang,
            state.length_settings,
            state.repeats_enabled,
        )
        state.current_sequence = sequence
        state.dialog_state = DialogState.IDLE
        await message.reply_text(
            f"Запомните последовательность:\n\n`{sequence}`",
            parse_mode="Markdown",
            reply_markup=remembered_keyboard(),
        )

    async def open_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "open_settings" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        await query.message.edit_text(
            "Настройки:",
            reply_markup=settings_keyboard(state.repeats_enabled),
        )
        await query.answer()

    async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "back_main" or query.message is None:
            return

        await query.message.edit_text(
            "Выберите действие:",
            reply_markup=main_menu_keyboard(),
        )
        await query.answer()

    async def continue_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "continue_training" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        await _send_training_sequence(query.message, user.id)
        await query.answer()

    async def set_lang_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "set_lang_en":
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        state.lang = Lang.EN
        await query.answer("Язык: English")

    async def set_lang_ru(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "set_lang_ru":
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        state.lang = Lang.RU
        await query.answer("Язык: Русский")

    async def toggle_repeats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "toggle_repeats" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        state.repeats_enabled = not state.repeats_enabled
        status_text = "Вкл" if state.repeats_enabled else "Откл"
        await query.message.edit_text(
            "Настройки:",
            reply_markup=settings_keyboard(state.repeats_enabled),
        )
        await query.answer(f"Повторы: {status_text}")

    async def len_mode_fixed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "len_mode_fixed" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        state.length_settings.mode = LengthMode.FIXED
        state.dialog_state = DialogState.WAITING_FIXED_LENGTH
        await query.message.reply_text("Введите фиксированную длину (например, 5):")
        await query.answer()

    async def len_mode_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "len_mode_range" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        state.length_settings.mode = LengthMode.RANGE
        state.dialog_state = DialogState.WAITING_RANGE_MIN
        state.pending_range_min = None
        await query.message.reply_text("Введите минимальную длину диапазона:")
        await query.answer()

    async def start_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "start_training" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        sequence = generate_sequence(state.lang, state.length_settings)
        state.current_sequence = sequence
        state.dialog_state = DialogState.IDLE
        await query.message.reply_text(
            f"Запомните последовательность:\n\n`{sequence}`",
            parse_mode="Markdown",
            reply_markup=remembered_keyboard(),
        )
        await query.answer()

    async def remembered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None or query.data != "remembered" or query.message is None:
            return

        user = query.from_user
        if user is None:
            return

        state = repo.get_or_create(user.id)
        if not state.current_sequence:
            await query.answer("Нет активной последовательности")
            return

        state.dialog_state = DialogState.WAITING_ANSWER
        await query.message.delete()
        await query.message.reply_text("Введите последовательность по памяти:")
        await query.answer()

    return [
        CallbackQueryHandler(open_settings, pattern="^open_settings$"),
        CallbackQueryHandler(back_main, pattern="^back_main$"),
        CallbackQueryHandler(continue_training, pattern="^continue_training$"),
        CallbackQueryHandler(set_lang_en, pattern="^set_lang_en$"),
        CallbackQueryHandler(set_lang_ru, pattern="^set_lang_ru$"),
        CallbackQueryHandler(toggle_repeats, pattern="^toggle_repeats$"),
        CallbackQueryHandler(len_mode_fixed, pattern="^len_mode_fixed$"),
        CallbackQueryHandler(len_mode_range, pattern="^len_mode_range$"),
        CallbackQueryHandler(start_training, pattern="^start_training$"),
        CallbackQueryHandler(remembered, pattern="^remembered$"),
    ]
