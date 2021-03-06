import logging
from ipaddress import IPv4Network, ip_network
from rules.action import ForwardAction
from rules.pattern import IPv4DstPattern
from switches.cache_switch import CacheSwitch
from rules.rule import Rule
from network.packet import Packet
from switches.cache_algorithm import CacheAlgorithm

from tests.general_test import general_test


def start_logging():
    logging.basicConfig(level=logging.ERROR)


def basic_switch_test():

    logging.info("[Main] Creating cache switch.")
    switch = CacheSwitch(hw_switch_size=10)

    # create a rule
    logging.info("[Main] Creating a basic rule.")
    pattern = IPv4DstPattern(ip_network('192.168.0.0/24'))
    action = ForwardAction(80)
    rule = Rule([pattern], action, 100)

    # add the rule
    logging.info("[Main] Adding the rule.")
    switch.add_rule(rule)

    # create a packet
    logging.info("[Main] Creating a basic packet.")
    packet = Packet(75, ip_network("192.168.0.2"),
                    ip_network("192.168.0.1"), 15, 16)

    # send the packet into the switch
    logging.info("[Main] Sending the packet to the switch.")
    response_action = switch.packet_in(packet, 74)

    # print results
    print(response_action.type)
    print(response_action.forward_port)

    print("Pakcets: " + str(switch.num_packets))
    print("Misses: " + str(switch.num_misses))


def main():
    start_logging()

    general_test(CacheAlgorithm.DEPENDENT_SET)
    general_test(CacheAlgorithm.COVER_SET)
    general_test(CacheAlgorithm.MIXED_SET)


if __name__ == "__main__":
    main()
