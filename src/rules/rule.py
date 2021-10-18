from enum import Enum

from rules.action import Action
from rules.pattern import Pattern
from packet import Packet


class Rule:

    patters = []
    action: Action
    priority: int

    def __init__(self, patterns, action: Action, priority: int):
        self.patterns = patterns
        self.action = action
        self.priority = priority

    def matches(self, packet: Packet) -> bool:
        for pattern in self.patterns:
            if not pattern.matches(packet):
                return False
        return True

    def action(self) -> Action:
        return self.action
