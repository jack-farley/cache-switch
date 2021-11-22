from sortedcontainers import SortedKeyList
from rules.rule import Rule
from packet import Packet
from rules.action import Action
from switches.switch import Switch


class BasicSwitch (Switch):

    rules: SortedKeyList

    def __init__(self):
        self.rules = SortedKeyList([], key=lambda r: r.priority)

    def add_rule(self, rule: Rule):
        self.rules.add(rule)

    def remove_rule(self, rule: Rule):
        self.rules.remove(rule)

    def set_rules(self, new_rules: set):
        self.rules = SortedKeyList([], key=lambda r: r.priority)
        for rule in new_rules:
            self.rules.add(rule)

    def _get_action(self, packet: Packet):
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

    def packet_in(self, packet: Packet, port: int = None) -> Action:
        if port != None:
            packet.in_port = port

        action = self._get_action(packet)

        return action
