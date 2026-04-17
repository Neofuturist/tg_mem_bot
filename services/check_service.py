def _normalize_for_check(value: str) -> str:
    return "".join(value.split()).casefold()


def is_correct_answer(original: str, answer: str) -> bool:
    return _normalize_for_check(original) == _normalize_for_check(answer)


def format_sequence_with_errors(original: str, answer: str) -> str:
    normalized_answer_chars = [ch for ch in answer if not ch.isspace()]

    answer_idx = 0
    parts: list[str] = []

    for orig_char in original:
        if orig_char.isspace():
            parts.append(orig_char)
            continue

        ans_char = normalized_answer_chars[answer_idx] if answer_idx < len(normalized_answer_chars) else ""
        answer_idx += 1

        if orig_char.casefold() != ans_char.casefold():
            parts.append(f"*{orig_char}*")
        else:
            parts.append(orig_char)

    return "".join(parts)
