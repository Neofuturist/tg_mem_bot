import random

from models.user_state import Lang, LengthMode, LengthSettings


EN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWX"
RU_ALPHABET = "АБВГДЕЖЗИКЛМНОПРСТУФХЧШЯ"


def resolve_length(length_settings: LengthSettings) -> int:
    if length_settings.mode == LengthMode.FIXED:
        return length_settings.fixed
    return random.randint(length_settings.min_len, length_settings.max_len)


def generate_sequence(
    lang: Lang,
    length_settings: LengthSettings,
    repeats_enabled: bool = True,
) -> str:
    alphabet = EN_ALPHABET if lang == Lang.EN else RU_ALPHABET
    length = resolve_length(length_settings)

    if repeats_enabled:
        return "".join(random.choice(alphabet) for _ in range(length))

    unique_length = min(length, len(alphabet))
    return "".join(random.sample(alphabet, k=unique_length))


def format_sequence_for_display(sequence: str, pair_grouping_enabled: bool) -> str:
    if not pair_grouping_enabled:
        return sequence
    return " ".join(sequence[idx : idx + 2] for idx in range(0, len(sequence), 2))
