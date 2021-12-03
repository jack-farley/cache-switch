from network.network import Network
from ipaddress import IPv4Network, ip_network
from network.switches.cache_switch import CacheSwitch
from network.rules.rule import Rule
from network.packet import Packet
from network.rules.action import ForwardAction, DropAction
from network.rules.pattern import IPv4DstPattern, InPortPattern
from network.switches.cache_algorithm import CacheAlgorithm


class TestNetwork (Network):

    def __init__(self, cache_algorithm: CacheAlgorithm):
        """Initialize the network and the switches."""
        super().__init__()
        self.init_topo(15, cache_algorithm)

    def init_topo(self, cache_size: int, cache_algorithm: CacheAlgorithm):

        # add the hosts
        self.add_host("h1", ip_network("10.0.1.1"))
        self.add_host("h2", ip_network("10.0.2.2"))
        self.add_host("h3", ip_network("10.0.3.3"))
        self.add_host("h4", ip_network("10.0.4.4"))
        self.add_host("h5", ip_network("10.0.5.5"))
        self.add_host("h6", ip_network("10.0.6.6"))

        # add the switches
        self.add_switch("s1", CacheSwitch(
            name="s1", algorithm=cache_algorithm, hw_switch_size=cache_size))
        self.add_switch("s2", CacheSwitch(
            name="s2", algorithm=cache_algorithm, hw_switch_size=cache_size))
        self.add_switch("s3", CacheSwitch(
            name="s3", algorithm=cache_algorithm, hw_switch_size=cache_size))
        self.add_switch("s4", CacheSwitch(
            name="s4", algorithm=cache_algorithm, hw_switch_size=cache_size))
        self.add_switch("s5", CacheSwitch(
            name="s5", algorithm=cache_algorithm, hw_switch_size=cache_size))
        self.add_switch("s6", CacheSwitch(
            name="s6", algorithm=cache_algorithm, hw_switch_size=cache_size))

        # add the links
        self.add_link("s1", 2, "s2", 1)
        self.add_link("s1", 3, "s3", 1)
        self.add_link("s1", 4, "s4", 1)
        self.add_link("s1", 5, "s5", 1)
        self.add_link("s1", 6, "s6", 1)

        # connect the hosts
        self.connect_host("h1", "s1", 1)
        self.connect_host("h2", "s2", 7)
        self.connect_host("h3", "s3", 7)
        self.connect_host("h4", "s4", 7)
        self.connect_host("h5", "s5", 7)
        self.connect_host("h6", "s6", 7)

        # install rules
        self.switches["s2"].add_rule(
            Rule([InPortPattern(7)], ForwardAction(1), 10))
        self.switches["s3"].add_rule(
            Rule([InPortPattern(7)], ForwardAction(1), 10))
        self.switches["s4"].add_rule(
            Rule([InPortPattern(7)], ForwardAction(1), 10))
        self.switches["s5"].add_rule(
            Rule([InPortPattern(7)], ForwardAction(1), 10))
        self.switches["s6"].add_rule(
            Rule([InPortPattern(7)], ForwardAction(1), 10))

        self.switches["s2"].add_rule(Rule([], ForwardAction(7), 1))
        self.switches["s3"].add_rule(Rule([], ForwardAction(7), 1))
        self.switches["s4"].add_rule(Rule([], ForwardAction(7), 1))
        self.switches["s5"].add_rule(Rule([], ForwardAction(7), 1))
        self.switches["s6"].add_rule(Rule([], ForwardAction(7), 1))

        self.switches["s1"].add_rule(
            Rule([InPortPattern(2)], ForwardAction(1), 100))
        self.switches["s1"].add_rule(
            Rule([InPortPattern(3)], ForwardAction(1), 100))
        self.switches["s1"].add_rule(
            Rule([InPortPattern(4)], ForwardAction(1), 100))
        self.switches["s1"].add_rule(
            Rule([InPortPattern(5)], ForwardAction(1), 100))
        self.switches["s1"].add_rule(
            Rule([InPortPattern(6)], ForwardAction(1), 100))

        # load balancing rules

        # depedent rules
        self.switches["s1"].add_rule(Rule(
            [InPortPattern(11), IPv4DstPattern(ip_network("10.0.2.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            3), IPv4DstPattern(ip_network("10.0.2.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            4), IPv4DstPattern(ip_network("10.0.2.0/24"))], DropAction, 50))

        self.switches["s1"].add_rule(Rule([InPortPattern(
            5), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            6), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            11), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            20), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            24), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            17), IPv4DstPattern(ip_network("10.0.3.0/24"))], DropAction, 50))

        self.switches["s1"].add_rule(Rule([InPortPattern(
            31), IPv4DstPattern(ip_network("10.0.4.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            45), IPv4DstPattern(ip_network("10.0.4.0/24"))], DropAction, 50))

        self.switches["s1"].add_rule(Rule([InPortPattern(
            51), IPv4DstPattern(ip_network("10.0.5.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            61), IPv4DstPattern(ip_network("10.0.5.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            112), IPv4DstPattern(ip_network("10.0.5.0/24"))], DropAction, 50))
        self.switches["s1"].add_rule(Rule([InPortPattern(
            201), IPv4DstPattern(ip_network("10.0.5.0/24"))], DropAction, 50))

        self.switches["s1"].add_rule(Rule([InPortPattern(
            23), IPv4DstPattern(ip_network("10.0.6.0/24"))], DropAction, 50))

        # main rules
        self.switches["s1"].add_rule(
            Rule([IPv4DstPattern(ip_network("10.0.2.2"))], ForwardAction(2), 10))
        self.switches["s1"].add_rule(
            Rule([IPv4DstPattern(ip_network("10.0.3.3"))], ForwardAction(3), 10))
        self.switches["s1"].add_rule(
            Rule([IPv4DstPattern(ip_network("10.0.4.4"))], ForwardAction(4), 10))
        self.switches["s1"].add_rule(
            Rule([IPv4DstPattern(ip_network("10.0.5.5"))], ForwardAction(5), 10))
        self.switches["s1"].add_rule(
            Rule([IPv4DstPattern(ip_network("10.0.6.6"))], ForwardAction(6), 10))

    def packet_in(self, packet: Packet, switch_name: str):
        # drop the packet
        self.drop_packet(packet)


def general_test(cache_algorithm: CacheAlgorithm):
    network = TestNetwork(cache_algorithm)

    for i in range(10):
        for j in range(5):
            network.send_packet("h1", 1, "h2", 1)
        for j in range(15):
            network.send_packet("h1", 1, "h3", 1)
        for j in range(2):
            network.send_packet("h1", 1, "h4", 1)
        for j in range(3):
            network.send_packet("h1", 1, "h5", 1)
        for j in range(10):
            network.send_packet("h1", 1, "h6", 1)

    packets_in, arrived, dropped = network.get_stats()

    print("Packets In: " + str(packets_in))
    print("Packets Arrived: " + str(arrived))
    print("Packets Dropped: " + str(dropped))

    print()

    packets, hits, misses = network.get_cache_switch_stats("s1")

    print("Packets through s1: " + str(packets))
    print("Hits: " + str(hits))
    print("Misses: " + str(misses))
