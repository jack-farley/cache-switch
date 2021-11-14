from enum import Enum

from rules.action import Action
from rules.rule import Rule
from packet import Packet


class Rule:

    patterns = []
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

    def intersects(self, rule: Rule) -> bool:
        for pattern_1 in self.patterns:
            for pattern_2 in rule.patterns:
                if not pattern_1.intersects(pattern_2):
                    return False
        return True
