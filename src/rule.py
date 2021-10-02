from enum import Enum


class ActionType (Enum):
    DROP = 0
    FORWARD = 1
    CONTROLLER = 2
    MODIFY_HEADER = 3


class Rule:

    patters = []
    priority: int
    counters = []
