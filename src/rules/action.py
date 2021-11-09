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
        super(ActionType.DROP)


class ForwardAction (Action):

    forward_port: int

    def __init__(self, forward_port: int):
        self.forward_port = forward_port
        super(ActionType.FORWARD)


class ControllerAction (Action):

    def __init__(self):
        super(ActionType.CONTROLLER)


class SoftwareSwitchAction (Action):

    sw_switch_id: int

    def __init__(self, sw_switch_id: int):
        super(ActionType.SOFTWARE_SWITCH)
        self.sw_switch_id = sw_switch_id
