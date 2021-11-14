from sortedcontainers import SortedKeyList
from switches.switch import Switch
from switches.basic_switch import BasicSwitch
from rules.rule import Rule
from rules.action import Action, ActionType
from packet import Packet


class CacheSwitch (Switch):

    hw_switch: BasicSwitch
    hw_switch_size: int

    all_rules: SortedKeyList

    def __init__(self, hw_switch_size: int):
        """Create a new cache switch."""
        self.hw_switch = BasicSwitch()
        self.hw_switch_size = hw_switch_size

        self.all_rules = SortedKeyList([], key=lambda r: r.priority)

    def update(self):
        """Update the rules in the hardware and software switches."""

        # get a list of dependencies
        dependency_graph = []
        for i in range(len(self.all_rules)):
            dependencies = []
            for j in range(i + 1, len(self.all_rules)):
                # check if j is dependent on i
                for prev_dependency in dependencies:
                    if self.all_rules[j].intersects(self.all_rules[prev_dependency]):
                        dependencies.append(j)
            dependency_graph.append(dependencies)

        # cache rules
        # [TODO]

    def packet_in(self, packet: Packet, port: int) -> Action:
        """Send a packet into the switch on the given port."""
        packet.in_port = port

        # check if the packet matches in the hardware switch
        action = self.hw_switch.packet_in(packet)

        # check if we need to go to a software switch
        if action.type == ActionType.SOFTWARE_SWITCH:
            action = self.sw_switches[action.sw_switch_id].packet_in(
                packet)

        return action

    def add_rule(self, rule: Rule):
        """Add a rule to this switch."""
        self.hw_switch.add_rule(rule)
        pass

    def remove_rule(self, rule: Rule):
        """Remove a rule from this switch."""
        self.hw_switch.remove_rule(rule)
        pass
