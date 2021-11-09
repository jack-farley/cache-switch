from switches.switch import Switch
from rules.rule import Rule
from rules.action import Action, ActionType
from packet import Packet


class CacheSwitch:

    hw_switch: Switch
    hw_switch_size: int
    sw_switches: list

    def __init__(self, num_sw_switches: int, hw_switch_size: int):
        """Create a new cache switch."""
        self.hw_switch = Switch()
        self.hw_switch_size = hw_switch_size
        self.sw_switches = []
        for i in range(num_sw_switches):
            self.sw_switches.append(Switch())

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
