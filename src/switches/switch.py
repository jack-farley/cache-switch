from rules.rule import Rule
from packet import Packet
from rules.action import Action


class Switch:

    def add_rule(self, rule: Rule):
        """Add a rule to this switch."""
        pass

    def remove_rule(self, rule: Rule):
        """Remove a rule from this switch."""
        pass

    def set_rules(self, new_rules: set):
        """Set the rules in this table."""
        pass

    def packet_in(self, packet: Packet, port: int = None) -> Action:
        """Send a packet intot the switch on the given port."""
        pass
