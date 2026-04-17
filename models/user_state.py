from dataclasses import dataclass, field
from enum import Enum


class Lang(str, Enum):
    EN = "en"
    RU = "ru"


class LengthMode(str, Enum):
    FIXED = "fixed"
    RANGE = "range"


class DialogState(str, Enum):
    IDLE = "idle"
    WAITING_ANSWER = "waiting_answer"
    WAITING_FIXED_LENGTH = "waiting_fixed_length"
    WAITING_RANGE_MIN = "waiting_range_min"
    WAITING_RANGE_MAX = "waiting_range_max"


@dataclass
class LengthSettings:
    mode: LengthMode = LengthMode.FIXED
    fixed: int = 5
    min_len: int = 4
    max_len: int = 7


@dataclass
class UserState:
    lang: Lang = Lang.EN
    length_settings: LengthSettings = field(default_factory=LengthSettings)
    repeats_enabled: bool = True
    current_sequence: str = ""
    dialog_state: DialogState = DialogState.IDLE
    pending_range_min: int | None = None
