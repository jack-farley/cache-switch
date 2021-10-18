from sortedcontainers import SortedKeyList
from rules.rule import Rule
from packet import Packet
from rules.action import Action


class Switch:

    rules: SortedKeyList

    def __init__(self):
        """Create a new switch."""
        self.rules = SortedKeyList([], key=lambda r: r.priority)

    def add_rule(self, rule: Rule):
        """"Add a rule to this switch."""
        self.rules.add(rule)

    def packet_in(self, packet: Packet, port: int) -> Action:
        """Send a packet into the switch on the given port."""
        packet.in_port = port

        # check if we have a rule matching this packet
        action: Action = None
        for rule in self.rules.__reversed__():
            if rule.matches(packet):
                action = rule.action()

        return action
