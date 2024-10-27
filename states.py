from enum import Enum, auto

class State(Enum):
    """
    Перечисление состояний для FSM.
    """
    NONE = auto()
    REGISTRATION_NAME = auto()
    REGISTRATION_LOGIN = auto()
    CREATE_TASK_TITLE = auto()
    CREATE_TASK_DESCRIPTION = auto()
