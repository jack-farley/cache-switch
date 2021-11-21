from sortedcontainers import SortedKeyList
from rules.rule import Rule
from rules.action import Action
from packet import Packet


class Table:

    rules: SortedKeyList

    def __init__(self):
        """Create a new table."""
        self.rules = SortedKeyList([], key=lambda r: r.priority)

    def add_rule(self, rule: Rule):
        """Add a rule to this table."""
        self.rules.add(rule)

    def remove_rule(self, rule: Rule):
        """Remove a rule from this table."""
        self.rules.remove(rule)

    def get_action(self, packet: Packet):
        """
        Get the action associated with a the highest priority matching rule.
        If no rule matches, this will return None.
        """
        action: Action = None
        for rule in self.rules.__reversed__():
            if rule.matches(packet):
                action = rule.action
                rule.increment_counter()
                break

        return action
