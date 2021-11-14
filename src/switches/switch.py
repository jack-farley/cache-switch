from rules.rule import Rule
from packet import Packet
from rules.action import Action
from switches.table import Table


class Switch:

    def add_rule(self, rule: Rule):
        """Add a rule to this switch."""
        pass

    def remove_rule(self, rule: Rule):
        """Remove a rule from this switch."""
        pass

    def packet_in(self, packet: Packet, port: int = None) -> Action:
        """Send a packet intot the switch on the given port."""
        pass
