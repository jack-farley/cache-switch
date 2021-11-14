from rules.rule import Rule
from packet import Packet
from rules.action import Action
from switches.table import Table
from switches.switch import Switch


class BasicSwitch (Switch):

    table: Table

    def __init__(self):
        self.table = Table()

    def add_rule(self, rule: Rule):
        self.table.add_rule(rule)

    def remove_rule(self, rule: Rule):
        self.table.remove_rule(rule)

    def packet_in(self, packet: Packet, port: int = None) -> Action:
        if port != None:
            packet.in_port = port

        action = self.table.get_action(packet)

        return action
