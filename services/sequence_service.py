import random

from models.user_state import Lang, LengthMode, LengthSettings


EN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWX"
RU_ALPHABET = "АБВГДЕЖЗИКЛМНОПРСТУФХЧШЯ"


def resolve_length(length_settings: LengthSettings) -> int:
    if length_settings.mode == LengthMode.FIXED:
        return length_settings.fixed
    return random.randint(length_settings.min_len, length_settings.max_len)


def generate_sequence(lang: Lang, length_settings: LengthSettings) -> str:
    alphabet = EN_ALPHABET if lang == Lang.EN else RU_ALPHABET
    length = resolve_length(length_settings)
    return "".join(random.choice(alphabet) for _ in range(length))
