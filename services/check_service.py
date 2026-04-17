def _normalize_for_check(value: str) -> str:
    return "".join(value.split()).casefold()


def is_correct_answer(original: str, answer: str) -> bool:
    return _normalize_for_check(original) == _normalize_for_check(answer)


def format_sequence_with_errors(original: str, answer: str) -> str:
    original_chars = list(original)
    answer_chars = list(answer)
    max_len = max(len(original_chars), len(answer_chars))

    parts: list[str] = []
    for i in range(max_len):
        orig_char = original_chars[i] if i < len(original_chars) else ""
        ans_char = answer_chars[i] if i < len(answer_chars) else ""

        if not orig_char:
            continue

        if orig_char.casefold() != ans_char.casefold():
            parts.append(f"*{orig_char}*")
        else:
            parts.append(orig_char)

    return "".join(parts)
