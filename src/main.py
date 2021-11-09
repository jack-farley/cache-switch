from ipaddress import IPv4Network, ip_network
from rules.action import ForwardAction
from rules.pattern import IPv4DstPattern
from switches.cache_switch import CacheSwitch
from rules.rule import Rule
from packet import Packet


def main():

    switch = CacheSwitch(num_sw_switches=2, hw_switch_size=10)

    # create a rule
    pattern = IPv4DstPattern(ip_network('192.168.0.0/24'))
    action = ForwardAction(80)
    rule = Rule([pattern], action, 100)

    # add the rule
    switch.add_rule(rule)

    # create a packet
    packet = Packet(75, ip_network("192.168.0.2"),
                    ip_network("192.168.0.1"), 15, 16)

    # send the packet into the switch
    response_action = switch.packet_in(packet, 74)

    print(response_action.type)
    print(response_action.forward_port)


if __name__ == "__main__":
    main()
