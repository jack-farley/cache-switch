from enum import Enum

from rules.action import Action, ActionType, SoftwareSwitchAction
from network.packet import Packet


class Rule:

    patterns = []
    action: Action
    priority: int

    counter: int

    def __init__(self, patterns, action: Action, priority: int):
        self.patterns = patterns
        self.action = action
        self.priority = priority
        self.counter = 0

    def matches(self, packet: Packet) -> bool:
        for pattern in self.patterns:
            if not pattern.matches(packet):
                return False
        return True

    def action(self) -> Action:
        return self.action

    def intersects(self, rule) -> bool:
        for pattern_1 in self.patterns:
            for pattern_2 in rule.patterns:
                if not pattern_1.intersects(pattern_2):
                    return False
        return True

    def increment_counter(self):
        self.counter += 1

    def create_cover_rule(self):
        return Rule(self.patterns, SoftwareSwitchAction(), self.priority)
