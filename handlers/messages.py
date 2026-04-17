from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from keyboards.inline import (
    answer_result_keyboard,
    main_menu_keyboard,
    remembered_keyboard,
    settings_keyboard,
)
from models.user_state import DialogState, LengthMode
from services.check_service import format_sequence_with_errors, is_correct_answer
from services.sequence_service import generate_sequence
from storage.user_state_repository import UserStateRepository


def build_messages_handlers(repo: UserStateRepository) -> list[object]:
    async def show_main_menu(message) -> None:
        await message.reply_text(
            "Выберите действие:",
            reply_markup=main_menu_keyboard(),
        )

    async def show_settings(message, user_id: int) -> None:
        state = repo.get_or_create(user_id)
        await message.reply_text(
            "Настройки:",
            reply_markup=settings_keyboard(state.repeats_enabled),
        )

    async def start_training(message, user_id: int) -> None:
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

    async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        if message is None or user is None:
            return

        await show_main_menu(message)

    async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        if message is None:
            return

        await message.reply_text(
            "Команды:\n"
            "/help — показать эту справку\n"
            "/setup — открыть настройки\n"
            "/play — начать тренировку"
        )

    async def setup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        if message is None or user is None:
            return

        await show_settings(message, user.id)

    async def play_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        if message is None or user is None:
            return

        await start_training(message, user.id)

    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        if message is None or user is None or message.text is None:
            return

        state = repo.get_or_create(user.id)
        text = message.text.strip()

        if state.dialog_state == DialogState.WAITING_FIXED_LENGTH:
            if not text.isdigit() or int(text) <= 0:
                await message.reply_text("Введите положительное целое число.")
                return
            state.length_settings.mode = LengthMode.FIXED
            state.length_settings.fixed = int(text)
            state.dialog_state = DialogState.IDLE
            await message.reply_text("Фиксированная длина сохранена.")
            return

        if state.dialog_state == DialogState.WAITING_RANGE_MIN:
            if not text.isdigit() or int(text) <= 0:
                await message.reply_text("Введите положительное целое число для минимума.")
                return
            state.pending_range_min = int(text)
            state.dialog_state = DialogState.WAITING_RANGE_MAX
            await message.reply_text("Введите максимальную длину диапазона:")
            return

        if state.dialog_state == DialogState.WAITING_RANGE_MAX:
            if not text.isdigit() or int(text) <= 0:
                await message.reply_text("Введите положительное целое число для максимума.")
                return
            max_len = int(text)
            min_len = state.pending_range_min or 1
            if max_len < min_len:
                await message.reply_text("Максимум должен быть не меньше минимума.")
                return
            state.length_settings.mode = LengthMode.RANGE
            state.length_settings.min_len = min_len
            state.length_settings.max_len = max_len
            state.pending_range_min = None
            state.dialog_state = DialogState.IDLE
            await message.reply_text("Диапазон длины сохранен.")
            return

        if state.dialog_state == DialogState.WAITING_ANSWER:
            original = state.current_sequence
            answer = text
            ok = is_correct_answer(original, answer)
            highlighted = format_sequence_with_errors(original, answer)

            if ok:
                await message.reply_text(
                    f"Верно!\nОригинал: `{original}`",
                    parse_mode="Markdown",
                    reply_markup=answer_result_keyboard(),
                )
            else:
                await message.reply_text(
                    f"Неверно.\nОригинал: {highlighted}",
                    parse_mode="Markdown",
                    reply_markup=answer_result_keyboard(),
                )

            state.current_sequence = ""
            state.dialog_state = DialogState.IDLE
            return

        await message.reply_text("Используйте /help, /setup или /play.")

    return [
        CommandHandler("start", start_cmd),
        CommandHandler("help", help_cmd),
        CommandHandler("setup", setup_cmd),
        CommandHandler("play", play_cmd),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text),
    ]
