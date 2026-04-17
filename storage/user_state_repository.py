from models.user_state import DialogState, UserState


class UserStateRepository:
    def __init__(self) -> None:
        self._states: dict[int, UserState] = {}

    def clear_session_state(self, user_id: int) -> UserState:
        state = self.get_or_create(user_id)
        state.current_sequence = ""
        state.dialog_state = DialogState.IDLE
        state.pending_range_min = None
        return state

    def get_or_create(self, user_id: int) -> UserState:
        if user_id not in self._states:
            self._states[user_id] = UserState()
        return self._states[user_id]

    def get(self, user_id: int) -> UserState | None:
        return self._states.get(user_id)

