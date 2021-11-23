from enum import Enum


class ActionType (Enum):
    DROP = 0
    FORWARD = 1
    CONTROLLER = 2
    MODIFY_HEADER = 3
    SOFTWARE_SWITCH = 4


class Action:

    type: ActionType

    def __init__(self, type: ActionType):
        self.type = type


class DropAction (Action):

    def __init__(self):
        super().__init__(ActionType.DROP)


class ForwardAction (Action):

    forward_port: int

    def __init__(self, forward_port: int):
        self.forward_port = forward_port
        super().__init__(ActionType.FORWARD)


class ControllerAction (Action):

    def __init__(self):
        super().__init__(ActionType.CONTROLLER)


class SoftwareSwitchAction (Action):

    def __init__(self):
        super().__init__(ActionType.SOFTWARE_SWITCH)
